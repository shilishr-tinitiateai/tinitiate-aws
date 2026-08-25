"""
AWS S3 Operation 06: Delete Bucket

Demonstrates deleting an S3 bucket programmatically using delete_bucket.
Includes emptying all objects and object versions prior to bucket deletion,
as required by the AWS S3 API.
"""

import sys
import argparse
from pathlib import Path
import boto3
from botocore.exceptions import ClientError, NoCredentialsError

# Add parent directory to sys.path
sys.path.append(str(Path(__file__).resolve().parent.parent.parent.parent))

from shared.config import AWS_REGION, S3_BUCKET_NAME
from shared.aws_client import get_s3_client, get_s3_resource


def empty_bucket(bucket_name: str, region: str = None) -> bool:
    """
    Deletes all objects and version markers from an S3 bucket.

    :param bucket_name: S3 bucket name.
    :param region: AWS Region.
    :return: True if bucket is empty, False otherwise.
    """
    region = region or AWS_REGION
    s3_resource = get_s3_resource(region_name=region)
    bucket = s3_resource.Bucket(bucket_name)

    print(f"[INFO] Emptying all objects and versions from s3://{bucket_name}...")

    try:
        # Delete all object versions (handles both versioned & unversioned buckets)
        bucket.object_versions.delete()
        print(f"[SUCCESS] All objects and version markers removed from '{bucket_name}'.")
        return True
    except ClientError as e:
        error_code = e.response["Error"]["Code"]
        if error_code == "NoSuchBucket":
            print(f"[INFO] Bucket '{bucket_name}' does not exist.")
            return True
        elif error_code == "AccessDenied":
            print(f"[ERROR] Access denied when attempting to empty bucket '{bucket_name}'.")
            return False
        else:
            print(f"[ERROR] Failed to empty bucket [{error_code}]: {e.response['Error']['Message']}")
            return False


def delete_bucket(bucket_name: str, force: bool = False, region: str = None) -> bool:
    """
    Empties and deletes an S3 bucket.

    :param bucket_name: S3 bucket name.
    :param force: Skip interactive user prompt if True.
    :param region: AWS Region.
    :return: True if deleted successfully, False otherwise.
    """
    region = region or AWS_REGION
    s3_client = get_s3_client(region_name=region)

    if not force:
        print(f"[WARNING] HIGH-RISK OPERATION: You are about to permanently delete bucket '{bucket_name}' and ALL ITS CONTENTS!")
        confirm = input("Type 'DELETE-BUCKET' to confirm: ").strip()
        if confirm != "DELETE-BUCKET":
            print("[INFO] Bucket deletion cancelled by user.")
            return False

    # Step 1: Empty bucket
    if not empty_bucket(bucket_name=bucket_name, region=region):
        print(f"[ERROR] Cannot delete bucket '{bucket_name}' because emptying it failed.")
        return False

    # Step 2: Delete bucket container
    print(f"[INFO] Deleting empty bucket container '{bucket_name}'...")
    try:
        s3_client.delete_bucket(Bucket=bucket_name)
        print(f"[SUCCESS] Bucket '{bucket_name}' has been deleted successfully!")
        return True

    except ClientError as e:
        error_code = e.response["Error"]["Code"]
        if error_code == "BucketNotEmpty":
            print(f"[ERROR] Bucket '{bucket_name}' is not empty. Cannot delete.")
        elif error_code == "NoSuchBucket":
            print(f"[INFO] Bucket '{bucket_name}' does not exist.")
            return True
        elif error_code == "AccessDenied":
            print(f"[ERROR] Access denied. Lacking 's3:DeleteBucket' permission.")
        else:
            print(f"[ERROR] ClientError deleting bucket [{error_code}]: {e.response['Error']['Message']}")
        return False
    except NoCredentialsError:
        print("[ERROR] AWS credentials not found.")
        return False


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Delete an AWS S3 Bucket.")
    parser.add_argument("--bucket", type=str, default=S3_BUCKET_NAME, help="S3 bucket name to delete")
    parser.add_argument("--force", action="store_true", help="Bypass interactive confirmation prompt")
    parser.add_argument("--region", type=str, default=AWS_REGION, help="AWS Region")

    args = parser.parse_args()

    success = delete_bucket(bucket_name=args.bucket, force=args.force, region=args.region)
    sys.exit(0 if success else 1)
