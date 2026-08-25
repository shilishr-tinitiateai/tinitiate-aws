"""
AWS S3 Operation 15: Low-Level Multipart Upload

Demonstrates low-level S3 Multipart Upload API using create_multipart_upload,
upload_part, complete_multipart_upload, and abort_multipart_upload.
"""

import sys
import argparse
from pathlib import Path
import boto3
from botocore.exceptions import ClientError, NoCredentialsError

# Add parent directory to sys.path
sys.path.append(str(Path(__file__).resolve().parent.parent.parent.parent))

from shared.config import AWS_REGION, S3_BUCKET_NAME, S3_OBJECT_KEY, LOCAL_SAMPLE_FILE
from shared.aws_client import get_s3_client


def multipart_upload(local_file: Path, bucket_name: str, object_key: str, chunk_size_mb: int = 5, region: str = None) -> bool:
    """
    Executes a low-level S3 multipart upload for a local file.

    :param local_file: Path object pointing to file.
    :param bucket_name: Target S3 bucket name.
    :param object_key: Target object key.
    :param chunk_size_mb: Size of each chunk in megabytes (minimum 5 MB for AWS S3).
    :param region: AWS Region.
    :return: True if upload succeeded, False otherwise.
    """
    region = region or AWS_REGION
    s3_client = get_s3_client(region_name=region)

    if not local_file.exists():
        print(f"[ERROR] Local file '{local_file}' does not exist.")
        return False

    file_size = local_file.stat().st_size
    chunk_bytes = max(chunk_size_mb * 1024 * 1024, 5 * 1024 * 1024) # Minimum S3 part size is 5MB

    print(f"\n[INFO] Starting Low-Level Multipart Upload for '{local_file.name}' ({file_size} bytes)...")
    print(f"       Destination: s3://{bucket_name}/{object_key}")
    print(f"       Chunk Size:  {chunk_bytes / (1024*1024):.1f} MB")

    upload_id = ""
    parts = []

    try:
        # Step 1: Initiate Multipart Upload
        init_res = s3_client.create_multipart_upload(Bucket=bucket_name, Key=object_key)
        upload_id = init_res["UploadId"]
        print(f"       [Step 1/3] Initiated Multipart Upload. UploadId: {upload_id[:16]}...")

        # Step 2: Read and upload parts sequentially
        part_number = 1
        with open(local_file, "rb") as f:
            while True:
                data = f.read(chunk_bytes)
                if not data:
                    break

                print(f"       [Step 2/3] Uploading Part {part_number} ({len(data)} bytes)...")
                part_res = s3_client.upload_part(
                    Bucket=bucket_name,
                    Key=object_key,
                    PartNumber=part_number,
                    UploadId=upload_id,
                    Body=data
                )
                etag = part_res["ETag"]
                parts.append({"PartNumber": part_number, "ETag": etag})
                print(f"       [Step 2/3] Part {part_number} uploaded. ETag: {etag}")
                part_number += 1

        # Step 3: Complete Multipart Upload
        print(f"       [Step 3/3] Completing Multipart Upload with {len(parts)} part(s)...")
        comp_res = s3_client.complete_multipart_upload(
            Bucket=bucket_name,
            Key=object_key,
            UploadId=upload_id,
            MultipartUpload={"Parts": parts}
        )
        print(f"[SUCCESS] Low-level Multipart Upload completed successfully!")
        print(f"         Location: {comp_res.get('Location', 'N/A')}")
        print(f"         ETag:     {comp_res.get('ETag', 'N/A')}")
        return True

    except Exception as e:
        print(f"[ERROR] Exception during multipart upload: {e}")
        if upload_id:
            print(f"[INFO] Aborting multipart upload ID '{upload_id}'...")
            try:
                s3_client.abort_multipart_upload(Bucket=bucket_name, Key=object_key, UploadId=upload_id)
                print("[INFO] Multipart upload aborted successfully.")
            except Exception as abort_err:
                print(f"[ERROR] Failed to abort multipart upload: {abort_err}")
        return False


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Perform a low-level S3 Multipart Upload.")
    parser.add_argument("--bucket", type=str, default=S3_BUCKET_NAME, help="Target S3 bucket name")
    parser.add_argument("--file", type=str, default=str(LOCAL_SAMPLE_FILE), help="Local file path")
    parser.add_argument("--key", type=str, default="multipart/sample_large.txt", help="Target S3 object key")
    parser.add_argument("--chunk-mb", type=int, default=5, help="Chunk size in MB (min 5MB)")
    parser.add_argument("--region", type=str, default=AWS_REGION, help="AWS Region")

    args = parser.parse_args()

    success = multipart_upload(
        local_file=Path(args.file),
        bucket_name=args.bucket,
        object_key=args.key,
        chunk_size_mb=args.chunk_mb,
        region=args.region
    )
    sys.exit(0 if success else 1)
