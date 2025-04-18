from keycloak import KeycloakAdmin
from functools import wraps
from flask import request, jsonify
import requests
from keycloak.exceptions import KeycloakGetError

def get_keycloak_admin():
    keycloak_admin = KeycloakAdmin(
        server_url="http://localhost:9000/",
        realm_name="security",
        client_id="security",  # Your confidential client ID
        client_secret_key="fVnoa6QyQNE89DkcxTCCrj24SR2J9dep",  # Your client secret
        verify=True  # Set to False if you're using a self-signed certificate
    )
    return keycloak_admin

def update_user_in_keycloak(username, first_name, last_name, email):
    keycloak_admin = get_keycloak_admin()
    
    # Step 1: Get user by username
    users = keycloak_admin.get_users({"username": username})

    if users:
        user_id = users[0]["id"]

        # Step 2: Prepare the update payload
        update_payload = {
            "firstName": first_name,
            "lastName": last_name,
            "email": email,
        }

        # Step 3: Update the user
        keycloak_admin.update_user(user_id=user_id, payload=update_payload)
        return {"message": f"User {username} updated successfully."}
    else:
        return {"error": "User not found"}

def increment_user_counter(user_id):
    try:
        keycloak_admin = get_keycloak_admin()

        # Fetch current user details
        user = keycloak_admin.get_user(user_id)

        # Preserve essential fields
        current_first_name = user.get("firstName", "")
        current_last_name = user.get("lastName", "")
        current_email = user.get("email", "")
        current_username = user.get("username", "")
        current_attributes = user.get("attributes", {})

        # Get current counter value from attributes
        current_counter = current_attributes.get("counter", ["0"])[0]
        new_counter = str(int(current_counter) + 1)

        # Update only the counter attribute but keep others intact
        current_attributes["counter"] = new_counter

        # Prepare full payload
        update_payload = {
            "firstName": current_first_name,
            "lastName": current_last_name,
            "email": current_email,
            "username": current_username,
            "attributes": current_attributes
        }

        # Update user in Keycloak
        keycloak_admin.update_user(user_id=user_id, payload=update_payload)

        return {"success": True, "message": f"Counter updated to {new_counter}"}

    except KeycloakGetError as ke:
        print(f"Keycloak error while updating counter: {ke}")
        return {"success": False, "message": "Keycloak error while updating counter"}

    except Exception as e:
        print(f"Unexpected error updating counter: {e}")
        return {"success": False, "message": "Unexpected error while updating counter"}

# Token introspection
def introspect_token(token):
    url = "http://localhost:9000/realms/security/protocol/openid-connect/token/introspect"
    
    client_id = "security"
    client_secret = "fVnoa6QyQNE89DkcxTCCrj24SR2J9dep"

    response = requests.post(url, data={
        "token": token,
        "client_id": client_id,
        "client_secret": client_secret
    })

    return response.json()

# Middleware to protect routes
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get("Authorization", "").replace("Bearer ", "")
        if not token:
            return jsonify({"error": "Missing token"}), 401

        result = introspect_token(token)
        if not result.get("active"):
            return jsonify({"error": "Invalid or expired token"}), 401

        # Store the user ID and other user information in the request object
        request.user = {
            "user_id": result.get("sub"),  # Assuming the 'sub' claim holds the user ID
            "username": result.get("preferred_username"),
            "email": result.get("email"),
            "first_name": result.get("given_name"),
            "last_name": result.get("family_name"),
        }
        return f(*args, **kwargs)

    return decorated
