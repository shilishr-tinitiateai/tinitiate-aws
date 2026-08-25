"""
AWS S3 Operation 02: Upload File

Demonstrates uploading a local file to an S3 bucket using boto3's managed
upload_file method, handling cross-platform paths using pathlib.
"""

import sys
import argparse
from pathlib import Path
import boto3
from botocore.exceptions import ClientError, NoCredentialsError

# Add parent directory to sys.path
sys.path.append(str(Path(__file__).resolve().parent.parent.parent.parent))

from shared.config import AWS_REGION, S3_BUCKET_NAME, S3_OBJECT_KEY, LOCAL_SAMPLE_FILE
from shared.aws_client import get_s3_client


def upload_file(local_path: Path, bucket_name: str, object_key: str, region: str = None) -> bool:
    """
    Uploads a local file to an S3 bucket using managed upload_file.

    :param local_path: Path object pointing to local file.
    :param bucket_name: Destination S3 bucket name.
    :param object_key: S3 object key (destination path in bucket).
    :param region: AWS Region.
    :return: True if upload succeeded, False otherwise.
    """
    region = region or AWS_REGION
    
    if not local_path.exists():
        print(f"[ERROR] Local file not found at path: '{local_path}'")
        return False

    s3_client = get_s3_client(region_name=region)

    print(f"[INFO] Uploading '{local_path}' -> s3://{bucket_name}/{object_key}...")

    try:
        s3_client.upload_file(
            Filename=str(local_path),
            Bucket=bucket_name,
            Key=object_key
        )
        print(f"[SUCCESS] File uploaded successfully!")
        print(f"         Bucket: {bucket_name}")
        print(f"         Key:    {object_key}")
        print(f"         Size:   {local_path.stat().st_size} bytes")
        return True

    except ClientError as e:
        error_code = e.response["Error"]["Code"]
        error_msg = e.response["Error"]["Message"]
        if error_code == "NoSuchBucket":
            print(f"[ERROR] The bucket '{bucket_name}' does not exist.")
        elif error_code == "AccessDenied":
            print(f"[ERROR] Access denied when attempting to upload to bucket '{bucket_name}'.")
        else:
            print(f"[ERROR] ClientError during upload [{error_code}]: {error_msg}")
        return False
    except NoCredentialsError:
        print("[ERROR] AWS credentials not found. Run 'aws configure' first.")
        return False


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Upload a local file to AWS S3.")
    parser.add_argument("--bucket", type=str, default=S3_BUCKET_NAME, help="Target S3 bucket name")
    parser.add_argument("--file", type=str, default=str(LOCAL_SAMPLE_FILE), help="Local file path")
    parser.add_argument("--key", type=str, default=S3_OBJECT_KEY, help="S3 object key")
    parser.add_argument("--region", type=str, default=AWS_REGION, help="AWS Region")

    args = parser.parse_args()

    file_path = Path(args.file)
    success = upload_file(local_path=file_path, bucket_name=args.bucket, object_key=args.key, region=args.region)
    sys.exit(0 if success else 1)
