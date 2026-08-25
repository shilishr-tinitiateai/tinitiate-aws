"""
===============================================================================
EXAMPLE 4 DEPLOYMENT & EXECUTION RUNNER: Multipart Large File Uploader
===============================================================================
Description:
    Demonstrates uploading large files in chunks/parts using the low-level S3 
    Multipart Upload API (`create_multipart_upload`, `upload_part`, 
    `complete_multipart_upload`). Ideal for files > 100MB to enable fault tolerance 
    and parallel transfers.

Dependencies:
    - boto3 (AWS SDK for Python)
===============================================================================
"""

import boto3
from botocore.config import Config
import os
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ENDPOINT_URL = os.getenv("AWS_ENDPOINT_URL", "http://localhost:4566")
REGION_NAME = os.getenv("AWS_DEFAULT_REGION", "us-east-1")
BUCKET_NAME = "my-large-data-lake-2026"
FILE_NAME = "large_dataset.bin"
S3_OBJECT_KEY = "datasets/large_dataset.bin"

BOTO_CONFIG = Config(connect_timeout=3, read_timeout=3, retries={'max_attempts': 1})

def main():
    print(f"🚀 Initializing AWS S3 Client (Endpoint: {ENDPOINT_URL})...")
    
    s3_client = boto3.client(
        "s3",
        region_name=REGION_NAME,
        endpoint_url=ENDPOINT_URL,
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID", "test"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY", "test"),
        config=BOTO_CONFIG
    )

    # 1. Ensure 6MB Sample File Exists
    file_path = os.path.join(os.path.dirname(__file__), FILE_NAME)
    if not os.path.exists(file_path):
        import generate_sample_data
        generate_sample_data.main() if hasattr(generate_sample_data, "main") else None

    # 2. Create Bucket
    try:
        print(f"🪣 Creating Bucket '{BUCKET_NAME}'...")
        s3_client.create_bucket(Bucket=BUCKET_NAME)
        print("✅ Bucket created successfully!")
    except s3_client.exceptions.BucketAlreadyOwnedByYou:
        print(f"ℹ️ Bucket '{BUCKET_NAME}' already exists.")
    except Exception as e:
        if "Could not connect to the endpoint URL" in str(e):
            print(f"⚠️ Endpoint {ENDPOINT_URL} is offline (LocalStack/Floci container not running).")
            print("💡 Start emulator with 'docker run -p 4566:4566 floci/floci' or run against AWS Cloud.")
            return
        else:
            print(f"❌ Error creating bucket: {e}")

    # 3. Initiate Multipart Upload
    upload_id = None
    try:
        print(f"🧩 Initiating Multipart Upload for 's3://{BUCKET_NAME}/{S3_OBJECT_KEY}'...")
        mp_init = s3_client.create_multipart_upload(Bucket=BUCKET_NAME, Key=S3_OBJECT_KEY)
        upload_id = mp_init['UploadId']
        print(f"✅ Multipart Upload Initiated! Upload ID: {upload_id[:30]}...")

        # 4. Upload File Parts in 5MB Chunks
        chunk_size = 5 * 1024 * 1024  # 5 MB S3 minimum part size
        parts = []
        part_number = 1

        with open(file_path, "rb") as f:
            while True:
                data = f.read(chunk_size)
                if not data:
                    break
                
                print(f"📤 Uploading Part {part_number} ({len(data)} bytes)...")
                part_resp = s3_client.upload_part(
                    Bucket=BUCKET_NAME,
                    Key=S3_OBJECT_KEY,
                    UploadId=upload_id,
                    PartNumber=part_number,
                    Body=data
                )
                parts.append({
                    'PartNumber': part_number,
                    'ETag': part_resp['ETag']
                })
                print(f"  └─ Part {part_number} uploaded! ETag: {part_resp['ETag']}")
                part_number += 1

        # 5. Complete Multipart Upload
        print(f"🏁 Completing Multipart Upload ({len(parts)} parts total)...")
        s3_client.complete_multipart_upload(
            Bucket=BUCKET_NAME,
            Key=S3_OBJECT_KEY,
            UploadId=upload_id,
            MultipartUpload={'Parts': parts}
        )
        print("🎉 Multipart Upload Completed Successfully!")

    except Exception as e:
        print(f"❌ Error during Multipart Upload: {e}")
        if upload_id:
            print("🧹 Aborting failed multipart upload...")
            s3_client.abort_multipart_upload(Bucket=BUCKET_NAME, Key=S3_OBJECT_KEY, UploadId=upload_id)

if __name__ == "__main__":
    main()
