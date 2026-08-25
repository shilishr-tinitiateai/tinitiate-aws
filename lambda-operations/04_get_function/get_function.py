"""
===============================================================================
MODULE: AWS Lambda Function Inspector
===============================================================================
Description:
    This script connects to AWS Lambda (or LocalStack mock environment) and 
    fetches detailed metadata, runtime configurations, and the pre-signed 
    code deployment package URL of a target function using Boto3 SDK.

Dependencies:
    - boto3 (AWS SDK for Python)
    - json (Standard Library)
    - os (Standard Library)

Usage:
    python get_function.py
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
# Set endpoint URL (defaults to LocalStack port 4566)
ENDPOINT_URL = os.getenv("AWS_ENDPOINT_URL", "http://localhost:4566")

# Set AWS region
REGION_NAME = os.getenv("AWS_DEFAULT_REGION", "us-east-1")

# Target function name to inspect
FUNCTION_NAME = "my-first-lambda"

# =============================================================================
# SECTION 3: MAIN EXECUTION FUNCTION
# =============================================================================
def main():
    """
    Main execution function: Initializes Boto3 Lambda client and fetches details 
    for the specified function name.
    """
    print(f"🚀 Initializing AWS Lambda Client (Endpoint: {ENDPOINT_URL})...")
    
    # Instantiate the Lambda client
    lambda_client = boto3.client(
        "lambda",
        region_name=REGION_NAME,
        endpoint_url=ENDPOINT_URL,
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID", "test"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY", "test")
    )

    try:
        print(f"🔍 Fetching configuration and code details for '{FUNCTION_NAME}'...")
        
        # Invoke GetFunction API call
        response = lambda_client.get_function(FunctionName=FUNCTION_NAME)

        config = response.get("Configuration", {})
        code_info = response.get("Code", {})

        print("\n⚙️ Function Configuration:")
        print(f"• Name:        {config.get('FunctionName')}")
        print(f"• ARN:         {config.get('FunctionArn')}")
        print(f"• Runtime:     {config.get('Runtime')}")
        print(f"• Handler:     {config.get('Handler')}")
        print(f"• Code Size:   {config.get('CodeSize')} bytes")
        print(f"• Memory Size: {config.get('MemorySize')} MB")
        print(f"• Timeout:     {config.get('Timeout')} s")
        print(f"• State:       {config.get('State', 'Active')}")

        print("\n📦 Code Metadata:")
        print(f"• Location URL: {code_info.get('Location', 'N/A')[:80]}...")
        print(f"• Repository:   {code_info.get('RepositoryType', 'S3')}")

        print("\n📊 Full Raw Response JSON:")
        print(json.dumps(response, indent=2, default=str))

    except lambda_client.exceptions.ResourceNotFoundException:
        print(f"❌ Function '{FUNCTION_NAME}' was not found.")
    except Exception as e:
        print(f"❌ Error getting function details: {e}")

# =============================================================================
# SECTION 4: SCRIPT ENTRY POINT
# =============================================================================
if __name__ == "__main__":
    main()
