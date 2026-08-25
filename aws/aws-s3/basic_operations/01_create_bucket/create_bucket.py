"""
AWS S3 Operation 01: Create Bucket

Demonstrates creating an S3 bucket programmatically using boto3, handling
region constraints (us-east-1 vs. other regions), bucket naming rules,
and common boto3 exceptions.
"""

import sys
import argparse
import boto3
from botocore.exceptions import ClientError, NoCredentialsError, ParamValidationError

# Add parent directory to sys.path to enable importing shared helpers when run directly
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent.parent.parent))

from shared.config import AWS_REGION, S3_BUCKET_NAME
from shared.aws_client import get_s3_client


def create_bucket(bucket_name: str, region: str = None) -> bool:
    """
    Creates an S3 bucket in the specified AWS region.

    :param bucket_name: Globally unique S3 bucket name.
    :param region: AWS region string (e.g., 'us-east-1', 'ap-south-1').
    :return: True if successful or already owned, False otherwise.
    """
    region = region or AWS_REGION
    s3_client = get_s3_client(region_name=region)

    print(f"[INFO] Attempting to create S3 bucket '{bucket_name}' in region '{region}'...")

    try:
        # us-east-1 does not require/accept LocationConstraint
        if region == "us-east-1":
            response = s3_client.create_bucket(Bucket=bucket_name)
        else:
            response = s3_client.create_bucket(
                Bucket=bucket_name,
                CreateBucketConfiguration={"LocationConstraint": region}
            )

        location = response.get("Location", f"/{bucket_name}")
        print(f"[SUCCESS] Bucket created successfully!")
        print(f"         Bucket Name: {bucket_name}")
        print(f"         Location:    {location}")
        return True

    except ClientError as e:
        error_code = e.response["Error"]["Code"]
        error_msg = e.response["Error"]["Message"]
        
        if error_code == "BucketAlreadyOwnedByYou":
            print(f"[WARNING] Bucket '{bucket_name}' already exists and is owned by you.")
            return True
        elif error_code == "BucketAlreadyExists":
            print(f"[ERROR] Bucket '{bucket_name}' already exists globally and is owned by another account.")
            print("        Please choose a different, globally unique bucket name.")
            return False
        elif error_code == "InvalidLocationConstraint":
            print(f"[ERROR] Invalid location constraint specified for region '{region}'.")
            return False
        elif error_code == "AccessDenied":
            print(f"[ERROR] Access denied. Your IAM user/role lacks 's3:CreateBucket' permissions.")
            return False
        else:
            print(f"[ERROR] ClientError creating bucket [{error_code}]: {error_msg}")
            return False

    except ParamValidationError as e:
        print(f"[ERROR] Parameter validation failed: {e}")
        return False
    except NoCredentialsError:
        print("[ERROR] AWS credentials not found. Run 'aws configure' first.")
        return False


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Create an AWS S3 Bucket.")
    parser.add_argument("--bucket", type=str, default=S3_BUCKET_NAME, help="Name of the S3 bucket")
    parser.add_argument("--region", type=str, default=AWS_REGION, help="AWS Region")
    
    args = parser.parse_args()
    
    success = create_bucket(bucket_name=args.bucket, region=args.region)
    sys.exit(0 if success else 1)
