"""
AWS S3 Operation 03: List Buckets and Objects

Demonstrates listing owned S3 buckets and listing objects within a specific bucket
using list_buckets() and list_objects_v2() API calls.
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


def list_buckets(region: str = None) -> list:
    """
    Lists all S3 buckets in the AWS account.

    :param region: AWS Region.
    :return: List of bucket names.
    """
    s3_client = get_s3_client(region_name=region)
    print("\n[INFO] Fetching account S3 buckets...")

    try:
        response = s3_client.list_buckets()
        buckets = response.get("Buckets", [])
        
        print(f"[SUCCESS] Found {len(buckets)} bucket(s):")
        for bucket in buckets:
            creation_date = bucket["CreationDate"].strftime("%Y-%m-%d %H:%M:%S UTC")
            print(f"  - {bucket['Name']} (Created: {creation_date})")
        return [b["Name"] for b in buckets]

    except ClientError as e:
        print(f"[ERROR] Failed to list buckets: {e.response['Error']['Message']}")
        return []


def list_objects(bucket_name: str, prefix: str = "", region: str = None) -> list:
    """
    Lists objects inside a specific S3 bucket using list_objects_v2.

    :param bucket_name: S3 bucket name.
    :param prefix: Optional key prefix filter.
    :param region: AWS Region.
    :return: List of object dictionaries.
    """
    s3_client = get_s3_client(region_name=region)
    print(f"\n[INFO] Listing objects in s3://{bucket_name} (Prefix: '{prefix}')...")

    try:
        kwargs = {"Bucket": bucket_name}
        if prefix:
            kwargs["Prefix"] = prefix

        response = s3_client.list_objects_v2(**kwargs)
        contents = response.get("Contents", [])

        if not contents:
            print(f"[INFO] Bucket s3://{bucket_name} is empty or no objects match prefix '{prefix}'.")
            return []

        print(f"[SUCCESS] Found {len(contents)} object(s):")
        total_size = 0
        for obj in contents:
            key = obj["Key"]
            size = obj["Size"]
            last_modified = obj["LastModified"].strftime("%Y-%m-%d %H:%M:%S UTC")
            total_size += size
            print(f"  - {key:<35} | Size: {size:>8} bytes | Modified: {last_modified}")
        
        print(f"Total objects size: {total_size} bytes")
        return contents

    except ClientError as e:
        error_code = e.response["Error"]["Code"]
        if error_code == "NoSuchBucket":
            print(f"[ERROR] Bucket '{bucket_name}' does not exist.")
        elif error_code == "AccessDenied":
            print(f"[ERROR] Access denied for bucket '{bucket_name}'.")
        else:
            print(f"[ERROR] ClientError listing objects: {e.response['Error']['Message']}")
        return []


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="List S3 buckets and objects.")
    parser.add_argument("--bucket", type=str, default=S3_BUCKET_NAME, help="Target S3 bucket name")
    parser.add_argument("--prefix", type=str, default="", help="Prefix filter for object listing")
    parser.add_argument("--region", type=str, default=AWS_REGION, help="AWS Region")

    args = parser.parse_args()

    list_buckets(region=args.region)
    list_objects(bucket_name=args.bucket, prefix=args.prefix, region=args.region)
