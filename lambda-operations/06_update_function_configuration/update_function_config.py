"""
===============================================================================
MODULE: AWS Lambda Function Configuration Updater
===============================================================================
Description:
    This script connects to AWS Lambda (or LocalStack mock environment) and 
    updates operational configuration settings (Timeout, Memory Allocation, 
    Description, Environment Variables) using the Boto3 SDK.

Dependencies:
    - boto3 (AWS SDK for Python)
    - json (Standard Library)
    - os (Standard Library)

Usage:
    python update_function_config.py
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

# Target Lambda Function Name
FUNCTION_NAME = "my-first-lambda"

# =============================================================================
# SECTION 3: MAIN EXECUTION FUNCTION
# =============================================================================
def main():
    """
    Main execution function: Initializes Boto3 Lambda client and updates 
    runtime configuration settings (timeout, memory, environment variables).
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

    try:
        print(f"⚙️ Updating configuration settings for function '{FUNCTION_NAME}'...")
        
        # Invoke UpdateFunctionConfiguration API call
        response = lambda_client.update_function_configuration(
            FunctionName=FUNCTION_NAME,
            Timeout=30,             # Increased execution timeout from 15 to 30 seconds
            MemorySize=256,         # Increased allocated RAM from 128 MB to 256 MB
            Description="Updated Lambda configuration with enhanced memory & env variables",
            Environment={
                "Variables": {
                    "ENVIRONMENT": "production",
                    "LOG_LEVEL": "DEBUG",
                    "DATABASE_NAME": "app_db_prod",
                    "MAX_CONNECTIONS": "100"
                }
            }
        )

        print("✅ Function Configuration Updated Successfully!")
        print("📊 New Configuration Summary:")
        print(json.dumps({
            "FunctionName": response.get("FunctionName"),
            "Timeout": response.get("Timeout"),
            "MemorySize": response.get("MemorySize"),
            "Description": response.get("Description"),
            "Environment": response.get("Environment"),
            "LastModified": response.get("LastModified")
        }, indent=2))

    except lambda_client.exceptions.ResourceNotFoundException:
        print(f"❌ Function '{FUNCTION_NAME}' does not exist.")
    except Exception as e:
        print(f"❌ Error updating function configuration: {e}")

# =============================================================================
# SECTION 4: SCRIPT ENTRY POINT
# =============================================================================
if __name__ == "__main__":
    main()
