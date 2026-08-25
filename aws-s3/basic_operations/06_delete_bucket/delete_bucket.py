"""
===============================================================================
MODULE: AWS S3 & LocalStack Bucket Deleter
===============================================================================
Description:
    This script deletes an empty AWS S3 bucket.
    Supports both local emulators (Floci/LocalStack) and real AWS S3 cloud.

Dependencies:
    - boto3 (AWS SDK for Python)
    - botocore (Low-level core module for boto3 exceptions)
    - python-dotenv (Loads environment variables from .env file)

Usage:
    python delete_bucket.py
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
def delete_bucket(bucket_name):
    """
    Deletes an empty S3 bucket.

    Parameters:
        bucket_name (str): The name of the empty S3 bucket to delete.

    Returns:
        bool: True if deletion succeeded, False if ClientError occurred.
    """
    try:
        # Call the S3 API to delete the empty bucket
        s3_client.delete_bucket(Bucket=bucket_name)
        print(f"✅ Bucket '{bucket_name}' deleted successfully!")
        return True
    except ClientError as e:
        # Catch S3 API errors (e.g., BucketNotEmpty, NoSuchBucket)
        print(f"❌ Error deleting bucket '{bucket_name}': {e}")
        return False

# =============================================================================
# SECTION 5: MAIN EXECUTION ENTRY POINT
# =============================================================================
if __name__ == "__main__":
    # Fetch configuration variables from environment or defaults
    bucket_name = os.getenv("S3_BUCKET_NAME", "my-local-bucket")

    print(f"🚀 Executing Script: Delete Bucket '{bucket_name}'...")
    
    # Execute bucket deletion
    delete_bucket(bucket_name)
