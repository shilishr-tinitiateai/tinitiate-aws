"""
AWS S3 Operation 09: Create Logical Folder (Prefix)

Demonstrates creating a logical directory structure (folder prefix) in S3.
Because S3 uses a flat object key architecture, folders are created by uploading
a zero-byte object whose key ends with a trailing slash '/'.
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


def create_folder(bucket_name: str, folder_name: str, region: str = None) -> bool:
    """
    Creates a zero-byte object key ending with '/' representing a logical folder.

    :param bucket_name: S3 bucket name.
    :param folder_name: Logical folder path (e.g. 'uploads/invoices').
    :param region: AWS Region.
    :return: True if folder created successfully, False otherwise.
    """
    region = region or AWS_REGION
    s3_client = get_s3_client(region_name=region)

    # Ensure trailing slash
    folder_key = folder_name.strip("/") + "/"

    print(f"[INFO] Creating logical folder 's3://{bucket_name}/{folder_key}'...")

    try:
        s3_client.put_object(
            Bucket=bucket_name,
            Key=folder_key,
            Body=b""  # 0-byte payload
        )
        print(f"[SUCCESS] Logical folder created successfully!")
        print(f"         Bucket:     {bucket_name}")
        print(f"         Folder Key: {folder_key}")
        return True

    except ClientError as e:
        print(f"[ERROR] Failed to create logical folder: {e.response['Error']['Message']}")
        return False
    except NoCredentialsError:
        print("[ERROR] AWS credentials not found.")
        return False


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Create a logical folder in AWS S3.")
    parser.add_argument("--bucket", type=str, default=S3_BUCKET_NAME, help="S3 bucket name")
    parser.add_argument("--folder", type=str, default="data/raw_files", help="Folder path name")
    parser.add_argument("--region", type=str, default=AWS_REGION, help="AWS Region")

    args = parser.parse_args()

    success = create_folder(bucket_name=args.bucket, folder_name=args.folder, region=args.region)
    sys.exit(0 if success else 1)
