"""
AWS S3 Operation 12: Presigned URL

Demonstrates generating secure temporary Presigned URLs for S3 object downloads (GET)
and uploads (PUT) using boto3 generate_presigned_url, and verifies access via urllib.
"""

import sys
import argparse
import urllib.request
from pathlib import Path
import boto3
from botocore.exceptions import ClientError, NoCredentialsError

# Add parent directory to sys.path
sys.path.append(str(Path(__file__).resolve().parent.parent.parent.parent))

from shared.config import AWS_REGION, S3_BUCKET_NAME, S3_OBJECT_KEY
from shared.aws_client import get_s3_client


def generate_presigned_url(bucket_name: str, object_key: str, client_method: str = "get_object", expiration: int = 3600, region: str = None) -> str:
    """
    Generates a presigned URL to share temporary read or write access to an S3 object.

    :param bucket_name: S3 bucket name.
    :param object_key: S3 object key.
    :param client_method: Boto3 S3 client method ('get_object' or 'put_object').
    :param expiration: Expiration time in seconds (default: 3600 / 1 hour).
    :param region: AWS Region.
    :return: Presigned URL string or empty string on error.
    """
    region = region or AWS_REGION
    s3_client = get_s3_client(region_name=region)

    print(f"[INFO] Generating presigned URL for method '{client_method}' on s3://{bucket_name}/{object_key}...")
    print(f"       Expiration: {expiration} seconds ({expiration // 60} minutes)")

    try:
        url = s3_client.generate_presigned_url(
            ClientMethod=client_method,
            Params={"Bucket": bucket_name, "Key": object_key},
            ExpiresIn=expiration
        )
        print(f"[SUCCESS] Presigned URL generated successfully!")
        print(f"         URL: {url[:100]}...[TRUNCATED]")
        return url

    except ClientError as e:
        print(f"[ERROR] ClientError generating presigned URL: {e.response['Error']['Message']}")
        return ""
    except NoCredentialsError:
        print("[ERROR] AWS credentials not found.")
        return ""


def test_presigned_get_url(url: str) -> bool:
    """
    Executes a standard HTTP GET request against the generated presigned URL to verify functionality.

    :param url: Presigned URL string.
    :return: True if HTTP 200 OK received, False otherwise.
    """
    print("\n[INFO] Testing HTTP GET download using presigned URL...")
    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req) as response:
            content = response.read().decode("utf-8")
            print(f"[SUCCESS] HTTP GET Status Code: {response.status}")
            print(f"         Downloaded Content Snippet ({len(content)} bytes):")
            print(f"         '{content[:120].strip()}...'")
            return True
    except Exception as e:
        print(f"[ERROR] Failed to fetch content via presigned URL: {e}")
        return False


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate and test AWS S3 Presigned URLs.")
    parser.add_argument("--bucket", type=str, default=S3_BUCKET_NAME, help="S3 bucket name")
    parser.add_argument("--key", type=str, default=S3_OBJECT_KEY, help="S3 object key")
    parser.add_argument("--expires", type=int, default=3600, help="Expiration in seconds")
    parser.add_argument("--region", type=str, default=AWS_REGION, help="AWS Region")

    args = parser.parse_args()

    # Generate GET Presigned URL
    get_url = generate_presigned_url(
        bucket_name=args.bucket,
        object_key=args.key,
        client_method="get_object",
        expiration=args.expires,
        region=args.region
    )

    if get_url:
        test_presigned_get_url(get_url)

    # Generate PUT Presigned URL
    generate_presigned_url(
        bucket_name=args.bucket,
        object_key=args.key,
        client_method="put_object",
        expiration=args.expires,
        region=args.region
    )
