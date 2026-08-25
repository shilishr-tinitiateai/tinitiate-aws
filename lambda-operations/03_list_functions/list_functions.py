"""
===============================================================================
MODULE: AWS Lambda Functions Lister
===============================================================================
Description:
    This script connects to AWS Lambda (or LocalStack mock environment) and 
    retrieves a list of all deployed Lambda functions in the target region 
    using the Boto3 SDK.

Dependencies:
    - boto3 (AWS SDK for Python)
    - json (Standard Library)
    - os (Standard Library)

Usage:
    python list_functions.py
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

# =============================================================================
# SECTION 3: MAIN EXECUTION FUNCTION
# =============================================================================
def main():
    """
    Main execution function: Initializes Boto3 Lambda client and lists all 
    functions deployed in the configured region.
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
        print("🔍 Listing all deployed Lambda functions...")
        
        # Invoke ListFunctions API call
        response = lambda_client.list_functions()

        functions = response.get("Functions", [])
        print(f"✅ Found {len(functions)} Lambda function(s).")
        
        print("\n📋 Functions Summary:")
        print("-" * 60)
        for fn in functions:
            print(f"• Name:        {fn.get('FunctionName')}")
            print(f"  Runtime:     {fn.get('Runtime')}")
            print(f"  Handler:     {fn.get('Handler')}")
            print(f"  Code Size:   {fn.get('CodeSize')} bytes")
            print(f"  Memory Size: {fn.get('MemorySize')} MB")
            print(f"  Timeout:     {fn.get('Timeout')} seconds")
            print(f"  ARN:         {fn.get('FunctionArn')}")
            print("-" * 60)

        print("\n📊 Full Raw JSON Response:")
        print(json.dumps(response, indent=2, default=str))

    except Exception as e:
        print(f"❌ Error listing functions: {e}")

# =============================================================================
# SECTION 4: SCRIPT ENTRY POINT
# =============================================================================
if __name__ == "__main__":
    main()
