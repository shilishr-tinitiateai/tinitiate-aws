"""
===============================================================================
MODULE: AWS S3 & LocalStack Bucket Creator
===============================================================================
Description:
    This script creates an AWS S3 bucket. It dynamically switches between 
    a local mock environment (LocalStack/Floci) and real AWS S3 cloud based on 
    environment configuration settings (.env file).

Dependencies:
    - boto3 (AWS SDK for Python)
    - botocore (Low-level core module for boto3 exceptions)
    - python-dotenv (Loads environment variables from .env file)

Usage:
    python create_bucket.py
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
def create_bucket(bucket_name):
    """
    Creates a new S3 bucket using the configured boto3 S3 client.

    Parameters:
        bucket_name (str): The unique name of the S3 bucket to create.

    Returns:
        dict: The raw response metadata from AWS/LocalStack if successful.
        None: If a ClientError or Connection error occurs.
    """
    try:
        # Call the S3 API to create the bucket
        response = s3_client.create_bucket(Bucket=bucket_name)
        print(f"✅ Bucket '{bucket_name}' created successfully!")
        return response
    except ClientError as e:
        # Catch S3 API errors (e.g., BucketAlreadyExists, InvalidBucketName)
        print(f"❌ AWS S3 API Error creating bucket '{bucket_name}': {e}")
        return None
    except BotoCoreError as e:
        # Catch network/connection errors (e.g. Floci Docker container not running on port 4566)
        print(f"\n❌ Connection Error: Could not connect to S3 endpoint at '{ENDPOINT_URL}'.")
        print("💡 Solution: Make sure Floci/LocalStack is running in Docker using:")
        print("   docker run -d --name floci -p 4566:4566 floci/floci:latest\n")
        return None
    except Exception as e:
        print(f"❌ Unexpected Error: {e}")
        return None

# =============================================================================
# SECTION 5: MAIN EXECUTION ENTRY POINT
# =============================================================================
if __name__ == "__main__":
    # Fetch target bucket name from environment or fallback to default
    bucket_name = os.getenv("S3_BUCKET_NAME", "my-local-bucket")
    
    print(f"🚀 Executing Script: Create Bucket ({bucket_name})")
    
    # Execute bucket creation
    create_bucket(bucket_name)
