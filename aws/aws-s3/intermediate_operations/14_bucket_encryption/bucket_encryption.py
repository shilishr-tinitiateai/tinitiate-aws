"""
AWS S3 Operation 14: Bucket Encryption

Demonstrates inspecting and applying default Server-Side Encryption (SSE) configuration
on S3 buckets using get_bucket_encryption and put_bucket_encryption (SSE-S3 AES256 or SSE-KMS).
"""

import sys
import argparse
from pathlib import Path
import boto3
from botocore.exceptions import ClientError, NoCredentialsError

# Add parent directory to sys.path
sys.path.append(str(Path(__file__).resolve().parent.parent.parent.parent))

from shared.config import AWS_REGION, S3_BUCKET_NAME
from shared.aws_client import get_s3_client


def get_bucket_encryption(bucket_name: str, region: str = None) -> dict:
    """
    Retrieves default server-side encryption settings for an S3 bucket.

    :param bucket_name: S3 bucket name.
    :param region: AWS Region.
    :return: Encryption configuration dictionary.
    """
    region = region or AWS_REGION
    s3_client = get_s3_client(region_name=region)

    print(f"[INFO] Fetching default encryption settings for s3://{bucket_name}...")

    try:
        response = s3_client.get_bucket_encryption(Bucket=bucket_name)
        rules = response.get("ServerSideEncryptionConfiguration", {}).get("Rules", [])
        
        print(f"[SUCCESS] Found {len(rules)} Encryption Rule(s):")
        for rule in rules:
            default_enc = rule.get("ApplyServerSideEncryptionByDefault", {})
            algorithm = default_enc.get("SSEAlgorithm")
            kms_key = default_enc.get("KMSMasterKeyID", "N/A (Managed S3 Key)")
            print(f"  - SSE Algorithm: {algorithm:<10} | KMS Key ID: {kms_key}")

        return response

    except ClientError as e:
        error_code = e.response["Error"]["Code"]
        if error_code == "ServerSideEncryptionConfigurationNotFoundError":
            print("[INFO] No explicit encryption configuration returned (defaults to SSE-S3 AES256).")
        else:
            print(f"[ERROR] Failed to get encryption config: {e.response['Error']['Message']}")
        return {}


def set_bucket_encryption(bucket_name: str, algorithm: str = "AES256", kms_key_id: str = None, region: str = None) -> bool:
    """
    Applies default server-side encryption (SSE-S3 AES256 or SSE-KMS) to an S3 bucket.

    :param bucket_name: S3 bucket name.
    :param algorithm: Encryption algorithm ('AES256' or 'aws:kms').
    :param kms_key_id: Optional KMS Master Key ARN or Alias (used if algorithm is 'aws:kms').
    :param region: AWS Region.
    :return: True if successful, False otherwise.
    """
    region = region or AWS_REGION
    s3_client = get_s3_client(region_name=region)

    sse_config = {
        "ApplyServerSideEncryptionByDefault": {
            "SSEAlgorithm": algorithm
        }
    }
    if algorithm == "aws:kms" and kms_key_id:
        sse_config["ApplyServerSideEncryptionByDefault"]["KMSMasterKeyID"] = kms_key_id

    print(f"[INFO] Setting default encryption on s3://{bucket_name} -> SSE Algorithm: '{algorithm}'...")

    try:
        s3_client.put_bucket_encryption(
            Bucket=bucket_name,
            ServerSideEncryptionConfiguration={"Rules": [sse_config]}
        )
        print(f"[SUCCESS] Default encryption applied successfully!")
        return True

    except ClientError as e:
        print(f"[ERROR] ClientError configuring encryption: {e.response['Error']['Message']}")
        return False
    except NoCredentialsError:
        print("[ERROR] AWS credentials not found.")
        return False


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Manage AWS S3 Default Bucket Encryption.")
    parser.add_argument("--bucket", type=str, default=S3_BUCKET_NAME, help="S3 bucket name")
    parser.add_argument("--algo", type=str, choices=["AES256", "aws:kms"], default="AES256", help="Encryption algorithm")
    parser.add_argument("--kms-key", type=str, default=None, help="KMS Key ID (required if algo is aws:kms)")
    parser.add_argument("--region", type=str, default=AWS_REGION, help="AWS Region")

    args = parser.parse_args()

    # Read current encryption settings
    get_bucket_encryption(bucket_name=args.bucket, region=args.region)

    # Set encryption configuration
    set_bucket_encryption(bucket_name=args.bucket, algorithm=args.algo, kms_key_id=args.kms_key, region=args.region)

    # Verify updated configuration
    get_bucket_encryption(bucket_name=args.bucket, region=args.region)
