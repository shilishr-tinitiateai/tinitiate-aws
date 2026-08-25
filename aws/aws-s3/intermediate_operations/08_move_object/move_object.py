"""
AWS S3 Operation 08: Move Object

Demonstrates moving (renaming/relocating) an object in S3.
Since S3 has no native 'move' API, this implements the atomic pattern:
1. Server-side copy (copy_object)
2. Source deletion (delete_object)
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


def move_object(src_bucket: str, src_key: str, dest_bucket: str, dest_key: str, region: str = None) -> bool:
    """
    Moves an S3 object via copy-then-delete pattern.

    :param src_bucket: Source S3 bucket.
    :param src_key: Source object key.
    :param dest_bucket: Destination S3 bucket.
    :param dest_key: Destination object key.
    :param region: AWS Region.
    :return: True if move succeeded, False otherwise.
    """
    region = region or AWS_REGION
    s3_client = get_s3_client(region_name=region)

    copy_source = {"Bucket": src_bucket, "Key": src_key}

    print(f"[INFO] Initiating Move: s3://{src_bucket}/{src_key} -> s3://{dest_bucket}/{dest_key}")

    try:
        # Step 1: Copy to destination
        print("       [Step 1/2] Copying server-side...")
        s3_client.copy_object(
            CopySource=copy_source,
            Bucket=dest_bucket,
            Key=dest_key
        )
        print("       [Step 1/2] Copy complete.")

        # Step 2: Delete source
        print("       [Step 2/2] Deleting source object...")
        s3_client.delete_object(
            Bucket=src_bucket,
            Key=src_key
        )
        print("       [Step 2/2] Source deleted.")

        print(f"[SUCCESS] Object move completed successfully!")
        print(f"         Old Location: s3://{src_bucket}/{src_key}")
        print(f"         New Location: s3://{dest_bucket}/{dest_key}")
        return True

    except ClientError as e:
        error_code = e.response["Error"]["Code"]
        if error_code == "NoSuchKey":
            print(f"[ERROR] Source object '{src_key}' not found in bucket '{src_bucket}'.")
        else:
            print(f"[ERROR] ClientError during move operation [{error_code}]: {e.response['Error']['Message']}")
        return False
    except NoCredentialsError:
        print("[ERROR] AWS credentials not found.")
        return False


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Move/Rename an object in AWS S3.")
    parser.add_argument("--src-bucket", type=str, default=S3_BUCKET_NAME, help="Source S3 bucket")
    parser.add_argument("--src-key", type=str, default="copies/sample_copy.txt", help="Source object key")
    parser.add_argument("--dest-bucket", type=str, default=S3_BUCKET_NAME, help="Destination S3 bucket")
    parser.add_argument("--dest-key", type=str, default="archived/sample_moved.txt", help="Destination object key")
    parser.add_argument("--region", type=str, default=AWS_REGION, help="AWS Region")

    args = parser.parse_args()

    success = move_object(
        src_bucket=args.src_bucket,
        src_key=args.src_key,
        dest_bucket=args.dest_bucket,
        dest_key=args.dest_key,
        region=args.region
    )
    sys.exit(0 if success else 1)
