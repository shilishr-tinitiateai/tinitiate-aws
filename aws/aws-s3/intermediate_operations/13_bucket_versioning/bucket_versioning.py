"""
AWS S3 Operation 13: Bucket Versioning

Demonstrates reading, enabling, and querying S3 Bucket Versioning configurations
and listing object versions via boto3 get_bucket_versioning, put_bucket_versioning,
and list_object_versions.
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


def get_versioning_status(bucket_name: str, region: str = None) -> str:
    """
    Checks the current versioning status of an S3 bucket.

    :param bucket_name: S3 bucket name.
    :param region: AWS Region.
    :return: Versioning status string ('Enabled', 'Suspended', or 'Disabled').
    """
    region = region or AWS_REGION
    s3_client = get_s3_client(region_name=region)

    print(f"[INFO] Checking versioning status for s3://{bucket_name}...")

    try:
        response = s3_client.get_bucket_versioning(Bucket=bucket_name)
        status = response.get("Status", "Disabled (Never Enabled)")
        print(f"[SUCCESS] Bucket Versioning Status: '{status}'")
        return status

    except ClientError as e:
        print(f"[ERROR] Failed to get versioning status: {e.response['Error']['Message']}")
        return "Unknown"


def set_versioning_status(bucket_name: str, enable: bool = True, region: str = None) -> bool:
    """
    Enables or suspends S3 Bucket Versioning.

    :param bucket_name: S3 bucket name.
    :param enable: Enable versioning if True, suspend if False.
    :param region: AWS Region.
    :return: True if status updated successfully, False otherwise.
    """
    region = region or AWS_REGION
    s3_client = get_s3_client(region_name=region)

    target_status = "Enabled" if enable else "Suspended"
    print(f"[INFO] Updating versioning status on s3://{bucket_name} -> '{target_status}'...")

    try:
        s3_client.put_bucket_versioning(
            Bucket=bucket_name,
            VersioningConfiguration={"Status": target_status}
        )
        print(f"[SUCCESS] Bucket Versioning configured to '{target_status}' successfully!")
        return True

    except ClientError as e:
        print(f"[ERROR] ClientError enabling versioning: {e.response['Error']['Message']}")
        return False
    except NoCredentialsError:
        print("[ERROR] AWS credentials not found.")
        return False


def list_versions(bucket_name: str, prefix: str = "", region: str = None) -> dict:
    """
    Lists all object versions and delete markers in an S3 bucket.

    :param bucket_name: S3 bucket name.
    :param prefix: Optional prefix string filter.
    :param region: AWS Region.
    :return: Response dictionary.
    """
    region = region or AWS_REGION
    s3_client = get_s3_client(region_name=region)

    print(f"\n[INFO] Listing object versions in s3://{bucket_name}...")

    try:
        kwargs = {"Bucket": bucket_name}
        if prefix:
            kwargs["Prefix"] = prefix

        response = s3_client.list_object_versions(**kwargs)
        versions = response.get("Versions", [])
        delete_markers = response.get("DeleteMarkers", [])

        print(f"[SUCCESS] Found {len(versions)} object version(s):")
        for v in versions:
            is_latest = "[LATEST]" if v.get("IsLatest") else "        "
            print(f"  {is_latest} Key: {v['Key']:<30} | VersionId: {v['VersionId'][:12]}... | Size: {v['Size']} bytes")

        if delete_markers:
            print(f"[SUCCESS] Found {len(delete_markers)} Delete Marker(s):")
            for dm in delete_markers:
                print(f"  [DELETE MARKER] Key: {dm['Key']:<25} | VersionId: {dm['VersionId'][:12]}...")

        return response

    except ClientError as e:
        print(f"[ERROR] Failed to list object versions: {e.response['Error']['Message']}")
        return {}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Manage AWS S3 Bucket Versioning.")
    parser.add_argument("--bucket", type=str, default=S3_BUCKET_NAME, help="S3 bucket name")
    parser.add_argument("--suspend", action="store_true", help="Suspend versioning instead of enabling")
    parser.add_argument("--region", type=str, default=AWS_REGION, help="AWS Region")

    args = parser.parse_args()

    # Step 1: Check status
    get_versioning_status(bucket_name=args.bucket, region=args.region)

    # Step 2: Enable versioning
    set_versioning_status(bucket_name=args.bucket, enable=not args.suspend, region=args.region)

    # Step 3: Verify updated status
    get_versioning_status(bucket_name=args.bucket, region=args.region)

    # Step 4: List object versions
    list_versions(bucket_name=args.bucket, region=args.region)
