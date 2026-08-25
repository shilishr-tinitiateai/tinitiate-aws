"""
===============================================================================
MODULE: AWS Lambda Function Code Updater
===============================================================================
Description:
    This script compresses `lambda_function_v2.py` as `lambda_function.py` inside 
    an in-memory ZIP deployment archive, connects to AWS Lambda via Boto3, and 
    invokes `update_function_code` to deploy the new code version.

Dependencies:
    - boto3 (AWS SDK for Python)
    - zipfile (Standard Library)
    - io (Standard Library)
    - os (Standard Library)

Usage:
    python update_function_code.py
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
# Set target endpoint URL (defaults to LocalStack port 4566)
ENDPOINT_URL = os.getenv("AWS_ENDPOINT_URL", "http://localhost:4566")

# Set AWS region
REGION_NAME = os.getenv("AWS_DEFAULT_REGION", "us-east-1")

# Target Lambda Function name
FUNCTION_NAME = "my-first-lambda"

# =============================================================================
# SECTION 3: HELPER FUNCTIONS
# =============================================================================
def create_updated_zip_in_memory():
    """
    Compresses lambda_function_v2.py into a ZIP package byte stream, aliasing 
    the internal filename to lambda_function.py so the handler entry point 
    remains valid.

    Returns:
        bytes: Compressed ZIP archive raw byte stream.
    """
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        file_path = os.path.join(os.path.dirname(__file__), "lambda_function_v2.py")
        zip_file.write(file_path, arcname="lambda_function.py")
    zip_buffer.seek(0)
    return zip_buffer.read()

# =============================================================================
# SECTION 4: MAIN EXECUTION FUNCTION
# =============================================================================
def main():
    """
    Main execution function: Initializes Boto3 Lambda client, builds the v2 ZIP 
    deployment package, and calls update_function_code.
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

    # Generate in-memory v2 ZIP archive bytes
    zip_bytes = create_updated_zip_in_memory()

    try:
        print(f"🔄 Updating code for Lambda function '{FUNCTION_NAME}'...")
        
        # Invoke UpdateFunctionCode API call
        response = lambda_client.update_function_code(
            FunctionName=FUNCTION_NAME,
            ZipFile=zip_bytes,
            Publish=True
        )

        print("✅ Lambda Function Code Updated Successfully!")
        print("📊 Updated Function Details:")
        print(json.dumps({
            "FunctionName": response.get("FunctionName"),
            "FunctionArn": response.get("FunctionArn"),
            "CodeSize": response.get("CodeSize"),
            "CodeSha256": response.get("CodeSha256"),
            "Version": response.get("Version"),
            "LastModified": response.get("LastModified")
        }, indent=2))

    except lambda_client.exceptions.ResourceNotFoundException:
        print(f"❌ Function '{FUNCTION_NAME}' does not exist. Please create it first.")
    except Exception as e:
        print(f"❌ Error updating function code: {e}")

# =============================================================================
# SECTION 5: SCRIPT ENTRY POINT
# =============================================================================
if __name__ == "__main__":
    main()
