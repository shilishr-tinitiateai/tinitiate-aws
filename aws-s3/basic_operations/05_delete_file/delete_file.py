"""
===============================================================================
MODULE: AWS S3 & LocalStack File Deleter
===============================================================================
Description:
    This script deletes a specific file object key from an AWS S3 bucket.
    Supports both local emulators (Floci/LocalStack) and real AWS S3 cloud.

Dependencies:
    - boto3 (AWS SDK for Python)
    - botocore (Low-level core module for boto3 exceptions)
    - python-dotenv (Loads environment variables from .env file)

Usage:
    python delete_file.py
===============================================================================
"""

# =============================================================================
# SECTION 1: IMPORTS
# =============================================================================
import os
import boto3
from botocore.exceptions import ClientError
from dotenv import load_dotenv

# =============================================================================
# SECTION 2: ENVIRONMENT CONFIGURATION
# =============================================================================
# Load environment variables from a local `.env` file into `os.environ`
load_dotenv()

# Determine whether to target LocalStack (local emulator) or Real AWS S3
USE_LOCALSTACK = os.getenv("USE_LOCALSTACK", "true").lower() == "true"

# Define local endpoint URL if using LocalStack; set to None for Real AWS
ENDPOINT_URL = (
    os.getenv("LOCALSTACK_ENDPOINT", "http://localhost:4566")
    if USE_LOCALSTACK
    else None
)

# =============================================================================
# SECTION 3: BOTO3 S3 CLIENT INITIALIZATION
# =============================================================================
# Instantiate the S3 client with dynamic credentials and endpoint configuration
s3_client = boto3.client(
    "s3",
    region_name=os.getenv("AWS_REGION", "us-east-1"),
    endpoint_url=ENDPOINT_URL,
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID", "test"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY", "test"),
)

# =============================================================================
# SECTION 4: S3 OPERATIONS & FUNCTIONS
# =============================================================================
def delete_file(bucket_name, s3_key):
    """
    Deletes a specific object key from an S3 bucket.

    Parameters:
        bucket_name (str): The target S3 bucket name.
        s3_key (str): The target Object Key path inside S3 to delete.

    Returns:
        bool: True if deletion succeeded, False if ClientError occurred.
    """
    try:
        # Call the S3 API to delete the object
        s3_client.delete_object(Bucket=bucket_name, Key=s3_key)
        print(f"✅ Deleted object '{s3_key}' from bucket '{bucket_name}' successfully!")
        return True
    except ClientError as e:
        # Catch S3 API errors (e.g., AccessDenied, NoSuchBucket)
        print(f"❌ Error deleting object '{s3_key}': {e}")
        return False

# =============================================================================
# SECTION 5: MAIN EXECUTION ENTRY POINT
# =============================================================================
if __name__ == "__main__":
    # Fetch configuration variables from environment or defaults
    bucket_name = os.getenv("S3_BUCKET_NAME", "my-local-bucket")
    s3_key = "documents/sample.txt"

    print(f"🚀 Executing Script: Delete File '{s3_key}' from '{bucket_name}'...")
    
    # Execute file deletion
    delete_file(bucket_name, s3_key)
