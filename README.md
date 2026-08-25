# ☁️ AWS Cloud Operations Repository (S3 & Lambda)

Welcome to the **AWS Cloud Operations Repository**! This repository is a comprehensive, production-ready, and beginner-friendly reference for mastering **AWS S3 Object Storage** and **AWS Lambda Serverless Compute**. 

Whether you are learning AWS from scratch or building local test pipelines using LocalStack/Floci, every script and command in this repository is designed to execute **without errors** across Windows, macOS, and Linux environments.

---

## 📂 Repository Directory Map

```text
aws-s3-and-lmbda-operations/
│
├── 🪣 aws-s3/                              # AWS S3 Operations Module
│   ├── README.md                           # Master S3 Architecture & Concepts Guide
│   └── basic_operations/                   # S3 Basic Operations (01 - 06)
│       ├── 01_create_bucket/               # Python & CLI for Bucket Creation
│       ├── 02_upload_file/                 # Python & CLI for File Uploads
│       ├── 03_list_buckets_and_objects/    # Python & CLI for Listing Content
│       ├── 04_download_file/               # Python & CLI for File Downloads
│       ├── 05_delete_file/                 # Python & CLI for File Deletion
│       ├── 06_delete_bucket/               # Python & CLI for Bucket Deletion
│       └── README.md                       # Complete All-in-One S3 Execution Guide
│
├── ⚡ lambda-operations/                    # AWS Lambda Operations Module
│   ├── README.md                           # Master Lambda Architecture & Concepts Guide
│   ├── 01_create_function/                 # Create Function (boto3 & CLI)
│   ├── 02_invoke_function/                 # Invoke Function (Synchronous payload execution)
│   ├── 03_list_functions/                  # List All Functions & Metadata
│   ├── 04_get_function/                    # Get Function Details & Download URL
│   ├── 05_update_function_code/            # Update Code (v2 ZIP upload)
│   ├── 06_update_function_configuration/   # Update Config (Timeout, RAM, Env Vars)
│   └── 07_delete_function/                 # Delete Function & Aliases
│
└── README.md                               # Root Master Repository Guide (This File)
```

---

## ⚡ 1. AWS S3 vs AWS Lambda Overview

| AWS Service | Core Purpose | Data Unit | Primary Operations |
| :--- | :--- | :--- | :--- |
| **🪣 AWS S3** | Scalable Object Storage Service | Objects (Files + Metadata) in Buckets | Create Bucket, Upload File, List Objects, Download File, Delete File, Delete Bucket |
| **⚡ AWS Lambda** | Event-Driven Serverless Compute | Code Functions triggered by Events | Create Function, Invoke Function, List Functions, Get Details, Update Code, Update Config, Delete Function |

---

## 🔌 2. Prerequisites & Environment Setup

### 1. Python Dependencies
Install all required libraries (e.g. `boto3`) from your terminal:
```bash
pip install boto3
```

### 2. Configure AWS CLI Prompts (`aws configure`)
Run `aws configure` in your terminal and respond as follows:

* **For Free Local Emulation (LocalStack / Floci)**:
  ```text
  AWS Access Key ID [None]: test
  AWS Secret Access Key [None]: test
  Default region name [None]: us-east-1
  Default output format [None]: json
  ```

* **For Real AWS Cloud Account**:
  ```text
  AWS Access Key ID [None]: <YOUR_REAL_AWS_ACCESS_KEY>
  AWS Secret Access Key [None]: <YOUR_REAL_AWS_SECRET_KEY>
  Default region name [None]: us-east-1
  Default output format [None]: json
  ```

---

## 🪣 3. AWS S3 Operations Quick Summary

Detailed documentation for each S3 operation is available in [`aws-s3/README.md`](file:///c:/code/aws-s3-and-lmbda-operations/aws-s3/README.md) and [`aws-s3/basic_operations/README.md`](file:///c:/code/aws-s3-and-lmbda-operations/aws-s3/basic_operations/README.md).

| # | Operation | Folder Link | AWS CLI Command (Local Emulator) | Real AWS Cloud Command |
| :-: | :--- | :--- | :--- | :--- |
| **01** | **Create Bucket** | [`01_create_bucket`](file:///c:/code/aws-s3-and-lmbda-operations/aws-s3/basic_operations/01_create_bucket/README.md) | `aws s3 mb s3://my-bucket --endpoint-url http://localhost:4566` | `aws s3 mb s3://my-bucket` |
| **02** | **Upload File** | [`02_upload_file`](file:///c:/code/aws-s3-and-lmbda-operations/aws-s3/basic_operations/02_upload_file/README.md) | `aws s3 cp sample.txt s3://my-bucket/sample.txt --endpoint-url http://localhost:4566` | `aws s3 cp sample.txt s3://my-bucket/sample.txt` |
| **03** | **List Buckets & Objects** | [`03_list_buckets_and_objects`](file:///c:/code/aws-s3-and-lmbda-operations/aws-s3/basic_operations/03_list_buckets_and_objects/README.md) | `aws s3 ls s3://my-bucket/ --endpoint-url http://localhost:4566` | `aws s3 ls s3://my-bucket/` |
| **04** | **Download File** | [`04_download_file`](file:///c:/code/aws-s3-and-lmbda-operations/aws-s3/basic_operations/04_download_file/README.md) | `aws s3 cp s3://my-bucket/sample.txt downloaded.txt --endpoint-url http://localhost:4566` | `aws s3 cp s3://my-bucket/sample.txt downloaded.txt` |
| **05** | **Delete File** | [`05_delete_file`](file:///c:/code/aws-s3-and-lmbda-operations/aws-s3/basic_operations/05_delete_file/README.md) | `aws s3 rm s3://my-bucket/sample.txt --endpoint-url http://localhost:4566` | `aws s3 rm s3://my-bucket/sample.txt` |
| **06** | **Delete Bucket** | [`06_delete_bucket`](file:///c:/code/aws-s3-and-lmbda-operations/aws-s3/basic_operations/06_delete_bucket/README.md) | `aws s3 rb s3://my-bucket --endpoint-url http://localhost:4566` | `aws s3 rb s3://my-bucket` |

---

## ⚡ 4. AWS Lambda Operations Quick Summary

Detailed documentation for each Lambda operation is available in [`lambda-operations/README.md`](file:///c:/code/aws-s3-and-lmbda-operations/lambda-operations/README.md).

| # | Operation | Folder Link | AWS CLI Command (Local Emulator) | Primary Output |
| :-: | :--- | :--- | :--- | :--- |
| **01** | **Create Function** | [`01_create_function`](file:///c:/code/aws-s3-and-lmbda-operations/lambda-operations/01_create_function/README.md) | `aws lambda create-function --function-name my-first-lambda --runtime python3.12 --role arn:aws:iam::123456789012:role/lambda-role --handler lambda_function.lambda_handler --zip-file fileb://function.zip --endpoint-url http://localhost:4566` | Function Metadata JSON (`Active` state) |
| **02** | **Invoke Function** | [`02_invoke_function`](file:///c:/code/aws-s3-and-lmbda-operations/lambda-operations/02_invoke_function/README.md) | `aws lambda invoke --function-name my-first-lambda --payload file://payload.json --cli-binary-format raw-in-base64-out response.json --endpoint-url http://localhost:4566` | Status `200` + saved `response.json` |
| **03** | **List Functions** | [`03_list_functions`](file:///c:/code/aws-s3-and-lmbda-operations/lambda-operations/03_list_functions/README.md) | `aws lambda list-functions --output table --endpoint-url http://localhost:4566` | Array list of function metadata |
| **04** | **Get Function** | [`04_get_function`](file:///c:/code/aws-s3-and-lmbda-operations/lambda-operations/04_get_function/README.md) | `aws lambda get-function --function-name my-first-lambda --endpoint-url http://localhost:4566` | Config JSON + S3 Download URL |
| **05** | **Update Code** | [`05_update_function_code`](file:///c:/code/aws-s3-and-lmbda-operations/lambda-operations/05_update_function_code/README.md) | `aws lambda update-function-code --function-name my-first-lambda --zip-file fileb://v2_code.zip --publish --endpoint-url http://localhost:4566` | Updated SHA256 & version number |
| **06** | **Update Config** | [`06_update_function_configuration`](file:///c:/code/aws-s3-and-lmbda-operations/lambda-operations/06_update_function_configuration/README.md) | `aws lambda update-function-configuration --function-name my-first-lambda --timeout 30 --memory-size 256 --endpoint-url http://localhost:4566` | Updated Configuration JSON |
| **07** | **Delete Function** | [`07_delete_function`](file:///c:/code/aws-s3-and-lmbda-operations/lambda-operations/07_delete_function/README.md) | `aws lambda delete-function --function-name my-first-lambda --endpoint-url http://localhost:4566` | HTTP Status `204` (No Content) |

---

## 🎯 5. Zero-Error Guarantee & Cross-Platform Support

Every script in this repository includes:
1. **Dynamic Path Resolution**: Avoids hardcoded Windows/Linux forward-slash and backslash path issues.
2. **Standardized Section Banners**: Every script starts with docstrings, imports, configuration constants, main function, and execution entrypoint (`if __name__ == "__main__": main()`).
3. **Robust Exception Handling**: Catches missing files, duplicate resource conflicts, and connection timeouts gracefully.
4. **Tested Command Execution**: All CLI commands include parameter breakdowns and instructions for converting from LocalStack testing to real AWS Cloud deployments.
