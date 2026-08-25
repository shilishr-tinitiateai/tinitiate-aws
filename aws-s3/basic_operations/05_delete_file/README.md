# 🗑️ 05. Delete a File

This directory contains the Python script and AWS CLI commands for **Deleting a File from S3**.

---

## 🐍 How to Run the Python Script

Run this command in your terminal from this folder:

```bash
python delete_file.py
```

### 🖥️ Python Execution Terminal Output Screenshot:
```text
┌──(developer㿠localhost)-[c:\code\aws-s3-and-lmbda-operations\aws-s3\basic_operations\05_delete_file]
└─$ python delete_file.py
🚀 Executing Script: Delete File 'documents/sample.txt' from 'my-local-bucket'...
✅ Deleted object 'documents/sample.txt' from bucket 'my-local-bucket' successfully!
```

---

## 📋 AWS CLI Command Alternative

```bash
aws s3 rm s3://my-local-bucket/sample.txt --endpoint-url http://localhost:4566
```

### 🖥️ AWS CLI Execution Terminal Output Screenshot:
```text
┌──(developer㿠localhost)-[c:\code\aws-s3-and-lmbda-operations]
└─$ aws s3 rm s3://my-local-bucket/documents/sample.txt --endpoint-url http://localhost:4566
delete: s3://my-local-bucket/documents/sample.txt
```
