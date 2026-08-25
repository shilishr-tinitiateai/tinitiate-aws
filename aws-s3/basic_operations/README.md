# AWS S3 Basic Operations - Master All-in-One Subdirectory Guide

This guide provides a unified reference for all 6 operation subdirectories inside `aws-s3/basic_operations/`. It explains **how to execute each Python script**, **how to run the corresponding AWS CLI command**, **line-by-line parameter breakdowns**, **what values to edit**, and **terminal output screenshots**.

---

## 📁 1. Master Operation Index

| Directory | Operation | Python Script File | AWS CLI Command |
| :--- | :--- | :--- | :--- |
| **[`01_create_bucket/`](file:///c:/code/aws-s3-and-lmbda-operations/aws-s3/basic_operations/01_create_bucket/README.md)** | Create Bucket | [`create_bucket.py`](file:///c:/code/aws-s3-and-lmbda-operations/aws-s3/basic_operations/01_create_bucket/create_bucket.py) | `aws s3 mb s3://<bucket-name> --endpoint-url http://localhost:4566` |
| **[`02_upload_file/`](file:///c:/code/aws-s3-and-lmbda-operations/aws-s3/basic_operations/02_upload_file/README.md)** | Upload File | [`upload_file.py`](file:///c:/code/aws-s3-and-lmbda-operations/aws-s3/basic_operations/02_upload_file/upload_file.py) | `aws s3 cp <local-file> s3://<bucket-name>/<s3-key> --endpoint-url http://localhost:4566` |
| **[`03_list_buckets_and_objects/`](file:///c:/code/aws-s3-and-lmbda-operations/aws-s3/basic_operations/03_list_buckets_and_objects/README.md)** | List Buckets & Objects | [`list_buckets_and_objects.py`](file:///c:/code/aws-s3-and-lmbda-operations/aws-s3/basic_operations/03_list_buckets_and_objects/list_buckets_and_objects.py) | `aws s3 ls s3://<bucket-name>/ --endpoint-url http://localhost:4566` |
| **[`04_download_file/`](file:///c:/code/aws-s3-and-lmbda-operations/aws-s3/basic_operations/04_download_file/README.md)** | Download File | [`download_file.py`](file:///c:/code/aws-s3-and-lmbda-operations/aws-s3/basic_operations/04_download_file/download_file.py) | `aws s3 cp s3://<bucket-name>/<s3-key> <local-destination> --endpoint-url http://localhost:4566` |
| **[`05_delete_file/`](file:///c:/code/aws-s3-and-lmbda-operations/aws-s3/basic_operations/05_delete_file/README.md)** | Delete File | [`delete_file.py`](file:///c:/code/aws-s3-and-lmbda-operations/aws-s3/basic_operations/05_delete_file/delete_file.py) | `aws s3 rm s3://<bucket-name>/<s3-key> --endpoint-url http://localhost:4566` |
| **[`06_delete_bucket/`](file:///c:/code/aws-s3-and-lmbda-operations/aws-s3/basic_operations/06_delete_bucket/README.md)** | Delete Bucket | [`delete_bucket.py`](file:///c:/code/aws-s3-and-lmbda-operations/aws-s3/basic_operations/06_delete_bucket/delete_bucket.py) | `aws s3 rb s3://<bucket-name> --endpoint-url http://localhost:4566` |

---

## 🛠️ 2. Prerequisites & Local Emulator Setup

### Step A: Install Dependencies
Run this command from the root directory:
```bash
pip install -r requirements.txt
```

### Step B: Start Floci S3 Container (Docker)
Make sure the Floci Docker container is running locally on port `4566`:
```bash
docker run -d --name floci -p 4566:4566 floci/floci:latest
```

### Step C: Set Terminal Credentials (Bypasses AWS Login)
* **Windows (PowerShell)**:
  ```powershell
  $env:AWS_ACCESS_KEY_ID="test"; $env:AWS_SECRET_ACCESS_KEY="test"; $env:AWS_DEFAULT_REGION="us-east-1"
  ```
* **Linux / macOS**:
  ```bash
  export AWS_ACCESS_KEY_ID=test AWS_SECRET_ACCESS_KEY=test AWS_DEFAULT_REGION=us-east-1
  ```

---

## 🔍 3. Detailed Breakdown of Operations & Output Screenshots

Below is the detailed breakdown for every subdirectory, explaining **how to run the script**, **how to run the CLI command**, **parameter editing**, and **terminal output screenshots**.

---

### 🪣 Directory 1: `01_create_bucket/`

#### A. Python Script Execution:
```bash
python 01_create_bucket/create_bucket.py
```

#### B. AWS CLI Command:
```bash
aws s3 mb s3://<bucket-name> --endpoint-url http://localhost:4566
```

#### C. Command Parameter Editing Breakdown:
| Parameter Element | Status | Action Required | Example Value |
| :--- | :--- | :--- | :--- |
| `aws s3 mb` | 🔒 **KEEP SAME** | Never change. Subcommand to create bucket. | `aws s3 mb` |
| `s3://<bucket-name>` | ✏️ **EDIT THIS** | Replace `<bucket-name>` with your custom bucket name. | `s3://my-app-photos-2026` |
| `--endpoint-url http://localhost:4566` | 🔒 **KEEP SAME** | Directs CLI to local Floci container. | `--endpoint-url http://localhost:4566` |

#### 🖥️ D. Terminal Output Screenshots:

* **Python Script Output Screenshot**:
  ```text
  ┌──(developer㿠localhost)-[c:\code\aws-s3-and-lmbda-operations\aws-s3\basic_operations]
  └─$ python 01_create_bucket/create_bucket.py
  🚀 Executing Script: Create Bucket (my-local-bucket)
  ✅ Bucket 'my-local-bucket' created successfully!
  ```

* **AWS CLI Output Screenshot**:
  ```text
  ┌──(developer㿠localhost)-[c:\code\aws-s3-and-lmbda-operations]
  └─$ aws s3 mb s3://my-local-bucket --endpoint-url http://localhost:4566
  make_bucket: my-local-bucket
  ```

---

### 📤 Directory 2: `02_upload_file/`

#### A. Python Script Execution:
```bash
python 02_upload_file/upload_file.py
```

#### B. AWS CLI Command:
```bash
aws s3 cp <local-file-path> s3://<bucket-name>/<s3-key> --endpoint-url http://localhost:4566
```

#### C. Command Parameter Editing Breakdown:
| Parameter Element | Status | Action Required | Example Value |
| :--- | :--- | :--- | :--- |
| `aws s3 cp` | 🔒 **KEEP SAME** | Never change. Subcommand to copy/upload file. | `aws s3 cp` |
| `<local-file-path>` | ✏️ **EDIT THIS** | Replace with local source file path on your disk. | `./sample.txt` or `C:\my-file.jpg` |
| `s3://<bucket-name>/<s3-key>` | ✏️ **EDIT THIS** | Replace `<bucket-name>` and `<s3-key>` target path in S3. | `s3://my-app-photos-2026/images/photo.jpg` |
| `--endpoint-url http://localhost:4566` | 🔒 **KEEP SAME** | Directs CLI to local Floci container. | `--endpoint-url http://localhost:4566` |

#### 🖥️ D. Terminal Output Screenshots:

* **Python Script Output Screenshot**:
  ```text
  ┌──(developer㿠localhost)-[c:\code\aws-s3-and-lmbda-operations\aws-s3\basic_operations]
  └─$ python 02_upload_file/upload_file.py
  🚀 Executing Script: Upload File 'sample.txt' to 'my-local-bucket'...
  📄 Created local sample file: 'sample.txt'
  ✅ Uploaded 'sample.txt' to s3://my-local-bucket/documents/sample.txt
  ```

* **AWS CLI Output Screenshot**:
  ```text
  ┌──(developer㿠localhost)-[c:\code\aws-s3-and-lmbda-operations]
  └─$ aws s3 cp sample.txt s3://my-local-bucket/sample.txt --endpoint-url http://localhost:4566
  upload: sample.txt to s3://my-local-bucket/sample.txt
  ```

---

### 📑 Directory 3: `03_list_buckets_and_objects/`

#### A. Python Script Execution:
```bash
python 03_list_buckets_and_objects/list_buckets_and_objects.py
```

#### B. AWS CLI Commands:
```bash
# List all buckets:
aws s3 ls --endpoint-url http://localhost:4566

# List objects inside a specific bucket:
aws s3 ls s3://<bucket-name>/ --endpoint-url http://localhost:4566
```

#### C. Command Parameter Editing Breakdown:
| Parameter Element | Status | Action Required | Example Value |
| :--- | :--- | :--- | :--- |
| `aws s3 ls` | 🔒 **KEEP SAME** | Never change. Subcommand to list buckets/files. | `aws s3 ls` |
| `s3://<bucket-name>/` | ✏️ **EDIT THIS** | Replace `<bucket-name>` with bucket to inspect. | `s3://my-app-photos-2026/` |
| `--endpoint-url http://localhost:4566` | 🔒 **KEEP SAME** | Directs CLI to local Floci container. | `--endpoint-url http://localhost:4566` |

#### 🖥️ D. Terminal Output Screenshots:

* **Python Script Output Screenshot**:
  ```text
  ┌──(developer㿠localhost)-[c:\code\aws-s3-and-lmbda-operations\aws-s3\basic_operations]
  └─$ python 03_list_buckets_and_objects/list_buckets_and_objects.py
  🚀 Executing Script: List Buckets & Objects...
  🪣 Total Buckets Found: 1
    - my-local-bucket
  📄 Objects inside 'my-local-bucket': 1 item(s)
    - Key: documents/sample.txt | Size: 44 bytes
  ```

* **AWS CLI Output Screenshot**:
  ```text
  ┌──(developer㿠localhost)-[c:\code\aws-s3-and-lmbda-operations]
  └─$ aws s3 ls s3://my-local-bucket/ --endpoint-url http://localhost:4566
  2026-08-25 12:10:15         44 documents/sample.txt
  ```

---

### 📥 Directory 4: `04_download_file/`

#### A. Python Script Execution:
```bash
python 04_download_file/download_file.py
```

#### B. AWS CLI Command:
```bash
aws s3 cp s3://<bucket-name>/<s3-key> <local-destination-path> --endpoint-url http://localhost:4566
```

#### C. Command Parameter Editing Breakdown:
| Parameter Element | Status | Action Required | Example Value |
| :--- | :--- | :--- | :--- |
| `aws s3 cp` | 🔒 **KEEP SAME** | Subcommand for file download. | `aws s3 cp` |
| `s3://<bucket-name>/<s3-key>` | ✏️ **EDIT THIS** | Source object location inside S3. | `s3://my-app-photos-2026/documents/sample.txt` |
| `<local-destination-path>` | ✏️ **EDIT THIS** | Target output file path on your local disk. | `./downloaded_sample.txt` |
| `--endpoint-url http://localhost:4566` | 🔒 **KEEP SAME** | Directs CLI to local Floci container. | `--endpoint-url http://localhost:4566` |

#### 🖥️ D. Terminal Output Screenshots:

* **Python Script Output Screenshot**:
  ```text
  ┌──(developer㿠localhost)-[c:\code\aws-s3-and-lmbda-operations\aws-s3\basic_operations]
  └─$ python 04_download_file/download_file.py
  🚀 Executing Script: Download File 'documents/sample.txt' from 'my-local-bucket'...
  ✅ Downloaded s3://my-local-bucket/documents/sample.txt to 'downloaded_sample.txt' successfully!
  ```

* **AWS CLI Output Screenshot**:
  ```text
  ┌──(developer㿠localhost)-[c:\code\aws-s3-and-lmbda-operations]
  └─$ aws s3 cp s3://my-local-bucket/documents/sample.txt ./downloaded_sample.txt --endpoint-url http://localhost:4566
  download: s3://my-local-bucket/documents/sample.txt to ./downloaded_sample.txt
  ```

---

### 🗑️ Directory 5: `05_delete_file/`

#### A. Python Script Execution:
```bash
python 05_delete_file/delete_file.py
```

#### B. AWS CLI Command:
```bash
aws s3 rm s3://<bucket-name>/<s3-key> --endpoint-url http://localhost:4566
```

#### C. Command Parameter Editing Breakdown:
| Parameter Element | Status | Action Required | Example Value |
| :--- | :--- | :--- | :--- |
| `aws s3 rm` | 🔒 **KEEP SAME** | Subcommand to remove/delete file. | `aws s3 rm` |
| `s3://<bucket-name>/<s3-key>` | ✏️ **EDIT THIS** | Target object key to delete from S3. | `s3://my-app-photos-2026/documents/sample.txt` |
| `--endpoint-url http://localhost:4566` | 🔒 **KEEP SAME** | Directs CLI to local Floci container. | `--endpoint-url http://localhost:4566` |

#### 🖥️ D. Terminal Output Screenshots:

* **Python Script Output Screenshot**:
  ```text
  ┌──(developer㿠localhost)-[c:\code\aws-s3-and-lmbda-operations\aws-s3\basic_operations]
  └─$ python 05_delete_file/delete_file.py
  🚀 Executing Script: Delete File 'documents/sample.txt' from 'my-local-bucket'...
  ✅ Deleted object 'documents/sample.txt' from bucket 'my-local-bucket' successfully!
  ```

* **AWS CLI Output Screenshot**:
  ```text
  ┌──(developer㿠localhost)-[c:\code\aws-s3-and-lmbda-operations]
  └─$ aws s3 rm s3://my-local-bucket/documents/sample.txt --endpoint-url http://localhost:4566
  delete: s3://my-local-bucket/documents/sample.txt
  ```

---

### 💥 Directory 6: `06_delete_bucket/`

#### A. Python Script Execution:
```bash
python 06_delete_bucket/delete_bucket.py
```

#### B. AWS CLI Command:
```bash
aws s3 rb s3://<bucket-name> --endpoint-url http://localhost:4566
```

#### C. Command Parameter Editing Breakdown:
| Parameter Element | Status | Action Required | Example Value |
| :--- | :--- | :--- | :--- |
| `aws s3 rb` | 🔒 **KEEP SAME** | Subcommand to remove/delete empty bucket. | `aws s3 rb` |
| `s3://<bucket-name>` | ✏️ **EDIT THIS** | Target empty bucket container to delete. | `s3://my-app-photos-2026` |
| `--endpoint-url http://localhost:4566` | 🔒 **KEEP SAME** | Directs CLI to local Floci container. | `--endpoint-url http://localhost:4566` |

#### 🖥️ D. Terminal Output Screenshots:

* **Python Script Output Screenshot**:
  ```text
  ┌──(developer㿠localhost)-[c:\code\aws-s3-and-lmbda-operations\aws-s3\basic_operations]
  └─$ python 06_delete_bucket/delete_bucket.py
  🚀 Executing Script: Delete Bucket 'my-local-bucket'...
  ✅ Bucket 'my-local-bucket' deleted successfully!
  ```

* **AWS CLI Output Screenshot**:
  ```text
  ┌──(developer㿠localhost)-[c:\code\aws-s3-and-lmbda-operations]
  └─$ aws s3 rb s3://my-local-bucket --endpoint-url http://localhost:4566
  remove_bucket: my-local-bucket
  ```
