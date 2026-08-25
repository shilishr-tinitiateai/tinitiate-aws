"""
AWS S3 Operation 18: Lifecycle Configuration

Demonstrates creating, applying, and inspecting S3 Bucket Lifecycle Rules
(transitions to Glacier, object expiration, and incomplete multipart upload cleanup)
using put_bucket_lifecycle_configuration and get_bucket_lifecycle_configuration.
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


def get_lifecycle_config(bucket_name: str, region: str = None) -> list:
    """
    Retrieves active lifecycle rules for an S3 bucket.

    :param bucket_name: S3 bucket name.
    :param region: AWS Region.
    :return: List of rule dictionaries.
    """
    region = region or AWS_REGION
    s3_client = get_s3_client(region_name=region)

    print(f"\n[INFO] Fetching Lifecycle configuration for s3://{bucket_name}...")

    try:
        response = s3_client.get_bucket_lifecycle_configuration(Bucket=bucket_name)
        rules = response.get("Rules", [])
        print(f"[SUCCESS] Found {len(rules)} Lifecycle Rule(s):")
        for r in rules:
            rule_id = r.get("ID")
            status = r.get("Status")
            prefix = r.get("Filter", {}).get("Prefix", r.get("Prefix", "All"))
            print(f"  - Rule ID: {rule_id:<25} | Status: {status:<8} | Filter Prefix: '{prefix}'")
        return rules

    except ClientError as e:
        error_code = e.response["Error"]["Code"]
        if error_code == "NoSuchLifecycleConfiguration":
            print("[INFO] No lifecycle configuration currently exists for this bucket.")
        else:
            print(f"[ERROR] ClientError fetching lifecycle config: {e.response['Error']['Message']}")
        return []


def set_lifecycle_config(bucket_name: str, region: str = None) -> bool:
    """
    Applies a standard production lifecycle configuration to an S3 bucket:
    1. Transition 'logs/' objects to GLACIER after 30 days.
    2. Expire 'logs/' objects after 365 days.
    3. Abort incomplete multipart uploads after 7 days across entire bucket.

    :param bucket_name: S3 bucket name.
    :param region: AWS Region.
    :return: True if successful, False otherwise.
    """
    region = region or AWS_REGION
    s3_client = get_s3_client(region_name=region)

    lifecycle_policy = {
        "Rules": [
            {
                "ID": "LogArchivalAndExpirationPolicy",
                "Status": "Enabled",
                "Filter": {"Prefix": "logs/"},
                "Transitions": [
                    {
                        "Days": 30,
                        "StorageClass": "GLACIER"
                    }
                ],
                "Expiration": {
                    "Days": 365
                }
            },
            {
                "ID": "AbortIncompleteMultipartUploadsPolicy",
                "Status": "Enabled",
                "Filter": {"Prefix": ""},
                "AbortIncompleteMultipartUpload": {
                    "DaysAfterInitiation": 7
                }
            }
        ]
    }

    print(f"\n[INFO] Applying Lifecycle configuration to s3://{bucket_name}...")

    try:
        s3_client.put_bucket_lifecycle_configuration(
            Bucket=bucket_name,
            LifecycleConfiguration=lifecycle_policy
        )
        print(f"[SUCCESS] Lifecycle rules applied successfully!")
        return True

    except ClientError as e:
        print(f"[ERROR] ClientError applying lifecycle rules: {e.response['Error']['Message']}")
        return False
    except NoCredentialsError:
        print("[ERROR] AWS credentials not found.")
        return False


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Manage AWS S3 Bucket Lifecycle Configurations.")
    parser.add_argument("--bucket", type=str, default=S3_BUCKET_NAME, help="S3 bucket name")
    parser.add_argument("--region", type=str, default=AWS_REGION, help="AWS Region")

    args = parser.parse_args()

    # Step 1: Read existing rules
    get_lifecycle_config(bucket_name=args.bucket, region=args.region)

    # Step 2: Apply production policy
    set_lifecycle_config(bucket_name=args.bucket, region=args.region)

    # Step 3: Verify rules applied
    get_lifecycle_config(bucket_name=args.bucket, region=args.region)
