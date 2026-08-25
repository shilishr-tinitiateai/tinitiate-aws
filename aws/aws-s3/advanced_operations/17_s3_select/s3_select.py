"""
AWS S3 Operation 17: S3 Select Query

Demonstrates querying file content directly inside S3 using SQL expressions
via select_object_content without downloading the full dataset.
"""

import sys
import argparse
from pathlib import Path
import boto3
from botocore.exceptions import ClientError, NoCredentialsError

# Add parent directory to sys.path
sys.path.append(str(Path(__file__).resolve().parent.parent.parent.parent))

from shared.config import AWS_REGION, S3_BUCKET_NAME, LOCAL_SAMPLE_JSON
from shared.aws_client import get_s3_client


def query_s3_select(bucket_name: str, object_key: str, sql_expression: str, region: str = None) -> str:
    """
    Executes an S3 Select SQL query on a JSON or CSV object stored in S3.

    :param bucket_name: S3 bucket name.
    :param object_key: Object key to query.
    :param sql_expression: SQL query expression.
    :param region: AWS Region.
    :return: Query output payload string.
    """
    region = region or AWS_REGION
    s3_client = get_s3_client(region_name=region)

    # First ensure sample JSON file is present in S3
    if LOCAL_SAMPLE_JSON.exists():
        try:
            s3_client.upload_file(Filename=str(LOCAL_SAMPLE_JSON), Bucket=bucket_name, Key=object_key)
        except Exception:
            pass

    print(f"\n[INFO] Executing S3 Select query on s3://{bucket_name}/{object_key}...")
    print(f"       SQL Expression: \"{sql_expression}\"")

    try:
        response = s3_client.select_object_content(
            Bucket=bucket_name,
            Key=object_key,
            ExpressionType="SQL",
            Expression=sql_expression,
            InputSerialization={"JSON": {"Type": "DOCUMENT"}},
            OutputSerialization={"JSON": {"RecordDelimiter": "\n"}}
        )

        output_records = ""
        for event in response.get("Payload", []):
            if "Records" in event:
                records = event["Records"]["Payload"].decode("utf-8")
                output_records += records
            elif "Stats" in event:
                stats = event["Stats"]["Details"]
                print(f"[INFO] Query Stats - Bytes Scanned: {stats['BytesScanned']}, Processed: {stats['BytesProcessed']}")

        print(f"[SUCCESS] S3 Select Query Result:")
        print("----------------------------------------")
        print(output_records.strip())
        print("----------------------------------------")
        return output_records

    except ClientError as e:
        error_code = e.response["Error"]["Code"]
        print(f"[ERROR] ClientError executing S3 Select [{error_code}]: {e.response['Error']['Message']}")
        return ""
    except NoCredentialsError:
        print("[ERROR] AWS credentials not found.")
        return ""


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Query S3 Object Content using S3 Select SQL.")
    parser.add_argument("--bucket", type=str, default=S3_BUCKET_NAME, help="S3 bucket name")
    parser.add_argument("--key", type=str, default="sample.json", help="S3 JSON/CSV object key")
    parser.add_argument("--query", type=str, default="SELECT s.name, s.amount FROM S3Object[*].records[*] s WHERE s.amount > 100.0", help="SQL Expression")
    parser.add_argument("--region", type=str, default=AWS_REGION, help="AWS Region")

    args = parser.parse_args()

    query_s3_select(
        bucket_name=args.bucket,
        object_key=args.key,
        sql_expression=args.query,
        region=args.region
    )
