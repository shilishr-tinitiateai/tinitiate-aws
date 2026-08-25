"""
AWS S3 Operation 04: Download File

Demonstrates downloading an object from an S3 bucket to the local filesystem using
boto3's managed download_file method and pathlib.
"""

import sys
import argparse
from pathlib import Path
import boto3
from botocore.exceptions import ClientError, NoCredentialsError

# Add parent directory to sys.path
sys.path.append(str(Path(__file__).resolve().parent.parent.parent.parent))

from shared.config import AWS_REGION, S3_BUCKET_NAME, S3_OBJECT_KEY, get_downloads_dir
from shared.aws_client import get_s3_client


def download_file(bucket_name: str, object_key: str, dest_path: Path, region: str = None) -> bool:
    """
    Downloads an S3 object to a local filesystem destination.

    :param bucket_name: S3 bucket name.
    :param object_key: Key of object in S3.
    :param dest_path: Path object for local destination file.
    :param region: AWS Region.
    :return: True if download succeeded, False otherwise.
    """
    region = region or AWS_REGION
    s3_client = get_s3_client(region_name=region)

    # Ensure parent destination folder exists
    dest_path.parent.mkdir(parents=True, exist_ok=True)

    print(f"[INFO] Downloading s3://{bucket_name}/{object_key} -> '{dest_path}'...")

    try:
        s3_client.download_file(
            Bucket=bucket_name,
            Key=object_key,
            Filename=str(dest_path)
        )
        print(f"[SUCCESS] Download completed successfully!")
        print(f"         Local File: {dest_path}")
        print(f"         Size:       {dest_path.stat().st_size} bytes")
        return True

    except ClientError as e:
        error_code = e.response["Error"]["Code"]
        error_msg = e.response["Error"]["Message"]

        if error_code in ("404", "NoSuchKey"):
            print(f"[ERROR] The object key '{object_key}' does not exist in bucket '{bucket_name}'.")
        elif error_code == "NoSuchBucket":
            print(f"[ERROR] The bucket '{bucket_name}' does not exist.")
        elif error_code == "AccessDenied":
            print(f"[ERROR] Access denied when attempting to download '{object_key}'.")
        else:
            print(f"[ERROR] ClientError downloading file [{error_code}]: {error_msg}")
        return False
    except NoCredentialsError:
        print("[ERROR] AWS credentials not found.")
        return False


if __name__ == "__main__":
    default_dest = get_downloads_dir() / "downloaded_sample.txt"

    parser = argparse.ArgumentParser(description="Download a file from AWS S3.")
    parser.add_argument("--bucket", type=str, default=S3_BUCKET_NAME, help="Source S3 bucket name")
    parser.add_argument("--key", type=str, default=S3_OBJECT_KEY, help="S3 object key to download")
    parser.add_argument("--dest", type=str, default=str(default_dest), help="Local destination file path")
    parser.add_argument("--region", type=str, default=AWS_REGION, help="AWS Region")

    args = parser.parse_args()

    destination = Path(args.dest)
    success = download_file(bucket_name=args.bucket, object_key=args.key, dest_path=destination, region=args.region)
    sys.exit(0 if success else 1)
