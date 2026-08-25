"""
AWS S3 Operation 07: Copy Object

Demonstrates performing a server-side object copy between S3 buckets or prefixes
without downloading data to the local host machine using boto3 copy_object.
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


def copy_object(src_bucket: str, src_key: str, dest_bucket: str, dest_key: str, region: str = None) -> bool:
    """
    Copies an object server-side within S3.

    :param src_bucket: Source S3 bucket.
    :param src_key: Source object key.
    :param dest_bucket: Destination S3 bucket.
    :param dest_key: Destination object key.
    :param region: AWS Region.
    :return: True if copy succeeded, False otherwise.
    """
    region = region or AWS_REGION
    s3_client = get_s3_client(region_name=region)

    copy_source = {"Bucket": src_bucket, "Key": src_key}

    print(f"[INFO] Copying s3://{src_bucket}/{src_key} -> s3://{dest_bucket}/{dest_key}...")

    try:
        response = s3_client.copy_object(
            CopySource=copy_source,
            Bucket=dest_bucket,
            Key=dest_key
        )
        print(f"[SUCCESS] Object copied successfully!")
        print(f"         Source:      s3://{src_bucket}/{src_key}")
        print(f"         Destination: s3://{dest_bucket}/{dest_key}")
        print(f"         ETag:        {response.get('CopyObjectResult', {}).get('ETag', 'N/A')}")
        return True

    except ClientError as e:
        error_code = e.response["Error"]["Code"]
        if error_code == "NoSuchKey":
            print(f"[ERROR] Source object '{src_key}' does not exist in bucket '{src_bucket}'.")
        elif error_code == "NoSuchBucket":
            print(f"[ERROR] Either source or destination bucket does not exist.")
        elif error_code == "AccessDenied":
            print(f"[ERROR] Access denied. Requires s3:GetObject on source and s3:PutObject on destination.")
        else:
            print(f"[ERROR] ClientError copying object [{error_code}]: {e.response['Error']['Message']}")
        return False
    except NoCredentialsError:
        print("[ERROR] AWS credentials not found.")
        return False


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Copy an object server-side in AWS S3.")
    parser.add_argument("--src-bucket", type=str, default=S3_BUCKET_NAME, help="Source S3 bucket")
    parser.add_argument("--src-key", type=str, default="sample.txt", help="Source object key")
    parser.add_argument("--dest-bucket", type=str, default=S3_BUCKET_NAME, help="Destination S3 bucket")
    parser.add_argument("--dest-key", type=str, default="copies/sample_copy.txt", help="Destination object key")
    parser.add_argument("--region", type=str, default=AWS_REGION, help="AWS Region")

    args = parser.parse_args()

    success = copy_object(
        src_bucket=args.src_bucket,
        src_key=args.src_key,
        dest_bucket=args.dest_bucket,
        dest_key=args.dest_key,
        region=args.region
    )
    sys.exit(0 if success else 1)
