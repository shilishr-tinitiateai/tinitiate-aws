# ⚡ AWS Lambda Operations (Comprehensive Guide & Workflow Repository)

Welcome to the **AWS Lambda Operations** master reference guide. This repository contains complete, modular, ready-to-run Python automation scripts and AWS CLI commands for managing the full lifecycle of AWS Lambda functions.

---

## ⚡ 1. What is AWS Lambda?

**AWS Lambda** is an event-driven serverless compute service that runs code in response to events (e.g., S3 object uploads, HTTP requests via API Gateway, CloudWatch timers) automatically managing compute resources.

---

## 🔌 2. Environment Setup & LocalStack Configurations

### 1. AWS Credentials Configuration (`aws configure`)
Run `aws configure` in your terminal and enter:
* **AWS Access Key ID**: `test` *(for LocalStack)* or your real AWS Access Key.
* **AWS Secret Access Key**: `test` *(for LocalStack)* or your real AWS Secret Key.
* **Default region name**: `us-east-1`
* **Default output format**: `json`

### 2. Terminal Environment Variables
* **Windows (PowerShell)**:
  ```powershell
  $env:AWS_ACCESS_KEY_ID="test"
  $env:AWS_SECRET_ACCESS_KEY="test"
  $env:AWS_DEFAULT_REGION="us-east-1"
  $env:AWS_ENDPOINT_URL="http://localhost:4566"
  ```
* **Linux / macOS (Bash)**:
  ```bash
  export AWS_ACCESS_KEY_ID=test
  export AWS_SECRET_ACCESS_KEY=test
  export AWS_DEFAULT_REGION=us-east-1
  export AWS_ENDPOINT_URL=http://localhost:4566
  ```

> 💡 **LocalStack vs AWS Cloud Deployment Rule**:
> * **Local Emulator (LocalStack/Floci)**: Include `--endpoint-url http://localhost:4566` in CLI commands.
> * **Real AWS Cloud**: **Remove** `--endpoint-url http://localhost:4566` completely.

---

## 📂 3. Repository Directory Structure

```text
lambda-operations/
│
├── 01_create_function/              # Create Lambda Function
│   ├── lambda_function.py            # Lambda handler python source code
│   ├── create_function.py            # Python Boto3 script to package & deploy function
│   └── README.md                     # Dedicated guide for create-function
│
├── 02_invoke_function/              # Invoke Lambda Function
│   ├── payload.json                  # Sample input JSON payload file
│   ├── invoke_function.py            # Python Boto3 script to invoke Lambda function
│   └── README.md                     # Dedicated guide for invoke
│
├── 03_list_functions/               # List Lambda Functions
│   ├── list_functions.py             # Python Boto3 script to list all functions
│   └── README.md                     # Dedicated guide for list-functions
│
├── 04_get_function/                 # Get Lambda Function Details
│   ├── get_function.py               # Python Boto3 script to fetch function metadata & zip URL
│   └── README.md                     # Dedicated guide for get-function
│
├── 05_update_function_code/         # Update Function Code
│   ├── lambda_function_v2.py         # Updated Lambda handler code (v2)
│   ├── update_function_code.py       # Python Boto3 script to upload new ZIP
│   └── README.md                     # Dedicated guide for update-function-code
│
├── 06_update_function_configuration/# Update Function Configuration
│   ├── update_function_config.py     # Python Boto3 script to update timeout, memory & env vars
│   └── README.md                     # Dedicated guide for update-function-configuration
│
├── 07_delete_function/              # Delete Lambda Function
│   ├── delete_function.py            # Python Boto3 script to delete function
│   └── README.md                     # Dedicated guide for delete-function
│
├── examples/                        # Real-World Beginner Examples
│   ├── 01_s3_thumbnail_generator/    # Automated S3 file processing trigger
│   ├── 02_serverless_api_backend/    # Serverless REST API backend endpoint
│   ├── 03_scheduled_cloudwatch_cleaner/# Scheduled cron audit & cleaner task
│   ├── 04_user_registration_processor/# User signup data validator & ingestion
│   └── README.md                     # Master Examples Directory Index & Guide
│
└── README.md                        # Master Documentation (This File)
```

---

## 🛠️ 4. Master Operations Summary Table

| # | Operation | Folder Link | Primary CLI Command | Primary Input | Expected Output |
| :-: | :--- | :--- | :--- | :--- | :--- |
| **01** | **Create Function** | [`01_create_function`](file:///c:/code/aws-s3-and-lmbda-operations/lambda-operations/01_create_function/README.md) | `aws lambda create-function` | `function.zip` package + IAM Role ARN | Function Metadata JSON (`Active` state) |
| **02** | **Invoke Function** | [`02_invoke_function`](file:///c:/code/aws-s3-and-lmbda-operations/lambda-operations/02_invoke_function/README.md) | `aws lambda invoke` | Input payload JSON / `payload.json` | Status `200` + saved `response.json` |
| **03** | **List Functions** | [`03_list_functions`](file:///c:/code/aws-s3-and-lmbda-operations/lambda-operations/03_list_functions/README.md) | `aws lambda list-functions` | AWS Region / Optional filters | Array list of function metadata |
| **04** | **Get Function** | [`04_get_function`](file:///c:/code/aws-s3-and-lmbda-operations/lambda-operations/04_get_function/README.md) | `aws lambda get-function` | Function Name / ARN | Detailed Config JSON + S3 Download URL |
| **05** | **Update Code** | [`05_update_function_code`](file:///c:/code/aws-s3-and-lmbda-operations/lambda-operations/05_update_function_code/README.md) | `aws lambda update-function-code` | Updated `v2_code.zip` package | Updated code size, SHA256 & version |
| **06** | **Update Config** | [`06_update_function_configuration`](file:///c:/code/aws-s3-and-lmbda-operations/lambda-operations/06_update_function_configuration/README.md) | `aws lambda update-function-configuration` | Timeout, Memory Size, Env variables | Updated Configuration JSON |
| **07** | **Delete Function** | [`07_delete_function`](file:///c:/code/aws-s3-and-lmbda-operations/lambda-operations/07_delete_function/README.md) | `aws lambda delete-function` | Function Name / Alias / Version | HTTP Status `204` (No Content) |

---

## 📜 5. Detailed Breakdown of Operations & Commands

### 1️⃣ Create Lambda Function (`01_create_function`)
* **Purpose**: Deploys a new Lambda function from a `.zip` deployment package containing code and handlers.
* **AWS CLI Command**:
  ```bash
  aws lambda create-function \
    --function-name my-first-lambda \
    --runtime python3.12 \
    --role arn:aws:iam::123456789012:role/lambda-execution-role \
    --handler lambda_function.lambda_handler \
    --zip-file fileb://function.zip \
    --endpoint-url http://localhost:4566
  ```
* **Command Breakdown**:
  * `--function-name`: Name assigned to function resource.
  * `--runtime`: Language runtime (`python3.12`, `nodejs20.x`).
  * `--role`: IAM Execution Role ARN with CloudWatch logging policies.
  * `--handler`: Point to module and entry function (`<file>.<function>`).
  * `--zip-file fileb://...`: Raw binary upload of code archive.
* **Modifications to Make**: Change `--function-name`, `--role`, `--zip-file`, and remove `--endpoint-url` for AWS Cloud.
* **Input**: `function.zip` with `lambda_function.py`.
* **Output**: JSON containing `FunctionName`, `FunctionArn`, `State: "Active"`.

---

### 2️⃣ Invoke Lambda Function (`02_invoke_function`)
* **Purpose**: Synchronously executes deployed Lambda function with JSON payload.
* **AWS CLI Command**:
  ```bash
  aws lambda invoke \
    --function-name my-first-lambda \
    --payload file://payload.json \
    --cli-binary-format raw-in-base64-out \
    response.json \
    --endpoint-url http://localhost:4566
  ```
* **Command Breakdown**:
  * `--payload file://payload.json`: Path to input JSON payload.
  * `--cli-binary-format raw-in-base64-out`: Required AWS CLI v2 flag for unencoded raw strings.
  * `response.json`: Output filename to store function return body.
* **Modifications to Make**: Update function name, input payload file, and output destination.
* **Input**: JSON dictionary `{ "name": "Alice Developer" }`.
* **Output**: Terminal status `{ "StatusCode": 200 }` and execution body saved in `response.json`.

---

### 3️⃣ List Lambda Functions (`03_list_functions`)
* **Purpose**: Retrieves metadata for all deployed functions in the region.
* **AWS CLI Command**:
  ```bash
  aws lambda list-functions \
    --query "Functions[*].{Name:FunctionName, Runtime:Runtime, Memory:MemorySize}" \
    --output table \
    --endpoint-url http://localhost:4566
  ```
* **Command Breakdown**:
  * `--query`: JMESPath expression selecting specific fields.
  * `--output table`: Displays output as a clean text table.
* **Modifications to Make**: Remove query for full JSON, or change output format to `json` or `yaml`.
* **Input**: None / Region credentials.
* **Output**: Array table of function names, runtimes, and memory allocations.

---

### 4️⃣ Get Lambda Function Details (`04_get_function`)
* **Purpose**: Obtains complete configuration parameters and pre-signed download URL for code ZIP.
* **AWS CLI Command**:
  ```bash
  aws lambda get-function \
    --function-name my-first-lambda \
    --endpoint-url http://localhost:4566
  ```
* **Command Breakdown**:
  * `--function-name`: Target function name or ARN.
* **Modifications to Make**: Replace function name; optionally specify `--qualifier` for a version.
* **Input**: Function Name string (`my-first-lambda`).
* **Output**: JSON containing `Configuration` dictionary and `Code.Location` download link.

---

### 5️⃣ Update Function Code (`05_update_function_code`)
* **Purpose**: Replaces code deployment package of an existing function.
* **AWS CLI Command**:
  ```bash
  aws lambda update-function-code \
    --function-name my-first-lambda \
    --zip-file fileb://v2_code.zip \
    --publish \
    --endpoint-url http://localhost:4566
  ```
* **Command Breakdown**:
  * `--zip-file fileb://v2_code.zip`: New ZIP package path.
  * `--publish`: Creates a published immutable numbered version snapshot.
* **Modifications to Make**: Update `--function-name` and `--zip-file` path.
* **Input**: `v2_code.zip` containing updated `lambda_function_v2.py`.
* **Output**: Updated code hash (`CodeSha256`), code size, and version number.

---

### 6️⃣ Update Function Configuration (`06_update_function_configuration`)
* **Purpose**: Modifies runtime configuration settings (RAM, timeout, environment variables).
* **AWS CLI Command**:
  ```bash
  aws lambda update-function-configuration \
    --function-name my-first-lambda \
    --timeout 30 \
    --memory-size 256 \
    --environment "Variables={ENVIRONMENT=production,LOG_LEVEL=DEBUG}" \
    --endpoint-url http://localhost:4566
  ```
* **Command Breakdown**:
  * `--timeout`: Sets maximum runtime duration in seconds (1 - 900s).
  * `--memory-size`: Sets allocated RAM in MB (128 - 10240 MB).
  * `--environment`: Injects runtime environment key-value pairs.
* **Modifications to Make**: Adjust memory size, timeout value, and environment variables.
* **Input**: Configuration parameter values.
* **Output**: Updated configuration object JSON.

---

### 7️⃣ Delete Lambda Function (`07_delete_function`)
* **Purpose**: Permanently deletes a Lambda function resource.
* **AWS CLI Command**:
  ```bash
  aws lambda delete-function \
    --function-name my-first-lambda \
    --endpoint-url http://localhost:4566
  ```
* **Command Breakdown**:
  * `--function-name`: Name or ARN of function to delete.
* **Modifications to Make**: Ensure correct function name before executing.
* **Input**: Function Name (`my-first-lambda`).
* **Output**: HTTP 204 Status Code (No Content).

---

## 💡 6. AWS Lambda Best Practices

1. **Keep Deployment Packages Small**: Only include required dependencies to minimize cold start latency.
2. **Use Environment Variables**: Decouple configuration from code logic (e.g. database endpoints, feature flags).
3. **Right-Size Memory Allocation**: Test function memory usage; Lambda allocates CPU power proportionally to RAM.
4. **Idempotency & Error Handling**: Write functions to handle retries gracefully without causing side effects.
5. **IAM Principle of Least Privilege**: Grant only necessary permissions to the Lambda Execution Role.
