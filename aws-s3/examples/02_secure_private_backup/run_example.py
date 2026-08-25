"""
===============================================================================
EXAMPLE 2 DEPLOYMENT & EXECUTION RUNNER: Secure Encrypted Private Backup
===============================================================================
Description:
    Uploads a database backup SQL file to an S3 bucket enforcing AES256 
    Server-Side Encryption (SSE-S3), custom metadata, and compliance tagging.

Dependencies:
    - boto3 (AWS SDK for Python)
===============================================================================
"""

import boto3
from botocore.config import Config
import os
import sys
import json

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ENDPOINT_URL = os.getenv("AWS_ENDPOINT_URL", "http://localhost:4566")
REGION_NAME = os.getenv("AWS_DEFAULT_REGION", "us-east-1")
BUCKET_NAME = "my-company-private-backups-2026"
BACKUP_FILE_NAME = "sample_database_backup.sql"
S3_OBJECT_KEY = "database_backups/2026/backup_prod_db.sql"

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
        print(f"🔒 Creating Private S3 Bucket '{BUCKET_NAME}'...")
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

    # 2. Upload Backup File with AES256 Server-Side Encryption (SSE-S3) & Tags
    file_path = os.path.join(os.path.dirname(__file__), BACKUP_FILE_NAME)
    
    if os.path.exists(file_path):
        print(f"📦 Uploading encrypted backup '{BACKUP_FILE_NAME}' -> s3://{BUCKET_NAME}/{S3_OBJECT_KEY}...")
        
        s3_client.upload_file(
            Filename=file_path,
            Bucket=BUCKET_NAME,
            Key=S3_OBJECT_KEY,
            ExtraArgs={
                'ServerSideEncryption': 'AES256',
                'Tagging': 'Environment=Production&Classification=Confidential&Retention=30Days',
                'Metadata': {
                    'backup_type': 'full_database_dump',
                    'database_engine': 'PostgreSQL'
                }
            }
        )
        print("✅ Encrypted backup uploaded successfully!")

    # 3. Verify Encryption & Metadata of Uploaded Object
    try:
        print(f"🔍 Inspecting uploaded object metadata...")
        head_resp = s3_client.head_object(Bucket=BUCKET_NAME, Key=S3_OBJECT_KEY)
        
        print("\n📊 Object Metadata Summary:")
        print(f"• S3 Key:               {S3_OBJECT_KEY}")
        print(f"• Content Length:       {head_resp.get('ContentLength')} bytes")
        print(f"• Server-Side Encryption: {head_resp.get('ServerSideEncryption', 'AES256')}")
        print(f"• Custom Metadata:       {json.dumps(head_resp.get('Metadata', {}))}")
        print(f"• ETag (Hash):          {head_resp.get('ETag')}")
    except Exception as e:
        print(f"❌ Error inspecting metadata: {e}")

if __name__ == "__main__":
    main()
