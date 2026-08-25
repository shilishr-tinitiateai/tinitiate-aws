"""
Helper script to generate a 6MB dummy binary data file for S3 Multipart Upload testing.
S3 requires a minimum chunk size of 5MB per part for multipart uploads.
"""
import os

file_path = os.path.join(os.path.dirname(__file__), "large_dataset.bin")
# 6MB size = 6 * 1024 * 1024 bytes
target_size = 6 * 1024 * 1024

if not os.path.exists(file_path):
    print("📦 Generating 6MB sample dataset file for multipart upload...")
    with open(file_path, "wb") as f:
        f.write(b"A" * target_size)
    print(f"✅ Created '{file_path}' (6 MB)")
else:
    print(f"ℹ️ Sample dataset '{file_path}' already exists.")
