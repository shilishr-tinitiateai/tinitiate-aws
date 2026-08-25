"""
AWS Lambda Operation 08: End-to-End S3 Event Pipeline

Demonstrates a complete serverless ETL pipeline:
1. S3 Trigger fires when object uploaded to Source Bucket.
2. Lambda downloads and transforms object content.
3. Lambda uploads transformed JSON/CSV report to Destination Bucket.
"""

import os
import sys
import json
import urllib.parse
from pathlib import Path
from typing import Dict, Any
import boto3
from botocore.exceptions import ClientError

# Add parent directory to sys.path
sys.path.append(str(Path(__file__).resolve().parent.parent.parent.parent))


def transform_and_deliver(src_bucket: str, src_key: str, dest_bucket: str, s3_client: Any = None) -> bool:
    """
    Executes ETL transform pipeline: Reads object from src_bucket, transforms content,
    and uploads summary report to dest_bucket under 'processed/' prefix.

    :param src_bucket: Source S3 bucket.
    :param src_key: Source object key.
    :param dest_bucket: Destination S3 bucket.
    :param s3_client: Boto3 S3 Client instance.
    :return: True if pipeline succeeded, False otherwise.
    """
    if s3_client is None:
        s3_client = boto3.client("s3")

    filename = Path(src_key).name
    dest_key = f"processed/processed_{Path(filename).stem}.json"

    print(f"[ETL STEP 1/3] Reading s3://{src_bucket}/{src_key}...")

    try:
        # Step 1: Read source object content
        response = s3_client.get_object(Bucket=src_bucket, Key=src_key)
        raw_bytes = response["Body"].read()
        raw_text = raw_bytes.decode("utf-8", errors="ignore")

        # Step 2: Transform content (calculate metrics & structure output)
        print("[ETL STEP 2/3] Transforming payload content...")
        lines = [line.strip() for line in raw_text.splitlines() if line.strip()]
        
        transformed_payload = {
            "pipeline_status": "SUCCESS",
            "source": {
                "bucket": src_bucket,
                "key": src_key,
                "size_bytes": len(raw_bytes)
            },
            "transformation_summary": {
                "total_non_empty_lines": len(lines),
                "word_count": sum(len(line.split()) for line in lines),
                "uppercase_sample": [line.upper() for line in lines[:3]]
            },
            "processed_timestamp_utc": "2026-08-25T12:00:00Z"
        }

        # Step 3: Write transformed payload to Destination Bucket
        print(f"[ETL STEP 3/3] Uploading transformed result -> s3://{dest_bucket}/{dest_key}...")
        s3_client.put_object(
            Bucket=dest_bucket,
            Key=dest_key,
            Body=json.dumps(transformed_payload, indent=2).encode("utf-8"),
            ContentType="application/json"
        )
        print(f"[SUCCESS] End-to-End S3 Pipeline Completed successfully!")
        print(f"         Output Location: s3://{dest_bucket}/{dest_key}")
        return True

    except ClientError as e:
        print(f"[ERROR] ClientError in S3 ETL Pipeline: {e.response['Error']['Message']}")
        return False
    except Exception as e:
        print(f"[ERROR] Pipeline Exception: {e}")
        return False


def lambda_handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """
    AWS Lambda Handler Entrypoint for End-to-End S3 Processing.
    """
    dest_bucket = os.environ.get("DEST_BUCKET_NAME", os.environ.get("S3_BUCKET_NAME", "my-learning-s3-bucket-unique-12345"))
    print(f"[INFO] Pipeline triggered. Configured Destination Bucket: '{dest_bucket}'")

    processed_count = 0
    for record in event.get("Records", []):
        s3_data = record.get("s3", {})
        src_bucket = s3_data.get("bucket", {}).get("name")
        raw_key = s3_data.get("object", {}).get("key")

        if src_bucket and raw_key:
            src_key = urllib.parse.unquote_plus(raw_key)
            if transform_and_deliver(src_bucket=src_bucket, src_key=src_key, dest_bucket=dest_bucket):
                processed_count += 1

    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps({
            "status": "success",
            "pipeline_executions": processed_count
        })
    }


if __name__ == "__main__":
    print("=== LOCAL TEST DRIVER: S3 PIPELINE ===")

    from shared.config import LOCAL_SAMPLE_FILE

    # Mock S3 Client for local pipeline testing
    class MockPipelineS3Client:
        def get_object(self, Bucket, Key):
            with open(LOCAL_SAMPLE_FILE, "rb") as f:
                content = f.read()
            return {"Body": type("MockBody", (), {"read": lambda self=None: content})()}

        def put_object(self, Bucket, Key, Body, ContentType):
            print(f"\n[MOCK S3 WRITE SUCCESS]")
            print(f"Bucket: {Bucket}")
            print(f"Key:    {Key}")
            print("Body Content:")
            print(Body.decode("utf-8"))

    mock_event = {
        "Records": [
            {
                "s3": {
                    "bucket": {"name": "source-bucket-12345"},
                    "object": {"key": "sample.txt"}
                }
            }
        ]
    }

    transform_and_deliver(
        src_bucket="source-bucket-12345",
        src_key="sample.txt",
        dest_bucket="dest-bucket-12345",
        s3_client=MockPipelineS3Client()
    )
