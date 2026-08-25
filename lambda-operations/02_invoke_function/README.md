# ⚡ 02. Invoke Lambda Function (`invoke`)

This directory contains the payload configuration, Python execution script, and AWS CLI commands for **Invoking an AWS Lambda Function**.

---

## 📁 File Overview

* [`payload.json`](file:///c:/code/aws-s3-and-lmbda-operations/lambda-operations/02_invoke_function/payload.json): The input event payload file passed to the Lambda function handler.
* [`invoke_function.py`](file:///c:/code/aws-s3-and-lmbda-operations/lambda-operations/02_invoke_function/invoke_function.py): Python Boto3 script that reads `payload.json`, triggers synchronous Lambda execution, and writes output to `response.json`.

---

## 🐍 Detailed Section-by-Section Explanation of Code

### 1. Explanation of `payload.json`
* `"name": "Alice Developer"`: Custom key-value input parameter sent into `event["name"]` inside the Lambda code handler.
* `"environment": "production"`, `"request_id": "REQ-10042"`: Metadata passed inside the event dictionary payload.

### 2. Explanation of Python Invocation Script (`invoke_function.py`)

* **Module Banner & Header**: Describes module functionality, dependencies (`boto3`), and execution instructions.
* **`SECTION 1: IMPORTS`**: Loads `boto3`, `json`, and `os` standard libraries.
* **`SECTION 2: GLOBAL CONFIGURATION & ENVIRONMENT VARIABLES`**: Sets `ENDPOINT_URL`, `REGION_NAME`, target `FUNCTION_NAME`, and file paths for `payload.json` and `response.json`.
* **`SECTION 3: MAIN EXECUTION FUNCTION`**:
  * `lambda_client = boto3.client("lambda", ...)`: Initializes the Boto3 client object.
  * `with open(PAYLOAD_FILE, "r") as f`: Loads input event data from `payload.json`.
  * `lambda_client.invoke(...)`: Executes function with parameters:
    * `InvocationType="RequestResponse"`: Synchronous execution mode.
    * `LogType="Tail"`: Fetches execution log tail in response headers.
    * `Payload=payload_json.encode("utf-8")`: Converts JSON payload into byte stream.
  * `response["Payload"].read().decode("utf-8")`: Reads execution response stream and saves JSON payload into `response.json`.
* **`SECTION 4: SCRIPT ENTRY POINT`**: Triggers `main()` execution when script is executed directly.

---

## 🛠️ AWS CLI Commands

### 1. Invoke with Inline JSON Payload
```bash
aws lambda invoke \
  --function-name my-first-lambda \
  --payload '{"name": "Alice"}' \
  --cli-binary-format raw-in-base64-out \
  response.json \
  --endpoint-url http://localhost:4566
```

### 2. Invoke Using Payload File (`payload.json`)
```bash
# Windows PowerShell
aws lambda invoke `
  --function-name my-first-lambda `
  --payload file://payload.json `
  --cli-binary-format raw-in-base64-out `
  response.json `
  --endpoint-url http://localhost:4566

# Linux / macOS Bash
aws lambda invoke \
  --function-name my-first-lambda \
  --payload file://payload.json \
  --cli-binary-format raw-in-base64-out \
  response.json \
  --endpoint-url http://localhost:4566
```

---

## 🔍 Detailed AWS CLI Command Breakdown

| Parameter / Flag | Description & Purpose |
| :--- | :--- |
| `aws lambda invoke` | Subcommand that triggers the Invoke API call on AWS Lambda service. |
| `--function-name my-first-lambda` | Name or ARN of target Lambda function to run. |
| `--payload file://payload.json` | Passes event data to function. Can be inline raw JSON or file reference prefixed with `file://`. |
| `--cli-binary-format raw-in-base64-out` | **Crucial Flag**: Tells AWS CLI v2 to treat `--payload` input as raw string/bytes rather than base64 encoded payload. |
| `response.json` | Output filename argument where response payload returned by Lambda handler is saved. |
| `--invocation-type Event` *(Optional)* | Changes execution to **asynchronous** (returns status 202 without waiting for function result). |
| `--endpoint-url http://localhost:4566` | Target endpoint URL for LocalStack emulator. **Omit for AWS Cloud**. |

---

## ✏️ Changes You Should Make in the Command

1. **`--function-name`**: Replace `my-first-lambda` with your specific deployed Lambda function name.
2. **`--payload`**: Replace `'{"name": "Alice"}'` or `file://payload.json` with your actual input data structure.
3. **`response.json`**: Change the output file path/name if desired (e.g., `output_result.json`).
4. **`--endpoint-url`**: **Remove** `--endpoint-url http://localhost:4566` when executing against real AWS Cloud.

---

## 📥 Detailed Input Details

* **Input Event Payload (`payload.json`)**:
  ```json
  {
    "name": "Alice Developer",
    "environment": "production",
    "request_id": "REQ-10042",
    "tags": ["testing", "lambda", "demo"]
  }
  ```

---

## 📤 Detailed Output Details

### 1. Terminal Execution Response (CLI metadata output):
```json
{
  "StatusCode": 200,
  "ExecutedVersion": "$LATEST"
}
```

### 2. Saved File Output (`response.json`):
```json
{
  "statusCode": 200,
  "headers": {
    "Content-Type": "application/json"
  },
  "body": {
    "message": "Hello, Alice Developer! AWS Lambda function executed successfully.",
    "input_received": {
      "name": "Alice Developer",
      "environment": "production",
      "request_id": "REQ-10042",
      "tags": [
        "testing",
        "lambda",
        "demo"
      ]
    },
    "status": "SUCCESS"
  }
}
```
