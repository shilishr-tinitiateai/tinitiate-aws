"""
AWS Lambda Operation 10: IAM Execution Roles & Permissions

Demonstrates checking AWS IAM execution permissions, catching AccessDenied ClientErrors,
and enforcing least privilege principle for S3 and CloudWatch access inside Lambda.
"""

import os
import json
from typing import Dict, Any
import boto3
from botocore.exceptions import ClientError, NoCredentialsError


def verify_s3_permissions(bucket_name: str) -> Dict[str, Any]:
    """
    Tests S3 permissions by invoking ListBucket and PutObject API calls.

    :param bucket_name: S3 bucket name.
    :return: Permission test evaluation dictionary.
    """
    s3_client = boto3.client("s3")
    permission_report = {
        "bucket": bucket_name,
        "s3:ListBucket": "UNKNOWN",
        "s3:PutObject": "UNKNOWN"
    }

    # Test 1: ListBucket permission
    try:
        s3_client.list_objects_v2(Bucket=bucket_name, MaxKeys=1)
        permission_report["s3:ListBucket"] = "ALLOWED"
        print(f"[PERMISSION SUCCESS] s3:ListBucket granted on bucket '{bucket_name}'.")
    except ClientError as e:
        if e.response["Error"]["Code"] == "AccessDenied":
            permission_report["s3:ListBucket"] = "DENIED (Missing s3:ListBucket IAM action)"
            print(f"[PERMISSION DENIED] s3:ListBucket denied on bucket '{bucket_name}'.")
        else:
            permission_report["s3:ListBucket"] = f"ERROR: {e.response['Error']['Code']}"

    # Test 2: PutObject permission
    try:
        test_key = "permissions_check.txt"
        s3_client.put_object(
            Bucket=bucket_name,
            Key=test_key,
            Body=b"IAM Permission Audit Check Payload"
        )
        permission_report["s3:PutObject"] = "ALLOWED"
        print(f"[PERMISSION SUCCESS] s3:PutObject granted on bucket '{bucket_name}'.")
    except ClientError as e:
        if e.response["Error"]["Code"] == "AccessDenied":
            permission_report["s3:PutObject"] = "DENIED (Missing s3:PutObject IAM action)"
            print(f"[PERMISSION DENIED] s3:PutObject denied on bucket '{bucket_name}'.")
        else:
            permission_report["s3:PutObject"] = f"ERROR: {e.response['Error']['Code']}"

    return permission_report


def lambda_handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """
    AWS Lambda Handler Entrypoint.
    """
    bucket_name = event.get("bucket_name", os.environ.get("S3_BUCKET_NAME", "my-learning-s3-bucket-unique-12345"))
    print(f"[INFO] Auditing IAM Execution Role permissions for S3 bucket '{bucket_name}'...")

    try:
        audit_results = verify_s3_permissions(bucket_name=bucket_name)
        return {
            "statusCode": 200,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({"status": "audit_complete", "permissions": audit_results})
        }
    except NoCredentialsError:
        print("[ERROR] AWS Credentials missing.")
        return {
            "statusCode": 500,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({"status": "error", "message": "AWS credentials missing"})
        }


if __name__ == "__main__":
    print("=== LOCAL TEST DRIVER: LAMBDA PERMISSIONS AUDIT ===")
    
    # Mock S3 Client to simulate IAM Permission Checks
    class MockPermissionS3Client:
        def list_objects_v2(self, Bucket, MaxKeys):
            return {"Contents": []}
        def put_object(self, Bucket, Key, Body):
            raise ClientError({"Error": {"Code": "AccessDenied", "Message": "Access Denied by IAM Policy"}}, "PutObject")

    # Monkey patch boto3 client for local dry run
    boto3.client = lambda service, **kwargs: MockPermissionS3Client()

    res = lambda_handler(event={"bucket_name": "test-audit-bucket"}, context=None)
    print("\nAudit Response:")
    print(json.dumps(res, indent=2))
