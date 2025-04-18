from flask import Flask, request, jsonify
import os
import boto3
import uuid
from jose import jwt
from botocore.exceptions import NoCredentialsError
from pymongo import MongoClient
from flask import Flask, jsonify, request
from authentication import increment_user_counter
from authentication import token_required, update_user_in_keycloak

app = Flask(__name__)

# MongoDB setup (initialize once)
client = MongoClient("mongodb://admin:admin@localhost:27017/")
db = client["scoutsuite"]
collection = db["scan_results"]

def parse_scout_results(scan_id):

    try:

        # find the document by scan_id
        result = collection.find_one({"scan_id": scan_id})
        # Extract summary information
        summary = result["data"].get("last_run", {}).get("summary", {})

        # List all services in the summary
        services = list(summary.keys())
        print("All services in the summary:", services)

        # Optionally, you can also print the full details of each service
        for service, details in summary.items():
            print(f"Details for {service}: {details}")
        
        return {"success": True, "summary": summary}

    except Exception as e:
        print(f"Error occurred: {e}")
        return {"success": False, "message": str(e)}

@app.route('/get_summary/<scan_id>', methods=['GET'])
def get_summary(scan_id):
    result = parse_scout_results(scan_id)
    
    if result["success"]:
        return jsonify(result), 200
    else:
        return jsonify(result), 500

@app.route('/get_findings/<scan_id>/<service_name>', methods=['GET'])
@token_required
def get_findings(scan_id, service_name):

    try:

        # find the document by scan_id
        result = collection.find_one({"scan_id": scan_id})
        services = result["data"].get("services", {})
        service_data = services.get(service_name.lower())

        if not service_data:
            return jsonify({"success": False, "message": f"Service '{service_name}' not found in report"}), 404

        findings = service_data.get("findings", {})
        return jsonify({"success": True, "findings": findings}), 200

    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

@app.route('/get_service_groups/<scan_id>', methods=['GET'])
@token_required
def get_service_groups(scan_id):
    try:
        # find the document by scan_id
        result = collection.find_one({"scan_id": scan_id})

        metadata = result["data"].get("metadata", {})
        service_groups = {}

        for group, services in metadata.items():
            if isinstance(services, dict):
                service_groups[group] = list(services.keys())
            else:
                service_groups[group] = []

        return jsonify({"success": True, "service_groups": service_groups}), 200

    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

@app.route('/get_service_list/<scan_id>', methods=['GET'])
@token_required
def get_service_list(scan_id):
    try:
        # Insert into MongoDB
        client = MongoClient("mongodb://admin:admin@localhost:27017/")
        db = client["scoutsuite"]
        collection = db["scan_results"]

        # find the document by scan_id
        result = collection.find_one({"scan_id": scan_id})

        service_list = result["data"].get("service_list", [])

        return jsonify({"success": True, "service_list": service_list}), 200

    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

@app.route('/run-scoutsuite', methods=['POST'])
@token_required
def run_scan():
    data = request.get_json()
    aws_access_key = data.get('aws_access_key')
    aws_secret_key = data.get('aws_secret_key')
    region = data.get('region', 'us-east-1')

    if not aws_access_key or not aws_secret_key:
        return jsonify({"success": False, "message": "AWS credentials are required"}), 400

    os.environ["AWS_ACCESS_KEY_ID"] = aws_access_key
    os.environ["AWS_SECRET_ACCESS_KEY"] = aws_secret_key
    os.environ["AWS_DEFAULT_REGION"] = region

    try:
        sts = boto3.client("sts")
        sts.get_caller_identity()
    except NoCredentialsError:
        return jsonify({"success": False, "message": "Invalid AWS credentials"}), 403
    except Exception as e:
        return jsonify({"success": False, "message": f"Error verifying credentials: {str(e)}"}), 500

    #scan_id = str(uuid.uuid4())

    from scoutsuite_runner import run_scoutsuite_aws
    result = run_scoutsuite_aws(request.user.get("user_id"))

    user_id = request.user.get("user_id")
    counter_update_result = increment_user_counter(user_id)

    if not counter_update_result.get("success"):
        return jsonify(counter_update_result), 500
    
    return jsonify({"success": True, "message": "Scan done and counter updated successfully"}), 200

def main():
    print("Parsing ScoutSuite results...")


# API endpoint to get user details using the access token
@app.route('/user-details', methods=['GET'])
@token_required
def user_details():
    token = request.headers.get('Authorization')

    if not token:
        return jsonify({'error': 'Token missing'}), 400

    # Strip the 'Bearer ' prefix from token
    token = token.replace("Bearer ", "")

    try:
        # Decode without verifying signature (unsafe for production)
        decoded = jwt.get_unverified_claims(token)

        return {
            "username": decoded.get("preferred_username"),
            "email": decoded.get("email"),
            "first_name": decoded.get("given_name"),
            "last_name": decoded.get("family_name"),
            "full_name": decoded.get("name"),
            "counter": decoded.get("counter"),
        }
    
    except Exception as e:
        print(f"Error decoding token: {e}")
        return {}
    

# POST endpoint to update user details
@app.route('/update-user', methods=['POST'])
def update_user():
    # Extract user data from the request JSON body
    data = request.json
    username = data.get("username")
    first_name = data.get("firstName")
    last_name = data.get("lastName")
    email = data.get("email")

    # Ensure username is provided
    if not username:
        return jsonify({"error": "Username is required"}), 400

    # Step 1: Call the update_user_in_keycloak function from authentication.py
    result = update_user_in_keycloak(username, first_name, last_name, email)

    if "message" in result:
        return jsonify(result), 200
    else:
        return jsonify(result), 404


if __name__ == '__main__':
    main()
    app.run(debug=True)


