# 🔑 Example 3: Temporary File Sharing with Pre-Signed URLs

Welcome to **Example 3**! This beginner-friendly guide demonstrates how to generate **Pre-Signed URLs** to grant temporary download or upload access to private S3 files without sharing AWS credentials or making buckets public.

---

## 🎯 What Does This Example Do?

1. Uploads a private document (`private_document.pdf`) to a private S3 bucket.
2. Uses Boto3 `generate_presigned_url()` to create a time-limited **GET Download URL** (valid for 15 minutes).
3. Generates a time-limited **PUT Upload URL** allowing external clients (like mobile apps) to upload directly to S3.
4. When the 15-minute timer expires, AWS automatically revokes access to the URL.

---

## 📁 File Structure

* [`private_document.pdf`](file:///c:/code/aws-s3-and-lmbda-operations/aws-s3/examples/03_presigned_url_sharing/private_document.pdf): Sample confidential document file.
* [`run_example.py`](file:///c:/code/aws-s3-and-lmbda-operations/aws-s3/examples/03_presigned_url_sharing/run_example.py): Python Boto3 script generating GET and PUT pre-signed URLs.

---

## 💻 How to Run on ANY Computer (Windows, macOS, Linux)

### Option A: Run via Python Runner Script (Recommended)
```bash
python run_example.py
```

---

### Option B: Run via AWS CLI (Step-by-Step)

#### Step 1: Create Bucket & Upload Private File
```bash
aws s3 mb s3://my-secure-document-sharing-2026 --endpoint-url http://localhost:4566
aws s3 cp private_document.pdf s3://my-secure-document-sharing-2026/confidential/private_document.pdf --endpoint-url http://localhost:4566
```

#### Step 2: Generate Pre-Signed Download URL (Expires in 900 seconds / 15 minutes)
```bash
aws s3 presign s3://my-secure-document-sharing-2026/confidential/private_document.pdf \
  --expires-in 900 \
  --endpoint-url http://localhost:4566
```

---

## ✏️ Changes You Should Make for Real AWS Cloud

1. **Bucket Name**: Replace `my-secure-document-sharing-2026` with your bucket name.
2. **Expiration Time**: Set `--expires-in` to desired duration in seconds (e.g. 300 for 5 mins, 3600 for 1 hour, max 604800 for 7 days).
3. **Remove Local Endpoint**: Omit `--endpoint-url http://localhost:4566` from CLI commands.

---

## 📤 Verified Output Details
```text
📥 Secure GET Download URL:
http://my-secure-document-sharing-2026.s3.amazonaws.com/confidential/private_document.pdf?AWSAccessKeyId=...&Signature=...&Expires=1787680000

📤 Secure PUT Upload URL:
http://my-secure-document-sharing-2026.s3.amazonaws.com/uploads/user_uploaded_file.txt?AWSAccessKeyId=...&Signature=...&Expires=1787680000
```
