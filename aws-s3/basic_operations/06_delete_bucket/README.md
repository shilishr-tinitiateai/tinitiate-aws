# 💥 06. Delete a Bucket

This directory contains the Python script and AWS CLI commands for **Deleting an Empty S3 Bucket**.

---

## 🐍 How to Run the Python Script

Run this command in your terminal from this folder:

```bash
python delete_bucket.py
```

### 🖥️ Python Execution Terminal Output Screenshot:
```text
┌──(developer㿠localhost)-[c:\code\aws-s3-and-lmbda-operations\aws-s3\basic_operations\06_delete_bucket]
└─$ python delete_bucket.py
🚀 Executing Script: Delete Bucket 'my-local-bucket'...
✅ Bucket 'my-local-bucket' deleted successfully!
```

---

## 📋 AWS CLI Command Alternative

```bash
aws s3 rb s3://my-local-bucket --endpoint-url http://localhost:4566
```

### 🖥️ AWS CLI Execution Terminal Output Screenshot:
```text
┌──(developer㿠localhost)-[c:\code\aws-s3-and-lmbda-operations]
└─$ aws s3 rb s3://my-local-bucket --endpoint-url http://localhost:4566
remove_bucket: my-local-bucket
```
