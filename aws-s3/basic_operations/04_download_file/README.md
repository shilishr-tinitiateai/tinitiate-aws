# 📥 04. Download a File from S3

This directory contains the Python script and AWS CLI commands for **Downloading a File from S3**.

---

## 🐍 How to Run the Python Script

Run this command in your terminal from this folder:

```bash
python download_file.py
```

### 🖥️ Python Execution Terminal Output Screenshot:
```text
┌──(developer㿠localhost)-[c:\code\aws-s3-and-lmbda-operations\aws-s3\basic_operations\04_download_file]
└─$ python download_file.py
🚀 Executing Script: Download File 'documents/sample.txt' from 'my-local-bucket'...
✅ Downloaded s3://my-local-bucket/documents/sample.txt to 'downloaded_sample.txt' successfully!
```

---

## 📋 AWS CLI Command Alternative

```bash
aws s3 cp s3://my-local-bucket/sample.txt ./downloaded_sample.txt --endpoint-url http://localhost:4566
```

### 🖥️ AWS CLI Execution Terminal Output Screenshot:
```text
┌──(developer㿠localhost)-[c:\code\aws-s3-and-lmbda-operations]
└─$ aws s3 cp s3://my-local-bucket/documents/sample.txt ./downloaded_sample.txt --endpoint-url http://localhost:4566
download: s3://my-local-bucket/documents/sample.txt to ./downloaded_sample.txt
```
