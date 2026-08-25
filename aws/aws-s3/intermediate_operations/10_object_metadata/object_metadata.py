"""
AWS S3 Operation 10: Object Metadata

Demonstrates reading, setting, and updating S3 object metadata.
Includes system HTTP headers (ContentType, CacheControl) and user-defined custom metadata
(x-amz-meta-*) via head_object and copy_object (MetadataDirective='REPLACE').
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


def get_object_metadata(bucket_name: str, object_key: str, region: str = None) -> dict:
    """
    Retrieves system and custom metadata of an S3 object via head_object.

    :param bucket_name: S3 bucket name.
    :param object_key: S3 object key.
    :param region: AWS Region.
    :return: Dictionary containing metadata.
    """
    region = region or AWS_REGION
    s3_client = get_s3_client(region_name=region)

    print(f"\n[INFO] Fetching metadata for s3://{bucket_name}/{object_key}...")

    try:
        response = s3_client.head_object(Bucket=bucket_name, Key=object_key)
        
        system_metadata = {
            "ContentType": response.get("ContentType"),
            "ContentLength": response.get("ContentLength"),
            "ETag": response.get("ETag"),
            "LastModified": str(response.get("LastModified")),
            "ServerSideEncryption": response.get("ServerSideEncryption")
        }
        custom_metadata = response.get("Metadata", {})

        print("[SUCCESS] System Metadata:")
        for k, v in system_metadata.items():
            print(f"  - {k:<22}: {v}")

        print("[SUCCESS] Custom User Metadata (x-amz-meta-*):")
        if custom_metadata:
            for k, v in custom_metadata.items():
                print(f"  - x-amz-meta-{k:<15}: {v}")
        else:
            print("  (No custom user metadata attached)")

        return response

    except ClientError as e:
        print(f"[ERROR] Failed to fetch metadata: {e.response['Error']['Message']}")
        return {}


def update_object_metadata(bucket_name: str, object_key: str, custom_meta: dict, content_type: str = "text/plain", region: str = None) -> bool:
    """
    Updates custom metadata on an existing object using in-place copy_object with MetadataDirective='REPLACE'.

    :param bucket_name: S3 bucket name.
    :param object_key: S3 object key.
    :param custom_meta: Key-value dictionary of custom metadata.
    :param content_type: HTTP Content-Type header.
    :param region: AWS Region.
    :return: True if metadata updated, False otherwise.
    """
    region = region or AWS_REGION
    s3_client = get_s3_client(region_name=region)

    copy_source = {"Bucket": bucket_name, "Key": object_key}

    print(f"\n[INFO] Updating metadata on s3://{bucket_name}/{object_key}...")
    print(f"       New Custom Metadata: {custom_meta}")

    try:
        s3_client.copy_object(
            CopySource=copy_source,
            Bucket=bucket_name,
            Key=object_key,
            Metadata=custom_meta,
            MetadataDirective="REPLACE",
            ContentType=content_type
        )
        print("[SUCCESS] Metadata updated successfully!")
        return True

    except ClientError as e:
        print(f"[ERROR] Failed to update metadata: {e.response['Error']['Message']}")
        return False


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Read and update AWS S3 object metadata.")
    parser.add_argument("--bucket", type=str, default=S3_BUCKET_NAME, help="S3 bucket name")
    parser.add_argument("--key", type=str, default=S3_OBJECT_KEY, help="S3 object key")
    parser.add_argument("--region", type=str, default=AWS_REGION, help="AWS Region")

    args = parser.parse_args()

    # Step 1: Read existing metadata
    get_object_metadata(bucket_name=args.bucket, object_key=args.key, region=args.region)

    # Step 2: Update with custom metadata tags
    new_metadata = {
        "author": "dev-team",
        "environment": "learning",
        "project": "aws-operations"
    }
    update_object_metadata(bucket_name=args.bucket, object_key=args.key, custom_meta=new_metadata, region=args.region)

    # Step 3: Verify updated metadata
    get_object_metadata(bucket_name=args.bucket, object_key=args.key, region=args.region)
