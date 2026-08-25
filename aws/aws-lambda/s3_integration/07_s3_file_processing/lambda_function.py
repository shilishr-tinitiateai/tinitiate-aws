"""
AWS Lambda Operation 07: S3 File Processing

Demonstrates downloading a triggered S3 file into Lambda's ephemeral /tmp storage,
processing its contents (parsing text/JSON metrics), and reporting results to CloudWatch.
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


def process_s3_object(bucket_name: str, object_key: str, s3_client: Any = None) -> Dict[str, Any]:
    """
    Downloads an S3 object to ephemeral /tmp directory and computes file content metrics.

    :param bucket_name: S3 bucket name.
    :param object_key: S3 object key.
    :param s3_client: Boto3 S3 Client instance.
    :return: Processed metrics summary dictionary.
    """
    if s3_client is None:
        s3_client = boto3.client("s3")

    # Resolve local path inside ephemeral /tmp storage
    filename = Path(object_key).name
    tmp_download_path = Path("/tmp") / filename if os.name != "nt" else Path("./scratch") / filename
    tmp_download_path.parent.mkdir(parents=True, exist_ok=True)

    print(f"[INFO] Downloading s3://{bucket_name}/{object_key} -> '{tmp_download_path}'...")

    try:
        s3_client.download_file(Bucket=bucket_name, Key=object_key, Filename=str(tmp_download_path))
        
        file_size = tmp_download_path.stat().st_size
        with open(tmp_download_path, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()

        line_count = len(content.splitlines())
        word_count = len(content.split())
        char_count = len(content)

        metrics = {
            "bucket": bucket_name,
            "key": object_key,
            "local_tmp_path": str(tmp_download_path),
            "file_size_bytes": file_size,
            "line_count": line_count,
            "word_count": word_count,
            "character_count": char_count,
            "content_preview": content[:100].strip() + ("..." if len(content) > 100 else "")
        }

        print(f"[SUCCESS] Processed S3 File Metrics: Lines: {line_count} | Words: {word_count} | Size: {file_size} bytes")

        # Cleanup ephemeral file
        if tmp_download_path.exists():
            tmp_download_path.unlink()
            print(f"[INFO] Cleaned up ephemeral file '{tmp_download_path}'.")

        return metrics

    except ClientError as e:
        print(f"[ERROR] ClientError processing S3 object: {e.response['Error']['Message']}")
        return {"error": e.response['Error']['Message']}
    except Exception as e:
        print(f"[ERROR] Unexpected error: {e}")
        return {"error": str(e)}


def lambda_handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """
    AWS Lambda Handler Entrypoint for S3 File Processing.
    """
    print("[INFO] S3 File Processing function started.")
    
    results = []
    for record in event.get("Records", []):
        s3_data = record.get("s3", {})
        bucket = s3_data.get("bucket", {}).get("name")
        raw_key = s3_data.get("object", {}).get("key")

        if bucket and raw_key:
            key = urllib.parse.unquote_plus(raw_key)
            metrics = process_s3_object(bucket_name=bucket, object_key=key)
            results.append(metrics)

    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps({
            "status": "success",
            "processed_files_count": len(results),
            "results": results
        })
    }


# Local Test Driver
if __name__ == "__main__":
    print("=== LOCAL TEST DRIVER: S3 FILE PROCESSING ===")

    from shared.config import LOCAL_SAMPLE_FILE

    # Mock S3 Client for testing local sample file
    class MockS3Client:
        def download_file(self, Bucket, Key, Filename):
            with open(LOCAL_SAMPLE_FILE, "rb") as src, open(Filename, "wb") as dst:
                dst.write(src.read())

    mock_event = {
        "Records": [
            {
                "s3": {
                    "bucket": {"name": "my-learning-s3-bucket-unique-12345"},
                    "object": {"key": "sample.txt"}
                }
            }
        ]
    }

    # Pass mock client into function
    sample_key = mock_event["Records"][0]["s3"]["object"]["key"]
    res = process_s3_object(bucket_name="my-learning-s3-bucket-unique-12345", object_key=sample_key, s3_client=MockS3Client())
    print("\nProcessed Summary:")
    print(json.dumps(res, indent=2))
