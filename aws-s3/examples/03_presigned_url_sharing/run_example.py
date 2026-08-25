"""
===============================================================================
EXAMPLE 3 DEPLOYMENT & EXECUTION RUNNER: Pre-Signed URL Generator
===============================================================================
Description:
    Uploads a private document to S3 and generates secure, time-limited 
    Pre-Signed GET (download) and PUT (upload) URLs allowing temporary access 
    without granting IAM credentials or making the bucket public.

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
BUCKET_NAME = "my-secure-document-sharing-2026"
FILE_NAME = "private_document.pdf"
S3_OBJECT_KEY = "confidential/private_document.pdf"

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

    # 1. Create Private Bucket
    try:
        print(f"🔒 Creating Private Bucket '{BUCKET_NAME}'...")
        s3_client.create_bucket(Bucket=BUCKET_NAME)
        print("✅ Private Bucket created successfully!")
    except s3_client.exceptions.BucketAlreadyOwnedByYou:
        print(f"ℹ️ Bucket '{BUCKET_NAME}' already exists.")
    except Exception as e:
        if "Could not connect to the endpoint URL" in str(e):
            print(f"⚠️ Endpoint {ENDPOINT_URL} is offline (LocalStack/Floci container not running).")
            print("💡 Start emulator with 'docker run -p 4566:4566 floci/floci' or run against AWS Cloud.")
            return
        else:
            print(f"❌ Error creating bucket: {e}")

    # 2. Upload Private Document
    file_path = os.path.join(os.path.dirname(__file__), FILE_NAME)
    if os.path.exists(file_path):
        print(f"📄 Uploading private file -> s3://{BUCKET_NAME}/{S3_OBJECT_KEY}...")
        s3_client.upload_file(file_path, BUCKET_NAME, S3_OBJECT_KEY)
        print("✅ File uploaded successfully!")

    # 3. Generate Pre-Signed GET (Download) URL (Valid for 900 seconds / 15 minutes)
    try:
        print("🔑 Generating Pre-Signed GET (Download) URL (Expires in 15 minutes)...")
        presigned_get_url = s3_client.generate_presigned_url(
            ClientMethod='get_object',
            Params={'Bucket': BUCKET_NAME, 'Key': S3_OBJECT_KEY},
            ExpiresIn=900
        )
        print("✅ Pre-Signed GET URL generated!")
    except Exception as e:
        presigned_get_url = f"Error: {e}"

    # 4. Generate Pre-Signed PUT (Upload) URL (Valid for 900 seconds / 15 minutes)
    try:
        print("🔑 Generating Pre-Signed PUT (Upload) URL (Expires in 15 minutes)...")
        presigned_put_url = s3_client.generate_presigned_url(
            ClientMethod='put_object',
            Params={'Bucket': BUCKET_NAME, 'Key': 'uploads/user_uploaded_file.txt'},
            ExpiresIn=900
        )
        print("✅ Pre-Signed PUT URL generated!")
    except Exception as e:
        presigned_put_url = f"Error: {e}"

    print("\n🎉 Pre-Signed URL Generation Complete!")
    print("-" * 75)
    print(f"📥 Secure GET Download URL:\n{presigned_get_url}")
    print("-" * 75)
    print(f"📤 Secure PUT Upload URL:\n{presigned_put_url}")
    print("-" * 75)

if __name__ == "__main__":
    main()
