# ⚡ 01. Create Lambda Function (`create-function`)

This directory contains the source code, Python automation script, and AWS CLI commands for **Creating an AWS Lambda Function**.

---

## 📁 File Overview

* [`lambda_function.py`](file:///c:/code/aws-s3-and-lmbda-operations/lambda-operations/01_create_function/lambda_function.py): The Python handler code executed inside AWS Lambda environment.
* [`create_function.py`](file:///c:/code/aws-s3-and-lmbda-operations/lambda-operations/01_create_function/create_function.py): Python Boto3 script that packages code into a `.zip` archive and calls AWS Lambda API to create the function.

---

## 🐍 Detailed Section-by-Section Explanation of Code

### 1. Explanation of Lambda Function Handler (`lambda_function.py`)

* **Module Banner & Header**: Declares module docstrings explaining dependencies, usage, and runtime scope.
* **`SECTION 1: IMPORTS`**:
  * `import json`: Encodes and decodes JSON objects for event payload logging and returning output body.
  * `import logging`: Provides native Python logging functionality integrated with AWS CloudWatch.
* **`SECTION 2: LOGGER CONFIGURATION`**:
  * `logger = logging.getLogger()`: Retrives standard root logger.
  * `logger.setLevel(logging.INFO)`: Enables informative execution log statements.
* **`SECTION 3: LAMBDA HANDLER FUNCTION`**:
  * `def lambda_handler(event, context):`: Primary entrypoint function invoked by AWS Lambda service.
    * `event`: Dictionary object containing input event payload.
    * `context`: Runtime environment object providing AWS execution context.
  * `user_name = event.get("name", "World")`: Extracts `"name"` from `event` dictionary, defaulting to `"World"`.
  * `response = { "statusCode": 200, ... }`: Constructs standard HTTP API Gateway / CLI response dictionary with payload metadata.

---

### 2. Explanation of Python Deployment Script (`create_function.py`)

* **Module Banner & Header**: Describes module metadata, required SDK dependencies (`boto3`), and execution instructions.
* **`SECTION 1: IMPORTS`**:
  * `boto3`: AWS SDK for Python used to interact with AWS Lambda service APIs.
  * `zipfile`, `io`, `os`, `json`: Built-in utilities for in-memory file compression, environment reading, and formatting.
* **`SECTION 2: GLOBAL CONFIGURATION & ENVIRONMENT VARIABLES`**:
  * `ENDPOINT_URL`: Reads `AWS_ENDPOINT_URL` environment variable (defaults to `http://localhost:4566` for LocalStack).
  * `REGION_NAME`: AWS region identifier (`us-east-1`).
  * `FUNCTION_NAME`, `ROLE_ARN`, `RUNTIME`, `HANDLER`: Parameters defining the function name, IAM role, runtime engine, and entry point.
* **`SECTION 3: HELPER FUNCTIONS`**:
  * `def create_zip_in_memory()`: Uses `io.BytesIO()` and `zipfile.ZipFile` to compress `lambda_function.py` into a binary byte buffer without touching disk.
* **`SECTION 4: MAIN EXECUTION FUNCTION`**:
  * `lambda_client = boto3.client("lambda", ...)`: Connects to AWS Lambda API endpoint.
  * `lambda_client.create_function(...)`: Dispatches HTTP request to create the Lambda function resource.
  * `except lambda_client.exceptions.ResourceConflictException`: Gracefully intercepts duplicate function creation attempts.
* **`SECTION 5: SCRIPT ENTRY POINT`**:
  * `if __name__ == "__main__": main()`: Ensures function executes only when invoked directly.

---

## 🛠️ AWS CLI Command

To create the Lambda function using AWS CLI, first compress `lambda_function.py` into `function.zip`:

### PowerShell / Bash Zip Command:
```bash
# Windows PowerShell
Compress-Archive -Path lambda_function.py -DestinationPath function.zip -Force

# Linux / macOS Bash
zip function.zip lambda_function.py
```

### AWS CLI Command:
```bash
aws lambda create-function \
  --function-name my-first-lambda \
  --runtime python3.12 \
  --role arn:aws:iam::123456789012:role/lambda-execution-role \
  --handler lambda_function.lambda_handler \
  --zip-file fileb://function.zip \
  --description "Initial deployment of demo lambda function" \
  --timeout 15 \
  --memory-size 128 \
  --endpoint-url http://localhost:4566
```

---

## 🔍 Detailed AWS CLI Command Breakdown

| Parameter / Flag | Description & Purpose |
| :--- | :--- |
| `aws lambda create-function` | Subcommand that invokes the CreateFunction API call on AWS Lambda service. |
| `--function-name my-first-lambda` | Unique identifier name assigned to your Lambda function in your AWS region/account. |
| `--runtime python3.12` | Runtime environment for execution (e.g., `python3.12`, `python3.11`, `nodejs20.x`, `java17`). |
| `--role arn:...` | IAM Role ARN providing permissions for Lambda to access AWS resources (CloudWatch, S3, DynamoDB). |
| `--handler lambda_function.lambda_handler` | Entry point in format `<file_basename>.<function_name>`. Points to `lambda_handler` in `lambda_function.py`. |
| `--zip-file fileb://function.zip` | Path to deployment `.zip` package. The prefix `fileb://` reads the zip as raw binary bytes. |
| `--description "..."` | Human-readable text description stored with the function metadata. |
| `--timeout 15` | Maximum execution duration in seconds before Lambda terminates execution (1 to 900 seconds). |
| `--memory-size 128` | Memory allocated in MB (128 MB to 10,240 MB). CPU power scales proportionally. |
| `--endpoint-url http://localhost:4566` | Directs command to LocalStack emulator. **Omit for real AWS Cloud**. |

---

## ✏️ Changes You Should Make in the Command

1. **`--function-name`**: Replace `my-first-lambda` with your desired function name.
2. **`--runtime`**: Change `python3.12` to your code's language version if using Node.js or Java.
3. **`--role`**: Update `arn:aws:iam::123456789012:role/...` to match your actual AWS IAM Execution Role ARN.
4. **`--zip-file`**: Update `fileb://function.zip` to point to your actual `.zip` path.
5. **`--endpoint-url`**: **Remove** `--endpoint-url http://localhost:4566` when deploying to AWS Cloud.

---

## 📥 Detailed Input Details

* **Input File**: `function.zip` containing `lambda_function.py`.
* **Input CLI Parameters**:
  ```json
  {
    "FunctionName": "my-first-lambda",
    "Runtime": "python3.12",
    "Role": "arn:aws:iam::123456789012:role/lambda-execution-role",
    "Handler": "lambda_function.lambda_handler",
    "ZipFile": "fileb://function.zip",
    "Timeout": 15,
    "MemorySize": 128
  }
  ```

---

## 📤 Detailed Output Details

### 1. Terminal / Python Execution Output:
```text
🚀 Initializing AWS Lambda Client (Endpoint: http://localhost:4566)...
📦 Creating Lambda function 'my-first-lambda'...
✅ Lambda Function Created Successfully!
```

### 2. API Response JSON Output:
```json
{
  "FunctionName": "my-first-lambda",
  "FunctionArn": "arn:aws:lambda:us-east-1:000000000000:function:my-first-lambda",
  "Runtime": "python3.12",
  "Role": "arn:aws:iam::123456789012:role/lambda-execution-role",
  "Handler": "lambda_function.lambda_handler",
  "CodeSize": 482,
  "Description": "Initial deployment of demo lambda function",
  "Timeout": 15,
  "MemorySize": 128,
  "LastModified": "2026-08-25T15:58:00.000+0000",
  "CodeSha256": "47DEQpj8HBSa+/TImW+5JCeuQeRkm5NMpJWZG3hSuFU=",
  "Version": "$LATEST",
  "State": "Active",
  "PackageType": "Zip"
}
```
