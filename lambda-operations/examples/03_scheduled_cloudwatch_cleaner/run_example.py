"""
===============================================================================
EXAMPLE 3 DEPLOYMENT & EXECUTION RUNNER
===============================================================================
Description:
    Packages lambda_function.py, creates the scheduled cleaner function, 
    invokes it with sample_timer_event.json, and prints returned metrics.

Dependencies:
    - boto3 (AWS SDK for Python)
===============================================================================
"""

import boto3
from botocore.config import Config
import zipfile
import io
import os
import sys
import json

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ENDPOINT_URL = os.getenv("AWS_ENDPOINT_URL", "http://localhost:4566")
REGION_NAME = os.getenv("AWS_DEFAULT_REGION", "us-east-1")

FUNCTION_NAME = "scheduled-cron-cleaner-example"
ROLE_ARN = "arn:aws:iam::123456789012:role/lambda-cron-role"
RUNTIME = "python3.12"
HANDLER = "lambda_function.lambda_handler"

EVENT_FILE = os.path.join(os.path.dirname(__file__), "sample_timer_event.json")
BOTO_CONFIG = Config(connect_timeout=3, read_timeout=3, retries={'max_attempts': 1})

def create_zip_bytes():
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        file_path = os.path.join(os.path.dirname(__file__), "lambda_function.py")
        zip_file.write(file_path, arcname="lambda_function.py")
    zip_buffer.seek(0)
    return zip_buffer.read()

def main():
    print(f"🚀 Initializing AWS Lambda Client (Endpoint: {ENDPOINT_URL})...")
    
    lambda_client = boto3.client(
        "lambda",
        region_name=REGION_NAME,
        endpoint_url=ENDPOINT_URL,
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID", "test"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY", "test"),
        config=BOTO_CONFIG
    )

    zip_bytes = create_zip_bytes()

    try:
        print(f"📦 Deploying Lambda function '{FUNCTION_NAME}'...")
        lambda_client.create_function(
            FunctionName=FUNCTION_NAME,
            Runtime=RUNTIME,
            Role=ROLE_ARN,
            Handler=HANDLER,
            Code={'ZipFile': zip_bytes},
            Description="Example 3: Scheduled Cron Task Cleaner",
            Timeout=15,
            MemorySize=128
        )
        print("✅ Function created successfully!")
    except lambda_client.exceptions.ResourceConflictException:
        print(f"🔄 Updating code for '{FUNCTION_NAME}'...")
        lambda_client.update_function_code(
            FunctionName=FUNCTION_NAME,
            ZipFile=zip_bytes
        )
        print("✅ Function code updated successfully!")
    except Exception as e:
        if "Could not connect to the endpoint URL" in str(e) or "ConnectTimeoutError" in str(e):
            print(f"⚠️ Note: Endpoint {ENDPOINT_URL} is offline (LocalStack container not running).")
            print("💡 Start LocalStack with 'docker run -p 4566:4566 localstack/localstack' or run against real AWS Cloud.")
            return
        else:
            print(f"❌ Error deploying function: {e}")

    with open(EVENT_FILE, "r") as f:
        event_payload = json.load(f)

    try:
        print("⚡ Invoking Scheduled Cron Task function...")
        response = lambda_client.invoke(
            FunctionName=FUNCTION_NAME,
            InvocationType="RequestResponse",
            Payload=json.dumps(event_payload).encode("utf-8")
        )

        result_raw = response["Payload"].read().decode("utf-8")
        result_json = json.loads(result_raw)

        print("\n📊 Returned Scheduled Execution Metrics:")
        print(json.dumps(result_json, indent=2))
    except Exception as e:
        print(f"❌ Execution Error: {e}")

if __name__ == "__main__":
    main()
