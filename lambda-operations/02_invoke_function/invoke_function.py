"""
===============================================================================
MODULE: AWS Lambda Function Invoker
===============================================================================
Description:
    This script connects to AWS Lambda (or LocalStack mock environment), 
    loads an event payload from `payload.json`, synchronously invokes the target 
    Lambda function using Boto3 SDK, and writes the returned response body to 
    `response.json`.

Dependencies:
    - boto3 (AWS SDK for Python)
    - json (Standard Library)
    - os (Standard Library)

Usage:
    python invoke_function.py
===============================================================================
"""

# =============================================================================
# SECTION 1: IMPORTS
# =============================================================================
import boto3
import json
import os

# =============================================================================
# SECTION 2: GLOBAL CONFIGURATION & ENVIRONMENT VARIABLES
# =============================================================================
# Set target endpoint URL (defaults to LocalStack port 4566)
ENDPOINT_URL = os.getenv("AWS_ENDPOINT_URL", "http://localhost:4566")

# Set AWS region
REGION_NAME = os.getenv("AWS_DEFAULT_REGION", "us-east-1")

# Target Lambda Function and payload file paths
FUNCTION_NAME = "my-first-lambda"
PAYLOAD_FILE = os.path.join(os.path.dirname(__file__), "payload.json")
OUTPUT_FILE = os.path.join(os.path.dirname(__file__), "response.json")

# =============================================================================
# SECTION 3: MAIN EXECUTION FUNCTION
# =============================================================================
def main():
    """
    Main execution function: Loads payload.json, invokes the Lambda function, 
    and writes execution output to response.json.
    """
    print(f"🚀 Initializing AWS Lambda Client (Endpoint: {ENDPOINT_URL})...")
    
    # Initialize Boto3 Lambda client
    lambda_client = boto3.client(
        "lambda",
        region_name=REGION_NAME,
        endpoint_url=ENDPOINT_URL,
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID", "test"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY", "test")
    )

    # Read input payload file
    if os.path.exists(PAYLOAD_FILE):
        with open(PAYLOAD_FILE, "r") as f:
            payload_data = json.load(f)
    else:
        payload_data = {"name": "Alice"}

    payload_json = json.dumps(payload_data)
    print(f"📩 Sending Input Payload: {payload_json}")

    try:
        print(f"⚡ Invoking Lambda function '{FUNCTION_NAME}'...")
        
        # Invoke Lambda function synchronously (RequestResponse)
        response = lambda_client.invoke(
            FunctionName=FUNCTION_NAME,
            InvocationType="RequestResponse",  # Synchronous execution
            LogType="Tail",                    # Request CloudWatch log tail
            Payload=payload_json.encode("utf-8")
        )

        status_code = response.get("StatusCode")
        print(f"✅ Invocation Finished with HTTP Status Code: {status_code}")
        
        # Read returned payload stream and parse JSON
        response_payload_raw = response["Payload"].read().decode("utf-8")
        response_payload = json.loads(response_payload_raw)

        # Save result payload to response.json
        with open(OUTPUT_FILE, "w") as f:
            json.dump(response_payload, f, indent=2)

        print(f"💾 Response saved to '{OUTPUT_FILE}'")
        print("📊 Returned Lambda Output Body:")
        print(json.dumps(response_payload, indent=2))

    except lambda_client.exceptions.ResourceNotFoundException:
        print(f"❌ Error: Function '{FUNCTION_NAME}' does not exist. Please create it first.")
    except Exception as e:
        print(f"❌ Execution Error: {e}")

# =============================================================================
# SECTION 4: SCRIPT ENTRY POINT
# =============================================================================
if __name__ == "__main__":
    main()
