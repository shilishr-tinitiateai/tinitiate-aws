"""
AWS S3 Operation 11: Object Access Control List (ACL)

Demonstrates reading and setting S3 object ACLs (Access Control Lists).
Note: AWS best practice recommends keeping ACLs disabled (Bucket Owner Enforced)
and relying exclusively on IAM & Bucket Policies.
"""

import sys
import argparse
from pathlib import Path
import boto3
from botocore.exceptions import ClientError, NoCredentialsError

# Add parent directory to sys.path
sys.path.append(str(Path(__file__).resolve().parent.parent.parent.parent))

from shared.config import AWS_REGION, S3_BUCKET_NAME, S3_OBJECT_KEY
from shared.aws_client import get_s3_client


def get_object_acl(bucket_name: str, object_key: str, region: str = None) -> dict:
    """
    Retrieves the ACL for a specific S3 object.

    :param bucket_name: S3 bucket name.
    :param object_key: S3 object key.
    :param region: AWS Region.
    :return: ACL response dictionary.
    """
    region = region or AWS_REGION
    s3_client = get_s3_client(region_name=region)

    print(f"[INFO] Reading ACL for s3://{bucket_name}/{object_key}...")

    try:
        response = s3_client.get_object_acl(Bucket=bucket_name, Key=object_key)
        owner = response.get("Owner", {})
        grants = response.get("Grants", [])

        print(f"[SUCCESS] Object Owner: {owner.get('DisplayName', 'N/A')} (ID: {owner.get('ID', 'N/A')[:12]}...)")
        print(f"[SUCCESS] Found {len(grants)} Grant(s):")
        for grant in grants:
            grantee = grant.get("Grantee", {})
            permission = grant.get("Permission", "")
            grantee_type = grantee.get("Type", "")
            grantee_id = grantee.get("ID") or grantee.get("URI") or "N/A"
            print(f"  - Grantee Type: {grantee_type:<10} | Permission: {permission:<12} | ID: {grantee_id}")

        return response

    except ClientError as e:
        error_code = e.response["Error"]["Code"]
        if error_code == "AccessControlListNotSupported":
            print("[INFO] ACLs are disabled on this bucket (Bucket Owner Enforced). This is AWS's security best practice.")
        else:
            print(f"[ERROR] ClientError fetching ACL [{error_code}]: {e.response['Error']['Message']}")
        return {}


def set_object_acl(bucket_name: str, object_key: str, acl_canned: str = "private", region: str = None) -> bool:
    """
    Sets a canned ACL (e.g. 'private', 'bucket-owner-full-control') on an object.

    :param bucket_name: S3 bucket name.
    :param object_key: S3 object key.
    :param acl_canned: Canned ACL string.
    :param region: AWS Region.
    :return: True if successful, False otherwise.
    """
    region = region or AWS_REGION
    s3_client = get_s3_client(region_name=region)

    print(f"[INFO] Setting canned ACL '{acl_canned}' on s3://{bucket_name}/{object_key}...")

    try:
        s3_client.put_object_acl(
            Bucket=bucket_name,
            Key=object_key,
            ACL=acl_canned
        )
        print(f"[SUCCESS] Object ACL updated to '{acl_canned}' successfully!")
        return True

    except ClientError as e:
        error_code = e.response["Error"]["Code"]
        if error_code == "AccessControlListNotSupported":
            print("[WARNING] Cannot set ACL: ACLs are disabled on this bucket (Bucket Owner Enforced).")
            print("          Use IAM Policies or Bucket Policies for access control.")
        else:
            print(f"[ERROR] ClientError applying ACL [{error_code}]: {e.response['Error']['Message']}")
        return False


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Read and set AWS S3 Object ACLs.")
    parser.add_argument("--bucket", type=str, default=S3_BUCKET_NAME, help="S3 bucket name")
    parser.add_argument("--key", type=str, default=S3_OBJECT_KEY, help="S3 object key")
    parser.add_argument("--acl", type=str, default="private", help="Canned ACL (private, bucket-owner-full-control)")
    parser.add_argument("--region", type=str, default=AWS_REGION, help="AWS Region")

    args = parser.parse_args()

    get_object_acl(bucket_name=args.bucket, object_key=args.key, region=args.region)
    set_object_acl(bucket_name=args.bucket, object_key=args.key, acl_canned=args.acl, region=args.region)
