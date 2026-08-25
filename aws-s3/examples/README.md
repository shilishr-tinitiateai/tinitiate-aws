# 🪣 AWS S3 Operations - Real-World Beginner Examples

Welcome to the **AWS S3 Real-World Examples Directory**! This folder contains 4 complete, production-ready, beginner-friendly S3 application examples.

---

## 📁 Examples Directory Index

| Example Folder | Application Scenario | Key AWS S3 Feature | Link to Guide |
| :--- | :--- | :--- | :--- |
| **`01_static_website_hosting/`** | Hosting a Static Website | Bucket Website Hosting Configuration (`index.html` & `error.html`), Content-Type headers | [`01_static_website_hosting/README.md`](file:///c:/code/aws-s3-and-lmbda-operations/aws-s3/examples/01_static_website_hosting/README.md) |
| **`02_secure_private_backup/`** | Automated Private Database Backup | Server-Side Encryption (AES256 SSE-S3), custom metadata & retention tagging | [`02_secure_private_backup/README.md`](file:///c:/code/aws-s3-and-lmbda-operations/aws-s3/examples/02_secure_private_backup/README.md) |
| **`03_presigned_url_sharing/`** | Temporary Time-Limited File Sharing | Pre-Signed GET & PUT URLs (valid for 15 minutes without public bucket access) | [`03_presigned_url_sharing/README.md`](file:///c:/code/aws-s3-and-lmbda-operations/aws-s3/examples/03_presigned_url_sharing/README.md) |
| **`04_multipart_large_file_uploader/`** | Fault-Tolerant Large File Transfer | Multipart Upload API (`create`, `upload_part`, `complete`) for multi-GB uploads | [`04_multipart_large_file_uploader/README.md`](file:///c:/code/aws-s3-and-lmbda-operations/aws-s3/examples/04_multipart_large_file_uploader/README.md) |

---

## ⚡ Quick Execution Guide (Run Any Example on Any Computer)

Every example folder includes an automated Python runner (`run_example.py`) that creates buckets, configures features, uploads sample datasets, and prints formatted output.

### Run Example 1 (Static Website Hosting):
```bash
python aws-s3/examples/01_static_website_hosting/run_example.py
```

### Run Example 2 (Encrypted Private Backup):
```bash
python aws-s3/examples/02_secure_private_backup/run_example.py
```

### Run Example 3 (Pre-Signed URL File Sharing):
```bash
python aws-s3/examples/03_presigned_url_sharing/run_example.py
```

### Run Example 4 (Fault-Tolerant Multipart Uploader):
```bash
python aws-s3/examples/04_multipart_large_file_uploader/run_example.py
```

---

## 🌐 Cross-System & Cross-Platform Support

* **Local Emulator (Floci/LocalStack)**: Set environment variable `AWS_ENDPOINT_URL=http://localhost:4566`.
* **Real AWS Cloud**: Unset `AWS_ENDPOINT_URL` or remove `--endpoint-url http://localhost:4566` from CLI commands.
* **OS Support**: Windows (PowerShell), macOS (Zsh/Bash), Linux (Ubuntu).
