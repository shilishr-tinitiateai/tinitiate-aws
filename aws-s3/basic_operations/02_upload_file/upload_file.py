"""
===============================================================================
MODULE: AWS S3 & LocalStack File Uploader
===============================================================================
Description:
    This script uploads a local file to an AWS S3 bucket. It automatically 
    creates a sample file if one does not exist locally and supports both 
    local emulators (Floci/LocalStack) and real AWS S3 cloud environments.

Dependencies:
    - boto3 (AWS SDK for Python)
    - botocore (Low-level core module for boto3 exceptions)
    - python-dotenv (Loads environment variables from .env file)

Usage:
    python upload_file.py
===============================================================================
"""

# =============================================================================
# SECTION 1: IMPORTS
# =============================================================================
import os
import boto3
from botocore.exceptions import ClientError, BotoCoreError
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
def upload_file(local_file_path, bucket_name, s3_key):
    """
    Uploads a local file to an S3 bucket using boto3.

    Parameters:
        local_file_path (str): Path to the source file on local disk.
        bucket_name (str): The target S3 bucket name.
        s3_key (str): The target Object Key path inside the S3 bucket.

    Returns:
        bool: True if upload succeeded, False if an error occurred.
    """
    try:
        # Check if local file exists; if not, generate a sample text file
        if not os.path.exists(local_file_path):
            with open(local_file_path, "w") as f:
                f.write("Sample file content for AWS S3 upload test.\n")
            print(f"📄 Generated sample local file: '{local_file_path}'")

        # Call the S3 API to upload the file
        s3_client.upload_file(local_file_path, bucket_name, s3_key)
        print(f"✅ Uploaded '{local_file_path}' to s3://{bucket_name}/{s3_key}")
        return True
    except ClientError as e:
        # Catch S3 API errors (e.g., NoSuchBucket, AccessDenied)
        print(f"❌ AWS S3 API Error uploading file '{local_file_path}': {e}")
        return False
    except BotoCoreError as e:
        # Catch network/connection errors (e.g. Floci Docker container not running)
        print(f"\n❌ Connection Error: Could not connect to S3 endpoint at '{ENDPOINT_URL}'.")
        print("💡 Solution: Make sure Floci/LocalStack is running in Docker using:")
        print("   docker run -d --name floci -p 4566:4566 floci/floci:latest\n")
        return False

# =============================================================================
# SECTION 5: MAIN EXECUTION ENTRY POINT
# =============================================================================
if __name__ == "__main__":
    # Fetch configuration variables from environment or defaults
    bucket_name = os.getenv("S3_BUCKET_NAME", "my-local-bucket")
    local_file = "sample.txt"
    s3_key = "documents/sample.txt"

    print(f"🚀 Executing Script: Upload File '{local_file}' to '{bucket_name}'...")
    
    # Execute file upload
    upload_file(local_file, bucket_name, s3_key)
