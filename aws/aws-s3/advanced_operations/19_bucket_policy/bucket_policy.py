"""
AWS S3 Operation 19: Bucket Policy

Demonstrates reading, generating, applying, and deleting JSON S3 Bucket Policies
using get_bucket_policy, put_bucket_policy, and delete_bucket_policy (e.g. enforcing TLS/HTTPS access).
"""

import sys
import json
import argparse
from pathlib import Path
import boto3
from botocore.exceptions import ClientError, NoCredentialsError

# Add parent directory to sys.path
sys.path.append(str(Path(__file__).resolve().parent.parent.parent.parent))

from shared.config import AWS_REGION, S3_BUCKET_NAME
from shared.aws_client import get_s3_client


def get_bucket_policy(bucket_name: str, region: str = None) -> dict:
    """
    Retrieves the JSON Bucket Policy applied to an S3 bucket.

    :param bucket_name: S3 bucket name.
    :param region: AWS Region.
    :return: Parsed JSON policy dictionary.
    """
    region = region or AWS_REGION
    s3_client = get_s3_client(region_name=region)

    print(f"\n[INFO] Reading Bucket Policy for s3://{bucket_name}...")

    try:
        response = s3_client.get_bucket_policy(Bucket=bucket_name)
        policy_str = response.get("Policy", "{}")
        policy_json = json.loads(policy_str)
        print("[SUCCESS] Active Bucket Policy:")
        print(json.dumps(policy_json, indent=2))
        return policy_json

    except ClientError as e:
        error_code = e.response["Error"]["Code"]
        if error_code == "NoSuchBucketPolicy":
            print("[INFO] No custom Bucket Policy currently applied to this bucket.")
        else:
            print(f"[ERROR] ClientError reading policy [{error_code}]: {e.response['Error']['Message']}")
        return {}


def set_enforce_https_policy(bucket_name: str, region: str = None) -> bool:
    """
    Applies a security best-practice Bucket Policy enforcing TLS/HTTPS encrypted transport
    by explicitly denying any request where aws:SecureTransport is false.

    :param bucket_name: S3 bucket name.
    :param region: AWS Region.
    :return: True if successful, False otherwise.
    """
    region = region or AWS_REGION
    s3_client = get_s3_client(region_name=region)

    policy_document = {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Sid": "EnforceHTTPSTransportOnly",
                "Effect": "Deny",
                "Principal": "*",
                "Action": "s3:*",
                "Resource": [
                    f"arn:aws:s3:::{bucket_name}",
                    f"arn:aws:s3:::{bucket_name}/*"
                ],
                "Condition": {
                    "Bool": {
                        "aws:SecureTransport": "false"
                    }
                }
            }
        ]
    }

    policy_json_str = json.dumps(policy_document)
    print(f"\n[INFO] Applying Enforce-HTTPS Bucket Policy to s3://{bucket_name}...")

    try:
        s3_client.put_bucket_policy(
            Bucket=bucket_name,
            Policy=policy_json_str
        )
        print("[SUCCESS] Bucket Policy applied successfully!")
        return True

    except ClientError as e:
        print(f"[ERROR] ClientError applying Bucket Policy: {e.response['Error']['Message']}")
        return False
    except NoCredentialsError:
        print("[ERROR] AWS credentials not found.")
        return False


def delete_bucket_policy(bucket_name: str, region: str = None) -> bool:
    """
    Removes the Bucket Policy from an S3 bucket.

    :param bucket_name: S3 bucket name.
    :param region: AWS Region.
    :return: True if deleted successfully, False otherwise.
    """
    region = region or AWS_REGION
    s3_client = get_s3_client(region_name=region)

    print(f"\n[INFO] Removing Bucket Policy from s3://{bucket_name}...")

    try:
        s3_client.delete_bucket_policy(Bucket=bucket_name)
        print("[SUCCESS] Bucket Policy deleted successfully!")
        return True
    except ClientError as e:
        print(f"[ERROR] Failed to delete Bucket Policy: {e.response['Error']['Message']}")
        return False


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Manage AWS S3 Bucket Policies.")
    parser.add_argument("--bucket", type=str, default=S3_BUCKET_NAME, help="S3 bucket name")
    parser.add_argument("--delete", action="store_true", help="Remove active bucket policy")
    parser.add_argument("--region", type=str, default=AWS_REGION, help="AWS Region")

    args = parser.parse_args()

    if args.delete:
        delete_bucket_policy(bucket_name=args.bucket, region=args.region)
    else:
        # Step 1: Read policy
        get_bucket_policy(bucket_name=args.bucket, region=args.region)

        # Step 2: Apply HTTPS enforcement policy
        set_enforce_https_policy(bucket_name=args.bucket, region=args.region)

        # Step 3: Verify applied policy
        get_bucket_policy(bucket_name=args.bucket, region=args.region)
