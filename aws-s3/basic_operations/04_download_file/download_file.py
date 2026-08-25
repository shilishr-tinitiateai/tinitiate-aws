"""
===============================================================================
MODULE: AWS S3 & LocalStack File Downloader
===============================================================================
Description:
    This script downloads an object file from an S3 bucket onto the local disk.
    Supports both local emulators (Floci/LocalStack) and real AWS S3 cloud.

Dependencies:
    - boto3 (AWS SDK for Python)
    - botocore (Low-level core module for boto3 exceptions)
    - python-dotenv (Loads environment variables from .env file)

Usage:
    python download_file.py
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
def download_file(bucket_name, s3_key, local_download_path):
    """
    Downloads an object from S3 and saves it to a local disk path.

    Parameters:
        bucket_name (str): The target S3 bucket name.
        s3_key (str): The source Object Key path inside S3.
        local_download_path (str): The target file path on local disk.

    Returns:
        bool: True if download succeeded, False if ClientError occurred.
    """
    try:
        # Call the S3 API to download the object
        s3_client.download_file(bucket_name, s3_key, local_download_path)
        print(f"✅ Downloaded s3://{bucket_name}/{s3_key} to '{local_download_path}' successfully!")
        return True
    except ClientError as e:
        # Catch S3 API errors (e.g., NoSuchKey, NoSuchBucket)
        print(f"❌ Error downloading file '{s3_key}': {e}")
        return False

# =============================================================================
# SECTION 5: MAIN EXECUTION ENTRY POINT
# =============================================================================
if __name__ == "__main__":
    # Fetch configuration variables from environment or defaults
    bucket_name = os.getenv("S3_BUCKET_NAME", "my-local-bucket")
    s3_key = "documents/sample.txt"
    download_destination = "downloaded_sample.txt"

    print(f"🚀 Executing Script: Download File '{s3_key}' from '{bucket_name}'...")
    
    # Execute file download
    download_file(bucket_name, s3_key, download_destination)
