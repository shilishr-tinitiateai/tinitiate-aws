"""
Shared AWS Client Factory Module.

Centralized helper to instantiate boto3 S3 and Lambda clients/resources
using the standard AWS Credential Provider Chain.
"""

import sys
import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError, ClientError
from shared.config import AWS_REGION

def get_s3_client(region_name: str = None):
    """
    Instantiate and return a boto3 S3 client.
    
    :param region_name: AWS region string. Defaults to configured AWS_REGION.
    :return: boto3 S3 Client object.
    """
    region = region_name or AWS_REGION
    try:
        client = boto3.client("s3", region_name=region)
        return client
    except (NoCredentialsError, PartialCredentialsError) as e:
        print("[ERROR] AWS credentials not found or incomplete.")
        print("Please configure credentials via 'aws configure' or set AWS_ACCESS_KEY_ID & AWS_SECRET_ACCESS_KEY environment variables.")
        sys.exit(1)
    except Exception as e:
        print(f"[ERROR] Failed to initialize S3 client: {e}")
        sys.exit(1)

def get_s3_resource(region_name: str = None):
    """
    Instantiate and return a boto3 S3 Resource object.
    
    :param region_name: AWS region string. Defaults to configured AWS_REGION.
    :return: boto3 S3 Resource object.
    """
    region = region_name or AWS_REGION
    try:
        resource = boto3.resource("s3", region_name=region)
        return resource
    except (NoCredentialsError, PartialCredentialsError):
        print("[ERROR] AWS credentials not found or incomplete.")
        sys.exit(1)
    except Exception as e:
        print(f"[ERROR] Failed to initialize S3 resource: {e}")
        sys.exit(1)

def get_lambda_client(region_name: str = None):
    """
    Instantiate and return a boto3 Lambda client.
    
    :param region_name: AWS region string. Defaults to configured AWS_REGION.
    :return: boto3 Lambda Client object.
    """
    region = region_name or AWS_REGION
    try:
        client = boto3.client("lambda", region_name=region)
        return client
    except (NoCredentialsError, PartialCredentialsError):
        print("[ERROR] AWS credentials not found or incomplete.")
        sys.exit(1)
    except Exception as e:
        print(f"[ERROR] Failed to initialize Lambda client: {e}")
        sys.exit(1)
