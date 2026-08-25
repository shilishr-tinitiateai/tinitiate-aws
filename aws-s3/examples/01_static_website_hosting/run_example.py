"""
===============================================================================
EXAMPLE 1 DEPLOYMENT & EXECUTION RUNNER: S3 Static Website Hosting
===============================================================================
Description:
    Creates an S3 bucket, configures it for Static Website Hosting, uploads 
    index.html and error.html with proper MIME headers, and outputs the website 
    access URL.

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
BUCKET_NAME = "my-static-website-example-2026"

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

    # 1. Create S3 Bucket
    try:
        print(f"🪣 Creating S3 bucket '{BUCKET_NAME}'...")
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

    # 2. Configure Website Hosting
    try:
        print("🌐 Configuring S3 Website Configuration (index.html & error.html)...")
        website_config = {
            'IndexDocument': {'Suffix': 'index.html'},
            'ErrorDocument': {'Key': 'error.html'}
        }
        s3_client.put_bucket_website(Bucket=BUCKET_NAME, WebsiteConfiguration=website_config)
        print("✅ Bucket website configuration applied!")
    except Exception as e:
        print(f"⚠️ Note on website configuration: {e}")

    # 3. Upload HTML Files with Content-Type Header
    current_dir = os.path.dirname(__file__)
    files_to_upload = [
        ("index.html", "text/html"),
        ("error.html", "text/html")
    ]

    for file_name, content_type in files_to_upload:
        file_path = os.path.join(current_dir, file_name)
        if os.path.exists(file_path):
            print(f"📄 Uploading '{file_name}' to s3://{BUCKET_NAME}/{file_name}...")
            s3_client.upload_file(
                Filename=file_path,
                Bucket=BUCKET_NAME,
                Key=file_name,
                ExtraArgs={'ContentType': content_type}
            )
            print(f"✅ Uploaded '{file_name}' successfully!")

    # 4. Display Website Endpoint URL
    website_url = f"http://{BUCKET_NAME}.s3-website-{REGION_NAME}.amazonaws.com"
    local_url = f"{ENDPOINT_URL}/{BUCKET_NAME}/index.html"

    print("\n🎉 Static Website Deployment Complete!")
    print(f"🔗 Real AWS Cloud URL:  {website_url}")
    print(f"🔗 Local Emulator URL:   {local_url}")

if __name__ == "__main__":
    main()
