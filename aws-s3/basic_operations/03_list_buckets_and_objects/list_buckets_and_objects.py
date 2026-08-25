"""
===============================================================================
MODULE: AWS S3 & LocalStack Buckets & Objects Lister
===============================================================================
Description:
    This script lists all top-level S3 buckets in the account/emulator 
    and inspects objects stored inside a specified target bucket.

Dependencies:
    - boto3 (AWS SDK for Python)
    - botocore (Low-level core module for boto3 exceptions)
    - python-dotenv (Loads environment variables from .env file)

Usage:
    python list_buckets_and_objects.py
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
def list_buckets_and_objects(bucket_name):
    """
    Queries S3 to list all buckets and objects inside the specified bucket.

    Parameters:
        bucket_name (str): The target S3 bucket name to inspect.

    Returns:
        tuple: (list of buckets, list of objects) if successful.
        None: If a ClientError exception occurs.
    """
    try:
        # 1. Query S3 for all top-level buckets
        response_buckets = s3_client.list_buckets()
        buckets = response_buckets.get("Buckets", [])
        print(f"🪣 Total Buckets Found: {len(buckets)}")
        for b in buckets:
            print(f"  - {b['Name']}")

        # 2. Query S3 for objects inside the target bucket
        response_objects = s3_client.list_objects_v2(Bucket=bucket_name)
        contents = response_objects.get("Contents", [])
        print(f"\n📄 Objects inside '{bucket_name}': {len(contents)} item(s)")
        for obj in contents:
            print(f"  - Key: {obj['Key']} | Size: {obj['Size']} bytes")
        
        return buckets, contents
    except ClientError as e:
        # Catch S3 API errors (e.g., NoSuchBucket, AccessDenied)
        print(f"❌ Error listing buckets or objects: {e}")
        return None

# =============================================================================
# SECTION 5: MAIN EXECUTION ENTRY POINT
# =============================================================================
if __name__ == "__main__":
    # Fetch target bucket name from environment or fallback to default
    bucket_name = os.getenv("S3_BUCKET_NAME", "my-local-bucket")

    print("🚀 Executing Script: List Buckets & Objects...")
    
    # Execute listing operation
    list_buckets_and_objects(bucket_name)
