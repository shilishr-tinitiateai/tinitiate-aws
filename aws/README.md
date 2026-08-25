# AWS S3 and Lambda Operations with Python

A comprehensive, production-grade learning and operational engineering repository for **Amazon Simple Storage Service (S3)** and **AWS Lambda** using Python (`boto3`) and the AWS CLI.

---

## 1. Introduction

### What is AWS S3?
**Amazon Simple Storage Service (S3)** is an object storage service offering industry-leading scalability, data availability, security, and performance. Applications use S3 to store unstructured datasets (files, images, videos, backups, logs, data lake archives).

### What is AWS Lambda?
**AWS Lambda** is a serverless, event-driven compute service that lets developers run code without provisioning or managing servers. Lambda automatically executes your Python code in response to events (such as file uploads to S3 buckets, HTTP requests via API Gateway, or CloudWatch timer schedules) and automatically scales compute capacity.

### Why boto3?
**Boto3** is the official AWS Software Development Kit (SDK) for Python. It provides an object-oriented Python interface to programmatically create, configure, and manage AWS cloud resources.

### What This Repository Teaches
This repository provides **31 fully executable, production-tested operation modules** designed with a structured beginner-to-advanced progression. Every operation contains:
- Executive definition and enterprise use case rationale
- Real executable Python code adhering to `boto3` best practices, type hints, and `botocore` error handling
- Standard 17-section documentation explaining line-by-line mechanics, parameter breakdowns, AWS CLI equivalents, console verification steps, error troubleshooting, and security guidance
- Cross-platform portability (Windows, macOS, Linux) using Python `pathlib` and dynamic environment configuration

---

## 2. Technology Stack

- **Core Language**: Python 3.9+ (Python 3.9, 3.10, 3.11, 3.12 supported)
- **AWS SDK**: Boto3 (>= 1.34.0) & Botocore (>= 1.34.0)
- **Cloud Infrastructure**: AWS S3 & AWS Lambda
- **Tooling**: AWS CLI v2, IAM, Amazon CloudWatch Logs, `python-dotenv`
- **Portability**: Native Python `pathlib`, `argparse`, and environment variable configuration

---

## 3. Prerequisites & Verification

Before running operations, ensure your system meets the following requirements:

1. **Python 3.9+** installed on host machine.
2. **AWS Account** with active credentials.
3. **AWS CLI v2** installed.
4. **IAM Permissions** suitable for S3 and Lambda management.

### Verification Commands
Run the following commands in your shell to verify system readiness:

```bash
# Verify Python version:
python --version

# Verify AWS CLI version:
aws --version

# Verify AWS identity & credentials:
aws sts get-caller-identity
```

---

## 4. AWS Credential Configuration

Security is a primary requirement. **NEVER hardcode AWS access keys or secret keys inside Python scripts, `.env` files, or READMEs.**

### Recommended Credential Provider Chain
This repository relies exclusively on standard AWS Credential Provider Chain resolution in `boto3`:

1. Environment variables (`AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `AWS_REGION`).
2. Shared AWS credentials file configured via AWS CLI (`~/.aws/credentials` or `%USERPROFILE%\.aws\credentials`).
3. IAM Role for Amazon EC2 or AWS Lambda execution roles.

### Setting Up Credentials
Run the AWS CLI configuration command:

```bash
aws configure
```

You will be prompted for:
```text
AWS Access Key ID [None]: <YOUR_AWS_ACCESS_KEY_ID>
AWS Secret Access Key [None]: <YOUR_AWS_SECRET_ACCESS_KEY>
Default region name [None]: us-east-1
Default output format [None]: json
```

---

## 5. Repository QuickStart & Installation

### Step 1: Clone Repository
```bash
git clone <repository-url>
cd aws-s3-and-lambda-operations
```

### Step 2: Create & Activate Virtual Environment

#### On Windows (PowerShell / CMD):
```powershell
python -m venv .venv
.venv\Scripts\activate
```

#### On Linux / macOS (Bash / Zsh):
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Configure Environment Variables (Optional)
Copy `.env.example` to `.env` to customize default bucket names or region settings:
```bash
cp .env.example .env
```

---

## 6. Complete Repository Navigation Table

### AWS S3 Operations (`aws-s3/`)

| Tier | # | Operation | Python Script | Documentation |
|---|---|---|---|---|
| **Basic** | 01 | Create Bucket | [`create_bucket.py`](./aws-s3/basic_operations/01_create_bucket/create_bucket.py) | [README](./aws-s3/basic_operations/01_create_bucket/README.md) |
| | 02 | Upload File | [`upload_file.py`](./aws-s3/basic_operations/02_upload_file/upload_file.py) | [README](./aws-s3/basic_operations/02_upload_file/README.md) |
| | 03 | List Buckets & Objects | [`list_buckets_and_objects.py`](./aws-s3/basic_operations/03_list_buckets_and_objects/list_buckets_and_objects.py) | [README](./aws-s3/basic_operations/03_list_buckets_and_objects/README.md) |
| | 04 | Download File | [`download_file.py`](./aws-s3/basic_operations/04_download_file/download_file.py) | [README](./aws-s3/basic_operations/04_download_file/README.md) |
| | 05 | Delete File | [`delete_file.py`](./aws-s3/basic_operations/05_delete_file/delete_file.py) | [README](./aws-s3/basic_operations/05_delete_file/README.md) |
| | 06 | Delete Bucket | [`delete_bucket.py`](./aws-s3/basic_operations/06_delete_bucket/delete_bucket.py) | [README](./aws-s3/basic_operations/06_delete_bucket/README.md) |
| **Intermediate** | 07 | Copy Object | [`copy_object.py`](./aws-s3/intermediate_operations/07_copy_object/copy_object.py) | [README](./aws-s3/intermediate_operations/07_copy_object/README.md) |
| | 08 | Move Object | [`move_object.py`](./aws-s3/intermediate_operations/08_move_object/move_object.py) | [README](./aws-s3/intermediate_operations/08_move_object/README.md) |
| | 09 | Create Logical Folder | [`create_folder.py`](./aws-s3/intermediate_operations/09_create_folder/create_folder.py) | [README](./aws-s3/intermediate_operations/09_create_folder/README.md) |
| | 10 | S3 Object Metadata | [`object_metadata.py`](./aws-s3/intermediate_operations/10_object_metadata/object_metadata.py) | [README](./aws-s3/intermediate_operations/10_object_metadata/README.md) |
| | 11 | Object ACL | [`object_acl.py`](./aws-s3/intermediate_operations/11_object_acl/object_acl.py) | [README](./aws-s3/intermediate_operations/11_object_acl/README.md) |
| | 12 | S3 Presigned URL | [`presigned_url.py`](./aws-s3/intermediate_operations/12_presigned_url/presigned_url.py) | [README](./aws-s3/intermediate_operations/12_presigned_url/README.md) |
| | 13 | S3 Bucket Versioning | [`bucket_versioning.py`](./aws-s3/intermediate_operations/13_bucket_versioning/bucket_versioning.py) | [README](./aws-s3/intermediate_operations/13_bucket_versioning/README.md) |
| | 14 | Default Bucket Encryption | [`bucket_encryption.py`](./aws-s3/intermediate_operations/14_bucket_encryption/bucket_encryption.py) | [README](./aws-s3/intermediate_operations/14_bucket_encryption/README.md) |
| **Advanced** | 15 | Low-Level Multipart Upload | [`multipart_upload.py`](./aws-s3/advanced_operations/15_multipart_upload/multipart_upload.py) | [README](./aws-s3/advanced_operations/15_multipart_upload/README.md) |
| | 16 | S3 List Pagination | [`pagination.py`](./aws-s3/advanced_operations/16_pagination/pagination.py) | [README](./aws-s3/advanced_operations/16_pagination/README.md) |
| | 17 | S3 Select Query | [`s3_select.py`](./aws-s3/advanced_operations/17_s3_select/s3_select.py) | [README](./aws-s3/advanced_operations/17_s3_select/README.md) |
| | 18 | S3 Lifecycle Configuration | [`lifecycle_configuration.py`](./aws-s3/advanced_operations/18_lifecycle_configuration/lifecycle_configuration.py) | [README](./aws-s3/advanced_operations/18_lifecycle_configuration/README.md) |
| | 19 | S3 Bucket Policy | [`bucket_policy.py`](./aws-s3/advanced_operations/19_bucket_policy/bucket_policy.py) | [README](./aws-s3/advanced_operations/19_bucket_policy/README.md) |

---

### AWS Lambda Operations (`aws-lambda/`)

| Tier | # | Operation | Python Script | Documentation |
|---|---|---|---|---|
| **Basic** | 01 | Hello World | [`lambda_function.py`](./aws-lambda/basic_operations/01_hello_world/lambda_function.py) | [README](./aws-lambda/basic_operations/01_hello_world/README.md) |
| | 02 | Event Payload Parsing | [`lambda_function.py`](./aws-lambda/basic_operations/02_lambda_event/lambda_function.py) | [README](./aws-lambda/basic_operations/02_lambda_event/README.md) |
| | 03 | Context Object Inspection | [`lambda_function.py`](./aws-lambda/basic_operations/03_lambda_context/lambda_function.py) | [README](./aws-lambda/basic_operations/03_lambda_context/README.md) |
| | 04 | Environment Variables | [`lambda_function.py`](./aws-lambda/basic_operations/04_environment_variables/lambda_function.py) | [README](./aws-lambda/basic_operations/04_environment_variables/README.md) |
| | 05 | Error Handling | [`lambda_function.py`](./aws-lambda/basic_operations/05_error_handling/lambda_function.py) | [README](./aws-lambda/basic_operations/05_error_handling/README.md) |
| **S3 Integration** | 06 | S3 Event Trigger Notification | [`lambda_function.py`](./aws-lambda/s3_integration/06_s3_trigger/lambda_function.py) | [README](./aws-lambda/s3_integration/06_s3_trigger/README.md) |
| | 07 | S3 File Processing | [`lambda_function.py`](./aws-lambda/s3_integration/07_s3_file_processing/lambda_function.py) | [README](./aws-lambda/s3_integration/07_s3_file_processing/README.md) |
| | 08 | S3 Event Processing Pipeline | [`lambda_function.py`](./aws-lambda/s3_integration/08_s3_event_processing/lambda_function.py) | [README](./aws-lambda/s3_integration/08_s3_event_processing/README.md) |
| **Advanced** | 09 | AWS Lambda Layers | [`lambda_function.py`](./aws-lambda/advanced_operations/09_lambda_layers/lambda_function.py) | [README](./aws-lambda/advanced_operations/09_lambda_layers/README.md) |
| | 10 | IAM Execution Permissions | [`lambda_function.py`](./aws-lambda/advanced_operations/10_lambda_permissions/lambda_function.py) | [README](./aws-lambda/advanced_operations/10_lambda_permissions/README.md) |
| | 11 | Structured CloudWatch Logging | [`lambda_function.py`](./aws-lambda/advanced_operations/11_lambda_logging/lambda_function.py) | [README](./aws-lambda/advanced_operations/11_lambda_logging/README.md) |
| | 12 | Packaging & Automated Deployment | [`deploy_script.py`](./aws-lambda/advanced_operations/12_lambda_deployment/deploy_script.py) | [README](./aws-lambda/advanced_operations/12_lambda_deployment/README.md) |

---

## 7. Shared Modules & Examples

- **Shared Helpers**: [`shared/`](./shared/README.md)
  - `config.py`: Environment configuration & cross-platform `pathlib` paths.
  - `aws_client.py`: Boto3 S3 and Lambda client/resource factory.
- **Example Assets**: [`examples/`](./examples/README.md)
  - `sample.txt`: Plain text asset for upload, download, and copy operations.
  - `sample.json`: Structured JSON asset for S3 Select SQL queries and Lambda ETL.

---

## 8. AWS Cloud Technical Interview Questions & Answers

### Q1: What is the difference between Boto3 Client and Boto3 Resource?
- **Client**: Low-level 1-to-1 mapping with raw AWS HTTP service APIs. Returns standard Python dictionaries containing raw AWS JSON responses.
- **Resource**: Higher-level object-oriented abstraction representing AWS resources (e.g. `s3.Bucket('name')`). Resources manage identifiers, attributes, and actions natively.

### Q2: Why must S3 bucket names be globally unique?
S3 buckets share a global DNS namespace across all AWS accounts worldwide. Bucket names construct the public endpoint URL (e.g. `https://bucket-name.s3.amazonaws.com`).

### Q3: How does AWS S3 handle "folders" if storage is flat?
S3 is a flat key-value object store. "Folders" are visual UI abstractions created by placing slashes (`/`) in object key strings (e.g., `uploads/documents/sample.txt`). Explicit 0-byte objects ending with `/` can also be uploaded as directory placeholders.

### Q4: How does Presigned URL authorization work?
A Presigned URL embeds temporary cryptographic AWS authorization signature query string parameters (`X-Amz-Signature`) into a standard HTTP URL, allowing unauthenticated clients to GET or PUT a specific object for a limited timeframe without exposing IAM credentials.

### Q5: What is the difference between S3 Bucket Versioning and Delete Markers?
When versioning is enabled, overwriting an object creates a new version ID. Deleting an object without specifying a `VersionId` creates a 0-byte **Delete Marker**, hiding the object from normal queries while preserving historical data.

### Q6: What is S3 Select and why does it save costs?
S3 Select filters binary CSV/JSON/Parquet file data directly at the S3 storage layer using ANSI SQL queries before transferring data over the network, reducing network egress bandwidth costs and improving application query speed.

### Q7: What is the minimum part size for S3 Multipart Upload?
Each chunk part in a low-level Multipart Upload must be at least 5 MB (5,242,880 bytes), except for the final part.

### Q8: What are the two parameters passed to an AWS Lambda handler?
1. `event`: JSON dictionary containing trigger payload data.
2. `context`: AWS runtime object providing execution metadata (`aws_request_id`, `function_name`, `get_remaining_time_in_millis()`).

### Q9: How do you handle cold starts in AWS Lambda?
Cold starts occur when AWS provisions a new microVM container environment. They are mitigated using **Provisioned Concurrency**, keeping dependencies small, avoiding unnecessary top-level imports, or increasing allocated memory size.

### Q10: How do Lambda Layers work?
Lambda Layers package shared code dependencies or custom libraries into a `.zip` archive mounted at `/opt/python` inside the Lambda execution container. This reduces function zip sizes and promotes code reuse across serverless microservices.

---

## 9. Repository Automated Validation

To run the automated repository test suite (which validates Python syntax across all 36 scripts, checks Markdown relative links, and audits security):

```bash
python validate_repo.py
```
