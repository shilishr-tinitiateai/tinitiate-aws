"""
AWS S3 Operation 05: Delete File

Demonstrates deleting an object from an S3 bucket using delete_object,
including object existence checking via head_object and safety prompts.
"""

import sys
import argparse
from pathlib import Path
import boto3
from botocore.exceptions import ClientError, NoCredentialsError

# Add parent directory to sys.path
sys.path.append(str(Path(__file__).resolve().parent.parent.parent.parent))

from shared.config import AWS_REGION, S3_BUCKET_NAME, S3_OBJECT_KEY
from shared.aws_client import get_s3_client


def delete_file(bucket_name: str, object_key: str, force: bool = False, region: str = None) -> bool:
    """
    Deletes an object from an S3 bucket.

    :param bucket_name: S3 bucket name.
    :param object_key: Object key to delete.
    :param force: Skip confirmation prompt if True.
    :param region: AWS Region.
    :return: True if deleted or non-existent, False on error.
    """
    region = region or AWS_REGION
    s3_client = get_s3_client(region_name=region)

    # Verify object existence before attempting deletion
    try:
        s3_client.head_object(Bucket=bucket_name, Key=object_key)
    except ClientError as e:
        error_code = e.response["Error"]["Code"]
        if error_code in ("404", "NoSuchKey"):
            print(f"[INFO] Object 's3://{bucket_name}/{object_key}' does not exist. Nothing to delete.")
            return True
        elif error_code == "AccessDenied":
            print(f"[ERROR] Access denied checking object existence for s3://{bucket_name}/{object_key}.")
            return False
        else:
            print(f"[ERROR] ClientError verifying object [{error_code}]: {e.response['Error']['Message']}")
            return False

    if not force:
        print(f"[WARNING] You are about to permanently delete 's3://{bucket_name}/{object_key}'.")
        confirm = input("Type 'YES' to confirm deletion: ").strip()
        if confirm != "YES":
            print("[INFO] Deletion cancelled by user.")
            return False

    print(f"[INFO] Deleting 's3://{bucket_name}/{object_key}'...")

    try:
        response = s3_client.delete_object(Bucket=bucket_name, Key=object_key)
        print(f"[SUCCESS] Object deleted successfully!")
        print(f"         Bucket: {bucket_name}")
        print(f"         Key:    {object_key}")
        if response.get("VersionId"):
            print(f"         Delete Marker VersionId: {response['VersionId']}")
        return True

    except ClientError as e:
        print(f"[ERROR] Failed to delete object: {e.response['Error']['Message']}")
        return False
    except NoCredentialsError:
        print("[ERROR] AWS credentials not found.")
        return False


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Delete an object from AWS S3.")
    parser.add_argument("--bucket", type=str, default=S3_BUCKET_NAME, help="S3 bucket name")
    parser.add_argument("--key", type=str, default=S3_OBJECT_KEY, help="S3 object key to delete")
    parser.add_argument("--force", action="store_true", help="Bypass deletion prompt")
    parser.add_argument("--region", type=str, default=AWS_REGION, help="AWS Region")

    args = parser.parse_args()

    success = delete_file(bucket_name=args.bucket, object_key=args.key, force=args.force, region=args.region)
    sys.exit(0 if success else 1)
