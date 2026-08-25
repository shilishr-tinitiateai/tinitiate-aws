"""
===============================================================================
MODULE: AWS Lambda Function Deleter
===============================================================================
Description:
    This script connects to AWS Lambda (or LocalStack mock environment) 
    and deletes a specified Lambda function using the boto3 SDK.

Dependencies:
    - boto3 (AWS SDK for Python)

Usage:
    python delete_lambda.py
===============================================================================
"""

# =============================================================================
# SECTION 1: IMPORTS
# =============================================================================
import boto3
import os

# =============================================================================
# SECTION 2: GLOBAL CONFIGURATION & ENVIRONMENT VARIABLES
# =============================================================================
# Set endpoint URL (defaults to LocalStack port 4566 if env var is not set)
ENDPOINT_URL = os.getenv("AWS_ENDPOINT_URL", "http://localhost:4566")

# Set AWS region (defaults to us-east-1 if env var is not set)
REGION_NAME = os.getenv("AWS_DEFAULT_REGION", "us-east-1")

# The exact name of the Lambda function to be deleted
FUNCTION_NAME = "my-first-lambda"

# =============================================================================
# SECTION 3: MAIN EXECUTION FUNCTION
# =============================================================================
def main():
    """
    Main execution function: Initialises the Boto3 Lambda client and attempts 
    to delete the specified AWS Lambda function.
    """
    print(f"🚀 Initializing AWS Lambda Client (Endpoint: {ENDPOINT_URL})...")
    
    # Instantiate the Lambda client with region, endpoint URL, and credentials
    lambda_client = boto3.client(
        "lambda",
        region_name=REGION_NAME,
        endpoint_url=ENDPOINT_URL,
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID", "test"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY", "test")
    )

    try:
        print(f"🗑️ Deleting Lambda function '{FUNCTION_NAME}'...")
        
        # Make the API call to AWS/LocalStack to delete the function
        response = lambda_client.delete_function(FunctionName=FUNCTION_NAME)

        print(f"✅ Function '{FUNCTION_NAME}' deleted successfully!")
        
        # Safely extract and print the HTTP status code (204 = No Content / Success)
        http_status = response.get('ResponseMetadata', {}).get('HTTPStatusCode')
        print(f"📊 Response Metadata (HTTP Status Code): {http_status}")

    except lambda_client.exceptions.ResourceNotFoundException:
        # Gracefully handle the error if the function does not exist
        print(f"⚠️ Function '{FUNCTION_NAME}' does not exist or was already deleted.")
        
    except Exception as e:
        # Catch any other unexpected errors (e.g., connection errors, permission errors)
        print(f"❌ Error deleting function: {e}")

# =============================================================================
# SECTION 4: SCRIPT ENTRY POINT
# =============================================================================
if __name__ == "__main__":
    main()