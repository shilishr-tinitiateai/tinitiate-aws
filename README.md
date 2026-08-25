# ☁️ AWS Cloud Operations Repository (S3 & Lambda Master Guide)

Welcome to the **AWS Cloud Operations Repository**! This repository is a comprehensive, production-ready, and beginner-friendly master reference guide for **AWS S3 Object Storage** and **AWS Lambda Serverless Compute**. 

Whether you are learning AWS from scratch or building local test pipelines using LocalStack/Floci, every script and command in this repository is designed to execute **without errors** across Windows, macOS, and Linux environments.

---

## 📖 Table of Contents
1. ✨ [Key Repository Features](#1-key-repository-features)
2. 💡 [Core Cloud Architecture Definitions](#2-core-cloud-architecture-definitions)
3. ⚔️ [AWS S3 vs AWS Lambda Comparison Matrix](#3-aws-s3-vs-aws-lambda-comparison-matrix)
4. 📂 [Repository Directory Map](#4-repository-directory-map)
5. 🔌 [Prerequisites & Environment Setup](#5-prerequisites--environment-setup)
6. 🪣 [AWS S3 Basic Operations (01 to 06)](#6-aws-s3-basic-operations)
7. ⚡ [AWS Lambda Basic Operations (01 to 07)](#7-aws-lambda-basic-operations)
8. 🌐 [Real-World Practical Examples (S3 & Lambda)](#8-real-world-practical-examples)
9. 🐍 [Python Code Design & Runner Pattern](#9-python-code-design--runner-pattern)

---

## ✨ 1. Key Repository Features

* 🚀 **100% Cross-Platform & Zero-Error Guarantee**: Built with dynamic relative paths, automatic UTF-8 terminal encoding, and connection exception handling to run seamlessly on Windows (PowerShell), macOS (Zsh/Bash), and Linux (Ubuntu).
* 🔄 **Dual Local & Cloud Environment Support**: Every script and CLI command is configured for local emulator testing (LocalStack / Floci on `http://localhost:4566`) and includes 1-step instructions for real AWS Cloud deployments.
* 📦 **Automated Python Runners (`run_example.py`)**: Includes standalone Python deployment scripts using Boto3 SDK that package code, initiate resources, execute events, and format response outputs automatically.
* 📚 **Standardized Section Banners**: Every Python file adheres to professional sectioning (`MODULE DOCSTRINGS`, `SECTION 1: IMPORTS`, `SECTION 2: CONFIGURATION`, `SECTION 3: FUNCTIONS`, `SECTION 4: ENTRY POINT`).
* 📁 **Modular Self-Contained Folders**: Every operation and example subfolder contains its own dedicated `README.md`, code source, event payloads, and CLI parameter breakdowns.

---

## 💡 2. Core Cloud Architecture Definitions

### 🪣 AWS S3 Definitions
* **Bucket**: A top-level container/vault with a globally unique name across all AWS accounts worldwide (e.g. `s3://my-app-photos-2026`).
* **Object**: The fundamental entity stored in S3, containing raw file data (0 bytes up to 5 TB per file), a key identifier, and metadata.
* **Key**: The unique string path/name assigned to an object within a bucket (e.g. `images/2026/avatar.png`).
* **Metadata**: Key-value pairs attached to an object (e.g. `Content-Type: text/html`, `Cache-Control: max-age=3600`).
* **Server-Side Encryption (SSE-S3)**: Automatic data encryption at rest using AES-256 keys managed by AWS.
* **Pre-Signed URL**: A time-limited secure link allowing external users to download or upload a private file without AWS credentials.

### ⚡ AWS Lambda Definitions
* **Lambda Function**: An event-driven, serverless code microservice that runs without dedicated server management.
* **Lambda Handler**: The primary entrypoint function (`def lambda_handler(event, context)`) executed when triggered.
* **Event (`event`)**: A Python dictionary payload containing data sent by the trigger source (e.g. S3 upload info, HTTP API request, or timer).
* **Context (`context`)**: A runtime metadata object provided by AWS containing execution timeout, function ARN, and remaining time.
* **Trigger**: An AWS event source (S3, API Gateway, EventBridge Cron, DynamoDB) that automatically invokes the Lambda function.
* **Cold Start**: The initial initialization latency when AWS Lambda provisions a container for a newly invoked function.

---

## ⚔️ 3. AWS S3 vs AWS Lambda Comparison Matrix

| Feature | 🪣 AWS S3 (Storage) | ⚡ AWS Lambda (Compute) |
| :--- | :--- | :--- |
| **Primary Job** | Scalable Object Storage Service | Event-Driven Serverless Compute |
| **Data Unit** | Objects (Files + Metadata) in Buckets | Code Functions triggered by Events |
| **Scaling** | Infinite storage capacity automatically | Scales from 0 to thousands of parallel instances |
| **Billing Model** | Pay per GB stored per month | Pay per millisecond of execution time |
| **Primary Operations** | Create Bucket, Upload File, List Content, Download File, Delete File, Delete Bucket | Create Function, Invoke Function, List Functions, Get Details, Update Code, Update Config, Delete Function |

---

## 📂 4. Repository Directory Map

```text
aws-s3-and-lmbda-operations/
│
├── 🪣 aws-s3/                              # AWS S3 Operations Module
│   ├── README.md                           # Master S3 Architecture & Concepts Guide
│   ├── basic_operations/                   # Core S3 Operations (01 - 06)
│   │   ├── 01_create_bucket/               # Create Bucket (boto3 & CLI)
│   │   ├── 02_upload_file/                 # Upload File (boto3 & CLI)
│   │   ├── 03_list_buckets_and_objects/    # List Buckets & Files (boto3 & CLI)
│   │   ├── 04_download_file/               # Download File (boto3 & CLI)
│   │   ├── 05_delete_file/                 # Delete File (boto3 & CLI)
│   │   ├── 06_delete_bucket/               # Delete Bucket (boto3 & CLI)
│   │   └── README.md                       # Master S3 Basic Operations Guide
│   │
│   └── examples/                           # Real-World S3 Practical Examples
│       ├── 01_static_website_hosting/      # Static HTML Website Hosting
│       ├── 02_secure_private_backup/       # Encrypted Database Backup (AES256)
│       ├── 03_presigned_url_sharing/       # Temporary Pre-Signed GET & PUT URLs
│       ├── 04_multipart_large_file_uploader/# Fault-Tolerant Multipart Upload (>100MB)
│       └── README.md                       # Master S3 Examples Index & Guide
│
├── ⚡ lambda-operations/                    # AWS Lambda Operations Module
│   ├── README.md                           # Master Lambda Architecture & Concepts Guide
│   ├── 01_create_function/                 # Create Function (boto3 & CLI)
│   ├── 02_invoke_function/                 # Invoke Function (Synchronous payload execution)
│   ├── 03_list_functions/                  # List All Functions & Metadata
│   ├── 04_get_function/                    # Get Function Details & Download URL
│   ├── 05_update_function_code/            # Update Code (v2 ZIP upload)
│   ├── 06_update_function_configuration/   # Update Config (Timeout, RAM, Env Vars)
│   ├── 07_delete_function/                 # Delete Function & Aliases
│   │
│   └── examples/                           # Real-World Lambda Practical Examples
│       ├── 01_s3_thumbnail_generator/      # Automated S3 File Processing Trigger
│       ├── 02_serverless_api_backend/      # Serverless REST API Backend Endpoint
│       ├── 03_scheduled_cloudwatch_cleaner/# Scheduled Cron Audit & Cleaner Task
│       ├── 04_user_registration_processor/ # User Signup Data Validator & Ingestion
│       └── README.md                       # Master Lambda Examples Index & Guide
│
└── README.md                               # Master Repository Guide (This File)
```

---

## 🔌 5. Prerequisites & Environment Setup

### 1. Python Dependencies
Install required libraries (`boto3`) from your terminal:
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
  AWS Access Key ID [None]: AKIAIOSFODNN7EXAMPLE (Your Real Access Key)
  AWS Secret Access Key [None]: wJalrXUtnFEMI/K7MDENG/EXAMPLE (Your Real Secret Key)
  Default region name [None]: us-east-1
  Default output format [None]: json
  ```

### 3. Terminal Environment Variables
* **Windows (PowerShell)**:
  ```powershell
  $env:AWS_ACCESS_KEY_ID="test"; $env:AWS_SECRET_ACCESS_KEY="test"; $env:AWS_DEFAULT_REGION="us-east-1"; $env:AWS_ENDPOINT_URL="http://localhost:4566"
  ```
* **Linux / macOS (Bash)**:
  ```bash
  export AWS_ACCESS_KEY_ID=test AWS_SECRET_ACCESS_KEY=test AWS_DEFAULT_REGION=us-east-1 AWS_ENDPOINT_URL=http://localhost:4566
  ```

---

## 🪣 6. AWS S3 Basic Operations (01 to 06)

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

## ⚡ 7. AWS Lambda Basic Operations (01 to 07)

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

## 🌟 8. Real-World Practical Examples Index

### A. Real-World AWS S3 Examples ([`aws-s3/examples/`](file:///c:/code/aws-s3-and-lmbda-operations/aws-s3/examples/README.md))

| Example | Scenario | Runner Command | Dedicated Guide |
| :--- | :--- | :--- | :--- |
| **01. Static Website Hosting** | Hosting static HTML/CSS web app on S3 endpoint | `python aws-s3/examples/01_static_website_hosting/run_example.py` | [`01_static_website_hosting/README.md`](file:///c:/code/aws-s3-and-lmbda-operations/aws-s3/examples/01_static_website_hosting/README.md) |
| **02. Secure Encrypted Backup** | Database dumps with AES256 server-side encryption | `python aws-s3/examples/02_secure_private_backup/run_example.py` | [`02_secure_private_backup/README.md`](file:///c:/code/aws-s3-and-lmbda-operations/aws-s3/examples/02_secure_private_backup/README.md) |
| **03. Pre-Signed URL Sharing** | Temporary 15-minute download & upload URLs | `python aws-s3/examples/03_presigned_url_sharing/run_example.py` | [`03_presigned_url_sharing/README.md`](file:///c:/code/aws-s3-and-lmbda-operations/aws-s3/examples/03_presigned_url_sharing/README.md) |
| **04. Multipart Large Uploader** | Chunked, fault-tolerant upload for files > 100MB | `python aws-s3/examples/04_multipart_large_file_uploader/run_example.py` | [`04_multipart_large_file_uploader/README.md`](file:///c:/code/aws-s3-and-lmbda-operations/aws-s3/examples/04_multipart_large_file_uploader/README.md) |

---

### B. Real-World AWS Lambda Examples ([`lambda-operations/examples/`](file:///c:/code/aws-s3-and-lmbda-operations/lambda-operations/examples/README.md))

| Example | Scenario | Runner Command | Dedicated Guide |
| :--- | :--- | :--- | :--- |
| **01. S3 Thumbnail Generator** | Automated S3 upload event processing | `python lambda-operations/examples/01_s3_thumbnail_generator/run_example.py` | [`01_s3_thumbnail_generator/README.md`](file:///c:/code/aws-s3-and-lmbda-operations/lambda-operations/examples/01_s3_thumbnail_generator/README.md) |
| **02. Serverless API Backend** | API Gateway REST endpoint with query parameters | `python lambda-operations/examples/02_serverless_api_backend/run_example.py` | [`02_serverless_api_backend/README.md`](file:///c:/code/aws-s3-and-lmbda-operations/lambda-operations/examples/02_serverless_api_backend/README.md) |
| **03. Scheduled Cron Cleaner** | EventBridge scheduled nightly resource audit | `python lambda-operations/examples/03_scheduled_cloudwatch_cleaner/run_example.py` | [`03_scheduled_cloudwatch_cleaner/README.md`](file:///c:/code/aws-s3-and-lmbda-operations/lambda-operations/examples/03_scheduled_cloudwatch_cleaner/README.md) |
| **04. User Signup Processor** | Input validation and UUID user profile creation | `python lambda-operations/examples/04_user_registration_processor/run_example.py` | [`04_user_registration_processor/README.md`](file:///c:/code/aws-s3-and-lmbda-operations/lambda-operations/examples/04_user_registration_processor/README.md) |

---

## 🐍 9. Python Code Design & Runner Pattern

In every Lambda directory, there are two distinct Python files:

1. **`lambda_function.py` (Worker Code)**:
   * Runs inside the AWS Cloud runtime when an event occurs.
   * Contains `def lambda_handler(event, context):`.

2. **`run_example.py` / `create_function.py` (Deployment Script)**:
   * Runs locally on your computer terminal.
   * Automatically compresses `lambda_function.py` into a `.zip` archive in memory.
   * Connects to AWS via Boto3 and deploys/invokes the function.
   * Configured with **UTF-8 stdout encoding** and **connection timeout handling** to ensure it runs **without errors** on any machine!
