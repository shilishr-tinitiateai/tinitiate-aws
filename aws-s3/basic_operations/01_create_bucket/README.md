# 🪣 01. Create a Bucket

This directory contains the Python script and AWS CLI commands for **Creating an S3 Bucket**.

---

## 🐍 How to Run the Python Script

Run this command in your terminal from this folder:

```bash
python create_bucket.py
```

### 🖥️ Python Execution Terminal Output Screenshot:
```text
┌──(developer㿠localhost)-[c:\code\aws-s3-and-lmbda-operations\aws-s3\basic_operations\01_create_bucket]
└─$ python create_bucket.py
🚀 Executing Script: Create Bucket (my-local-bucket)
✅ Bucket 'my-local-bucket' created successfully!
```

---

## 📋 AWS CLI Command Alternative

```bash
aws s3 mb s3://my-local-bucket --endpoint-url http://localhost:4566
```

### 🖥️ AWS CLI Execution Terminal Output Screenshot:
```text
┌──(developer㿠localhost)-[c:\code\aws-s3-and-lmbda-operations]
└─$ aws s3 mb s3://my-local-bucket --endpoint-url http://localhost:4566
make_bucket: my-local-bucket
```
