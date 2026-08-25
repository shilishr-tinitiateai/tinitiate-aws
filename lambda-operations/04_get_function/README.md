# ⚡ 04. Get Lambda Function Details (`get-function`)

This directory contains the Python automation script and AWS CLI commands for **Retrieving Detailed Metadata & Code Location** of a single AWS Lambda function.

---

## 📁 File Overview

* [`get_function.py`](file:///c:/code/aws-s3-and-lmbda-operations/lambda-operations/04_get_function/get_function.py): Python Boto3 script that fetches configuration properties, IAM role, runtime attributes, and pre-signed deployment package download URL.

---

## 🐍 Detailed Section-by-Section Explanation of Code

### Explanation of `get_function.py`

* **Module Banner & Header**: Module docstrings detailing goals, SDK requirements (`boto3`), and execution syntax.
* **`SECTION 1: IMPORTS`**: Loads `boto3`, `json`, and `os`.
* **`SECTION 2: GLOBAL CONFIGURATION & ENVIRONMENT VARIABLES`**: Defines `ENDPOINT_URL`, `REGION_NAME`, and target `FUNCTION_NAME`.
* **`SECTION 3: MAIN EXECUTION FUNCTION`**:
  * `lambda_client = boto3.client("lambda", ...)`: Connects Boto3 to Lambda service endpoint.
  * `response = lambda_client.get_function(FunctionName=FUNCTION_NAME)`: Calls `GetFunction` API endpoint.
  * `config = response.get("Configuration", {})`: Extracts runtime metadata object (timeout, memory size, handler, IAM execution role).
  * `code_info = response.get("Code", {})`: Obtains secure pre-signed download S3 URL (`Location`) for the deployment ZIP package.
* **`SECTION 4: SCRIPT ENTRY POINT`**: Direct execution wrapper.

---

## 🛠️ AWS CLI Command

### Get Complete Details (JSON):
```bash
aws lambda get-function \
  --function-name my-first-lambda \
  --endpoint-url http://localhost:4566
```

### Download Deployment Package ZIP via CLI:
```bash
aws lambda get-function \
  --function-name my-first-lambda \
  --query "Code.Location" \
  --output text \
  --endpoint-url http://localhost:4566
```

---

## 🔍 Detailed AWS CLI Command Breakdown

| Parameter / Flag | Description & Purpose |
| :--- | :--- |
| `aws lambda get-function` | Subcommand that triggers GetFunction API call on AWS Lambda service. |
| `--function-name my-first-lambda` | The name, ARN, or qualified alias of the Lambda function to inspect. |
| `--qualifier $LATEST` *(Optional)* | Version number or alias name (e.g. `PROD`, `1`, `$LATEST`). Defaults to `$LATEST`. |
| `--query "Code.Location"` *(Optional)* | Filters response to extract only the HTTP download URL of the function source ZIP package. |
| `--endpoint-url http://localhost:4566` | Target endpoint URL for LocalStack emulator. **Omit for AWS Cloud**. |

---

## ✏️ Changes You Should Make in the Command

1. **`--function-name`**: Replace `my-first-lambda` with your targeted Lambda function name.
2. **`--qualifier`**: Optional - add `--qualifier 1` or `--qualifier PROD` to retrieve details for a published version or alias.
3. **`--endpoint-url`**: **Remove** `--endpoint-url http://localhost:4566` when retrieving from real AWS Cloud.

---

## 📥 Detailed Input Details

* **Input Parameters**:
  ```json
  {
    "FunctionName": "my-first-lambda",
    "Qualifier": "$LATEST"
  }
  ```

---

## 📤 Detailed Output Details

### 1. Terminal / Python Script Output Summary:
```text
🚀 Initializing AWS Lambda Client (Endpoint: http://localhost:4566)...
🔍 Fetching configuration and code details for 'my-first-lambda'...

⚙️ Function Configuration:
• Name:        my-first-lambda
• ARN:         arn:aws:lambda:us-east-1:000000000000:function:my-first-lambda
• Runtime:     python3.12
• Handler:     lambda_function.lambda_handler
• Code Size:   482 bytes
• Memory Size: 128 MB
• Timeout:     15 s
• State:       Active
```

### 2. Full API Response JSON Structure:
```json
{
  "Configuration": {
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
    "State": "Active"
  },
  "Code": {
    "RepositoryType": "S3",
    "Location": "http://localhost:4566/archive/my-first-lambda.zip?AWSAccessKeyId=test..."
  }
}
```
