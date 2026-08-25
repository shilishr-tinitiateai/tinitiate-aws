"""
AWS S3 Operation 16: Pagination

Demonstrates handling large S3 object listings across multiple pages using boto3 Paginator
for list_objects_v2, abstracting ContinuationToken handling.
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


def list_objects_with_pagination(bucket_name: str, page_size: int = 2, prefix: str = "", region: str = None) -> list:
    """
    Lists objects using Boto3 Paginator abstraction.

    :param bucket_name: Target S3 bucket.
    :param page_size: Artificial page limit (MaxKeys per request page).
    :param prefix: Key prefix filter.
    :param region: AWS Region.
    :return: Accumulated list of all object keys.
    """
    region = region or AWS_REGION
    s3_client = get_s3_client(region_name=region)

    print(f"\n[INFO] Initializing Paginator for list_objects_v2 on s3://{bucket_name}...")
    print(f"       Page Size (MaxKeys): {page_size}")

    all_keys = []
    page_count = 0

    try:
        paginator = s3_client.get_paginator("list_objects_v2")
        page_iterator = paginator.paginate(
            Bucket=bucket_name,
            Prefix=prefix,
            PaginationConfig={"PageSize": page_size}
        )

        for page in page_iterator:
            page_count += 1
            contents = page.get("Contents", [])
            print(f"\n[PAGE {page_count}] Retrieved {len(contents)} object(s) in page:")
            for obj in contents:
                key = obj["Key"]
                size = obj["Size"]
                print(f"  - Key: {key:<35} | Size: {size} bytes")
                all_keys.append(key)

        print(f"\n[SUCCESS] Pagination complete! Retrieved {len(all_keys)} total object(s) across {page_count} page(s).")
        return all_keys

    except ClientError as e:
        print(f"[ERROR] ClientError during pagination: {e.response['Error']['Message']}")
        return []
    except NoCredentialsError:
        print("[ERROR] AWS credentials not found.")
        return []


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Demonstrate S3 Pagination using Boto3 Paginator.")
    parser.add_argument("--bucket", type=str, default=S3_BUCKET_NAME, help="Target S3 bucket name")
    parser.add_argument("--page-size", type=int, default=2, help="Keys per page limit")
    parser.add_argument("--prefix", type=str, default="", help="Prefix filter")
    parser.add_argument("--region", type=str, default=AWS_REGION, help="AWS Region")

    args = parser.parse_args()

    list_objects_with_pagination(
        bucket_name=args.bucket,
        page_size=args.page_size,
        prefix=args.prefix,
        region=args.region
    )
