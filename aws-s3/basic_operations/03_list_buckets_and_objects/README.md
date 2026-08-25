# 📑 03. List Buckets & Objects

This directory contains the Python script and AWS CLI commands for **Listing S3 Buckets and Objects**.

---

## 🐍 How to Run the Python Script

Run this command in your terminal from this folder:

```bash
python list_buckets_and_objects.py
```

### 🖥️ Python Execution Terminal Output Screenshot:
```text
┌──(developer㿠localhost)-[c:\code\aws-s3-and-lmbda-operations\aws-s3\basic_operations\03_list_buckets_and_objects]
└─$ python list_buckets_and_objects.py
🚀 Executing Script: List Buckets & Objects...
🪣 Total Buckets Found: 1
  - my-local-bucket

📄 Objects inside 'my-local-bucket': 1 item(s)
  - Key: documents/sample.txt | Size: 44 bytes
```

---

## 📋 AWS CLI Commands Alternative

```bash
# 1. List all Buckets:
aws s3 ls --endpoint-url http://localhost:4566

# 2. List Objects inside a Bucket:
aws s3 ls s3://my-local-bucket/ --endpoint-url http://localhost:4566
```

### 🖥️ AWS CLI Execution Terminal Output Screenshot:
```text
┌──(developer㿠localhost)-[c:\code\aws-s3-and-lmbda-operations]
└─$ aws s3 ls s3://my-local-bucket/ --endpoint-url http://localhost:4566
2026-08-25 12:10:15         44 documents/sample.txt
```
