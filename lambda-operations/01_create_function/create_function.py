"""
===============================================================================
MODULE: AWS Lambda Function Creator
===============================================================================
Description:
    This script compresses the local `lambda_function.py` source code into an 
    in-memory ZIP deployment archive and calls the Boto3 AWS Lambda SDK 
    `create_function` API to deploy a new Lambda function to LocalStack or 
    real AWS Cloud.

Dependencies:
    - boto3 (AWS SDK for Python)
    - zipfile (Standard Library)
    - io (Standard Library)
    - os (Standard Library)

Usage:
    python create_function.py
===============================================================================
"""

# =============================================================================
# SECTION 1: IMPORTS
# =============================================================================
import boto3
import zipfile
import io
import os
import json

# =============================================================================
# SECTION 2: GLOBAL CONFIGURATION & ENVIRONMENT VARIABLES
# =============================================================================
# LocalStack mock endpoint (defaults to http://localhost:4566)
ENDPOINT_URL = os.getenv("AWS_ENDPOINT_URL", "http://localhost:4566")

# AWS Region setting
REGION_NAME = os.getenv("AWS_DEFAULT_REGION", "us-east-1")

# Target Lambda Function Parameters
FUNCTION_NAME = "my-first-lambda"
ROLE_ARN = "arn:aws:iam::123456789012:role/lambda-execution-role"
RUNTIME = "python3.12"
HANDLER = "lambda_function.lambda_handler"

# =============================================================================
# SECTION 3: HELPER FUNCTIONS
# =============================================================================
def create_zip_in_memory():
    """
    Compresses lambda_function.py into a ZIP byte payload directly in memory.
    
    Returns:
        bytes: Raw byte contents of the created ZIP deployment package.
    """
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        file_path = os.path.join(os.path.dirname(__file__), "lambda_function.py")
        zip_file.write(file_path, arcname="lambda_function.py")
    zip_buffer.seek(0)
    return zip_buffer.read()

# =============================================================================
# SECTION 4: MAIN EXECUTION FUNCTION
# =============================================================================
def main():
    """
    Initializes the Boto3 Lambda client, generates the ZIP package, and creates 
    the Lambda function via API call.
    """
    print(f"🚀 Initializing AWS Lambda Client (Endpoint: {ENDPOINT_URL})...")
    
    # Initialize Boto3 Lambda client with endpoint and fallback credentials
    lambda_client = boto3.client(
        "lambda",
        region_name=REGION_NAME,
        endpoint_url=ENDPOINT_URL,
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID", "test"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY", "test")
    )

    # Generate in-memory ZIP package bytes
    zip_bytes = create_zip_in_memory()

    try:
        print(f"📦 Creating Lambda function '{FUNCTION_NAME}'...")
        
        # Invoke CreateFunction API call
        response = lambda_client.create_function(
            FunctionName=FUNCTION_NAME,
            Runtime=RUNTIME,
            Role=ROLE_ARN,
            Handler=HANDLER,
            Code={'ZipFile': zip_bytes},
            Description="Initial deployment of demo lambda function",
            Timeout=15,
            MemorySize=128,
            Publish=True
        )

        print("✅ Lambda Function Created Successfully!")
        print("📊 Response Details:")
        print(json.dumps({
            "FunctionName": response.get("FunctionName"),
            "FunctionArn": response.get("FunctionArn"),
            "Runtime": response.get("Runtime"),
            "Role": response.get("Role"),
            "Handler": response.get("Handler"),
            "CodeSize": response.get("CodeSize"),
            "State": response.get("State", "Active"),
            "LastModified": response.get("LastModified")
        }, indent=2))

    except lambda_client.exceptions.ResourceConflictException:
        print(f"⚠️ Function '{FUNCTION_NAME}' already exists.")
    except Exception as e:
        print(f"❌ Error creating function: {e}")

# =============================================================================
# SECTION 5: SCRIPT ENTRY POINT
# =============================================================================
if __name__ == "__main__":
    main()
