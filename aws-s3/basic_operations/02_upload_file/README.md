# 📤 02. Upload a File

This directory contains the Python script and AWS CLI commands for **Uploading a Local File to S3**.

---

## 🐍 How to Run the Python Script

Run this command in your terminal from this folder:

```bash
python upload_file.py
```

### 🖥️ Python Execution Terminal Output Screenshot:
```text
┌──(developer㿠localhost)-[c:\code\aws-s3-and-lmbda-operations\aws-s3\basic_operations\02_upload_file]
└─$ python upload_file.py
🚀 Executing Script: Upload File 'sample.txt' to 'my-local-bucket'...
📄 Created local sample file: 'sample.txt'
✅ Uploaded 'sample.txt' to s3://my-local-bucket/documents/sample.txt
```

---

## 📋 AWS CLI Command Alternative

```bash
aws s3 cp sample.txt s3://my-local-bucket/sample.txt --endpoint-url http://localhost:4566
```

### 🖥️ AWS CLI Execution Terminal Output Screenshot:
```text
┌──(developer㿠localhost)-[c:\code\aws-s3-and-lmbda-operations]
└─$ aws s3 cp sample.txt s3://my-local-bucket/sample.txt --endpoint-url http://localhost:4566
upload: sample.txt to s3://my-local-bucket/sample.txt
```
