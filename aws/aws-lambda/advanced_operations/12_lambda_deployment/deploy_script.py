"""
AWS Lambda Operation 12: Automated Boto3 Packaging & Deployment Script

Demonstrates programmatically zip-packaging lambda_function.py in memory
and deploying/updating it on AWS Lambda using boto3 create_function and update_function_code.
"""

import io
import sys
import json
import zipfile
import argparse
from pathlib import Path
import boto3
from botocore.exceptions import ClientError, NoCredentialsError

# Add parent directory to sys.path
sys.path.append(str(Path(__file__).resolve().parent.parent.parent.parent))

from shared.config import AWS_REGION, LAMBDA_FUNCTION_NAME, LAMBDA_ROLE_ARN
from shared.aws_client import get_lambda_client


def build_deployment_zip(source_file: Path) -> bytes:
    """
    Creates an in-memory ZIP deployment archive containing the target lambda_function.py.

    :param source_file: Path to lambda_function.py.
    :return: Raw ZIP archive bytes.
    """
    print(f"[INFO] Packaging deployment ZIP archive from '{source_file}'...")
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zf:
        # Write file as lambda_function.py at root of zip archive
        zf.write(source_file, arcname="lambda_function.py")

    zip_bytes = zip_buffer.getvalue()
    print(f"[SUCCESS] ZIP package generated ({len(zip_bytes)} bytes).")
    return zip_bytes


def deploy_lambda_function(function_name: str, role_arn: str, zip_bytes: bytes, region: str = None) -> bool:
    """
    Deploys or updates a Lambda function using Boto3.

    :param function_name: Name of the Lambda function.
    :param role_arn: IAM Execution Role ARN.
    :param zip_bytes: Raw ZIP archive bytes.
    :param region: AWS Region.
    :return: True if deployment succeeded, False otherwise.
    """
    region = region or AWS_REGION
    lambda_client = get_lambda_client(region_name=region)

    print(f"[INFO] Deploying Lambda function '{function_name}' to region '{region}'...")

    try:
        # Step 1: Try updating existing function code
        print(f"       [Attempt] Updating existing function code for '{function_name}'...")
        response = lambda_client.update_function_code(
            FunctionName=function_name,
            ZipFile=zip_bytes,
            Publish=True
        )
        print(f"[SUCCESS] Function code updated successfully!")
        print(f"         Function ARN: {response.get('FunctionArn')}")
        print(f"         Version:      {response.get('Version')}")
        return True

    except ClientError as e:
        error_code = e.response["Error"]["Code"]
        if error_code == "ResourceNotFoundException":
            # Step 2: Create new function if function doesn't exist yet
            if not role_arn:
                print(f"[ERROR] Function '{function_name}' does not exist and no --role-arn was specified.")
                print("        Please provide an IAM Execution Role ARN via --role-arn or LAMBDA_ROLE_ARN env var.")
                return False

            print(f"       [Attempt] Function does not exist. Creating new function '{function_name}'...")
            try:
                create_res = lambda_client.create_function(
                    FunctionName=function_name,
                    Runtime="python3.12",
                    Role=role_arn,
                    Handler="lambda_function.lambda_handler",
                    Code={"ZipFile": zip_bytes},
                    Description="Automated deployment via boto3 script",
                    Timeout=15,
                    MemorySize=128
                )
                print(f"[SUCCESS] Function created successfully!")
                print(f"         Function ARN: {create_res.get('FunctionArn')}")
                return True
            except ClientError as create_err:
                print(f"[ERROR] Failed to create function: {create_err.response['Error']['Message']}")
                return False
        else:
            print(f"[ERROR] ClientError during deployment [{error_code}]: {e.response['Error']['Message']}")
            return False
    except NoCredentialsError:
        print("[ERROR] AWS credentials not found. Run 'aws configure' first.")
        return False


def invoke_deployed_function(function_name: str, region: str = None) -> bool:
    """
    Invokes the deployed Lambda function in AWS Cloud using Boto3 invoke.

    :param function_name: Name of the Lambda function.
    :param region: AWS Region.
    :return: True if invocation succeeded, False otherwise.
    """
    region = region or AWS_REGION
    lambda_client = get_lambda_client(region_name=region)

    payload = {"action": "cloud_deployment_verification"}
    print(f"\n[INFO] Invoking deployed cloud function '{function_name}'...")

    try:
        response = lambda_client.invoke(
            FunctionName=function_name,
            InvocationType="RequestResponse",
            Payload=json.dumps(payload).encode("utf-8")
        )
        response_payload = json.loads(response["Payload"].read().decode("utf-8"))
        print(f"[SUCCESS] Remote Invocation Status Code: {response.get('StatusCode')}")
        print("         Cloud Output Payload:")
        print(json.dumps(response_payload, indent=2))
        return True
    except ClientError as e:
        print(f"[ERROR] Remote invocation failed: {e.response['Error']['Message']}")
        return False


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Package and deploy AWS Lambda function via Boto3.")
    parser.add_argument("--name", type=str, default=LAMBDA_FUNCTION_NAME, help="Lambda function name")
    parser.add_argument("--role-arn", type=str, default=LAMBDA_ROLE_ARN, help="IAM Execution Role ARN")
    parser.add_argument("--invoke", action="store_true", help="Invoke cloud function after deployment")
    parser.add_argument("--region", type=str, default=AWS_REGION, help="AWS Region")

    args = parser.parse_args()

    source_path = Path(__file__).resolve().parent / "lambda_function.py"
    zip_data = build_deployment_zip(source_file=source_path)

    deployed = deploy_lambda_function(
        function_name=args.name,
        role_arn=args.role_arn,
        zip_bytes=zip_data,
        region=args.region
    )

    if deployed and args.invoke:
        invoke_deployed_function(function_name=args.name, region=args.region)
