# ⚡ 05. Update Lambda Function Code (`update-function-code`)

This directory contains the updated v2 Lambda code, deployment script, and AWS CLI commands for **Updating the Executable Code** of an existing Lambda function.

---

## 📁 File Overview

* [`lambda_function_v2.py`](file:///c:/code/aws-s3-and-lmbda-operations/lambda-operations/05_update_function_code/lambda_function_v2.py): Version 2.0 of the Lambda handler featuring ISO UTC timestamping, enhanced headers, and version tagging.
* [`update_function_code.py`](file:///c:/code/aws-s3-and-lmbda-operations/lambda-operations/05_update_function_code/update_function_code.py): Python Boto3 script that packages `lambda_function_v2.py` into a zip archive as `lambda_function.py` and calls `UpdateFunctionCode`.

---

## 🐍 Detailed Section-by-Section Explanation of Code

### 1. Explanation of Updated Handler (`lambda_function_v2.py`)

* **Module Banner & Header**: Describes handler versioning (v2.0), new features, and dependencies (`json`, `logging`, `datetime`).
* **`SECTION 1: IMPORTS`**: Imports standard library packages including `datetime` for ISO timestamp formatting.
* **`SECTION 2: LOGGER CONFIGURATION`**: Configures INFO logging level.
* **`SECTION 3: UPDATED LAMBDA HANDLER FUNCTION (v2)`**:
  * `timestamp = datetime.datetime.utcnow().isoformat()`: Captures current UTC timestamp.
  * `response_body`: Builds expanded response dictionary containing version string `"2.0.0"`, timestamp, and features list.
  * `response["headers"]["X-Lambda-Version"]`: Injects custom version tracking HTTP header.

### 2. Explanation of Python Boto3 Script (`update_function_code.py`)

* **Module Banner & Header**: Outlines deployment purpose, prerequisites, and execution commands.
* **`SECTION 1: IMPORTS`**: Imports `boto3`, `zipfile`, `io`, `os`, and `json`.
* **`SECTION 2: GLOBAL CONFIGURATION & ENVIRONMENT VARIABLES`**: Configures `ENDPOINT_URL`, `REGION_NAME`, and target `FUNCTION_NAME`.
* **`SECTION 3: HELPER FUNCTIONS`**:
  * `create_updated_zip_in_memory()`: Archives `lambda_function_v2.py` as `lambda_function.py` inside an in-memory ZIP buffer so the existing handler pointer (`lambda_function.lambda_handler`) remains valid.
* **`SECTION 4: MAIN EXECUTION FUNCTION`**:
  * `lambda_client.update_function_code(...)`: Sends new ZIP package bytes to AWS API via `UpdateFunctionCode`.
  * `Publish=True`: Directs AWS Lambda to publish an immutable numbered version snapshot (e.g. Version 2).
* **`SECTION 5: SCRIPT ENTRY POINT`**: Standalone execution block.

---

## 🛠️ AWS CLI Commands

### 1. Create ZIP Archive for v2 Code:
```bash
# Windows PowerShell
Compress-Archive -Path lambda_function_v2.py -DestinationPath v2_code.zip -Force

# Linux / macOS Bash
zip -j v2_code.zip lambda_function_v2.py
```

### 2. AWS CLI Update Code Command:
```bash
aws lambda update-function-code \
  --function-name my-first-lambda \
  --zip-file fileb://v2_code.zip \
  --publish \
  --endpoint-url http://localhost:4566
```

---

## 🔍 Detailed AWS CLI Command Breakdown

| Parameter / Flag | Description & Purpose |
| :--- | :--- |
| `aws lambda update-function-code` | Subcommand that invokes UpdateFunctionCode API call on AWS Lambda service. |
| `--function-name my-first-lambda` | Name or ARN of the existing Lambda function to update. |
| `--zip-file fileb://v2_code.zip` | Path to the updated `.zip` code package file. The `fileb://` prefix reads raw binary bytes. |
| `--publish` *(Optional)* | Publishes a new immutable version of the function (e.g., Version 2). |
| `--dry-run` *(Optional)* | Validates code package format and SHA256 checksum without updating deployment. |
| `--endpoint-url http://localhost:4566` | Target endpoint URL for LocalStack emulator. **Omit for AWS Cloud**. |

---

## ✏️ Changes You Should Make in the Command

1. **`--function-name`**: Replace `my-first-lambda` with your targeted Lambda function name.
2. **`--zip-file`**: Change `fileb://v2_code.zip` to your updated `.zip` file archive path.
3. **`--publish`**: Omit `--publish` if you only want to update `$LATEST` without creating a published numbered version.
4. **`--endpoint-url`**: **Remove** `--endpoint-url http://localhost:4566` when deploying to real AWS Cloud.

---

## 📥 Detailed Input Details

* **Input File**: `v2_code.zip` containing `lambda_function.py`.
* **Input API Parameters**:
  ```json
  {
    "FunctionName": "my-first-lambda",
    "ZipFile": "fileb://v2_code.zip",
    "Publish": true
  }
  ```

---

## 📤 Detailed Output Details

### 1. Terminal / Script Execution Output:
```text
🚀 Initializing AWS Lambda Client (Endpoint: http://localhost:4566)...
🔄 Updating code for Lambda function 'my-first-lambda'...
✅ Lambda Function Code Updated Successfully!
```

### 2. Full API Response JSON:
```json
{
  "FunctionName": "my-first-lambda",
  "FunctionArn": "arn:aws:lambda:us-east-1:000000000000:function:my-first-lambda",
  "Runtime": "python3.12",
  "Role": "arn:aws:iam::123456789012:role/lambda-execution-role",
  "Handler": "lambda_function.lambda_handler",
  "CodeSize": 540,
  "Description": "Initial deployment of demo lambda function",
  "Timeout": 15,
  "MemorySize": 128,
  "LastModified": "2026-08-25T15:59:00.000+0000",
  "CodeSha256": "vN3X5+P8zK7gU2M0a1QeW9v4J8z7L6K5j4H3g2F1e0D=",
  "Version": "2",
  "State": "Active"
}
```
