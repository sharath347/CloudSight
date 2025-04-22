import subprocess
import os
import json
import re
import glob
import shutil
import os
from flask import jsonify
from pymongo import MongoClient

def run_scoutsuite_aws(scan_id):
    output_dir = f"output/{scan_id}"
    os.makedirs(output_dir, exist_ok=True)

    env = os.environ.copy()
    env["SCOUTSUITE_NO_BROWSER"] = "true"  # Prevents ScoutSuite from opening browser

    try:
        result = subprocess.run(
            ["scout", "aws", "--no-browser", "--report-dir", output_dir],
            capture_output=True,
            text=True,
            env=env
        )

        if result.returncode != 0:
            return {"success": False, "message": result.stderr}

        folder_path = f"output/{scan_id}/scoutsuite-results/"
    
        # Pattern to match files like scoutsuite_results_aws-*.js
        pattern = os.path.join(folder_path, "scoutsuite_results_aws-*.js")
        
        matching_files = glob.glob(pattern)
        
        if not matching_files:
            return jsonify({"success": False, "message": "ScoutSuite result file not found"}), 404

        js_path = matching_files[0]
        with open(js_path, "r") as f:
            content = f.read()

        match = re.search(r'scoutsuite_results\s*=\s*(\{.*\})', content, re.DOTALL)
        if not match:
            return {"success": False, "message": "Could not extract JSON from .js file"}

        json_data = json.loads(match.group(1))

        # Insert into MongoDB
        client = MongoClient("mongodb://admin:admin@mongodb:27017/")
        db = client["scoutsuite"]
        collection = db["scan_results"]
        collection.insert_one({
            "scan_id": scan_id,
            "data": json_data
        })

        # Delete the .js file after insertion
        output_dir = f"output/{scan_id}"

        if os.path.exists(output_dir):
            shutil.rmtree(output_dir)
            print(f"Deleted directory: {output_dir}")
        else:
            print(f"Directory does not exist: {output_dir}")

        # Return success with optional report path
        report_path = os.path.join(output_dir, "scoutsuite-report", "scoutsuite-report.html")
        return {
            "success": True,
            "message": "Scan completed and data saved to MongoDB.",
            "scan_id": scan_id,
            "report_path": report_path
        }

    except Exception as e:
        return {"success": False, "message": str(e)}