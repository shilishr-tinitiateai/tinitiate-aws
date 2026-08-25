# ⚡ 06. Update Lambda Function Configuration (`update-function-configuration`)

This directory contains the Python automation script and AWS CLI commands for **Modifying Function Runtime Settings** (Timeout, Memory Allocation, Environment Variables, and Execution Role).

---

## 📁 File Overview

* [`update_function_config.py`](file:///c:/code/aws-s3-and-lmbda-operations/lambda-operations/06_update_function_configuration/update_function_config.py): Python Boto3 script that modifies timeout duration, RAM allocation, and environment key-value pairs of a Lambda function without re-uploading code.

---

## 🐍 Detailed Section-by-Section Explanation of Code

### Explanation of `update_function_config.py`

* **Module Banner & Header**: Describes module metadata, required SDK dependencies (`boto3`), and execution instructions.
* **`SECTION 1: IMPORTS`**: Loads `boto3`, `json`, and `os`.
* **`SECTION 2: GLOBAL CONFIGURATION & ENVIRONMENT VARIABLES`**: Configures `ENDPOINT_URL`, `REGION_NAME`, and target `FUNCTION_NAME`.
* **`SECTION 3: MAIN EXECUTION FUNCTION`**:
  * `lambda_client = boto3.client("lambda", ...)`: Initializes AWS Lambda API client.
  * `lambda_client.update_function_configuration(...)`: Submits operational setting modifications:
    * `Timeout=30`: Increases execution timeout limit from 15s to 30s.
    * `MemorySize=256`: Increases allocated RAM from 128 MB to 256 MB. CPU allocation doubles proportionally.
    * `Environment={"Variables": {...}}`: Injects environment variables (`ENVIRONMENT`, `LOG_LEVEL`, `DATABASE_NAME`, `MAX_CONNECTIONS`) accessible inside Lambda runtime code via `os.environ.get(...)`.
* **`SECTION 4: SCRIPT ENTRY POINT`**: Direct execution block.

---

## 🛠️ AWS CLI Command

```bash
aws lambda update-function-configuration \
  --function-name my-first-lambda \
  --timeout 30 \
  --memory-size 256 \
  --description "Updated Lambda configuration with enhanced memory & env variables" \
  --environment "Variables={ENVIRONMENT=production,LOG_LEVEL=DEBUG,DATABASE_NAME=app_db_prod}" \
  --endpoint-url http://localhost:4566
```

---

## 🔍 Detailed AWS CLI Command Breakdown

| Parameter / Flag | Description & Purpose |
| :--- | :--- |
| `aws lambda update-function-configuration` | Subcommand that triggers UpdateFunctionConfiguration API call. |
| `--function-name my-first-lambda` | Targeted Lambda function name or ARN. |
| `--timeout 30` | Maximum runtime limit in seconds (allowed range: 1 to 900 seconds / 15 mins). |
| `--memory-size 256` | RAM size in MB (allowed range: 128 MB to 10,240 MB in 1 MB increments). |
| `--description "..."` | Updates descriptive text summary associated with the function. |
| `--environment "Variables={...}"` | Key-Value dictionary object string injecting runtime environment variables. |
| `--handler lambda_function.lambda_handler` *(Optional)* | Modifies handler entrypoint function path without re-uploading ZIP package. |
| `--endpoint-url http://localhost:4566` | Directs command to LocalStack emulator. **Omit for real AWS Cloud**. |

---

## ✏️ Changes You Should Make in the Command

1. **`--function-name`**: Replace `my-first-lambda` with your specific Lambda function name.
2. **`--timeout`**: Set timeout appropriate for your workload (e.g. 5 seconds for light APIs, 300 seconds for batch processing).
3. **`--memory-size`**: Adjust memory allocation (128, 256, 512, 1024, 2048 MB).
4. **`--environment`**: Customize environment keys and values required by your application code.
5. **`--endpoint-url`**: **Remove** `--endpoint-url http://localhost:4566` when configuring real AWS Cloud.

---

## 📥 Detailed Input Details

* **Input Configuration Parameters**:
  ```json
  {
    "FunctionName": "my-first-lambda",
    "Timeout": 30,
    "MemorySize": 256,
    "Description": "Updated Lambda configuration with enhanced memory & env variables",
    "Environment": {
      "Variables": {
        "ENVIRONMENT": "production",
        "LOG_LEVEL": "DEBUG",
        "DATABASE_NAME": "app_db_prod"
      }
    }
  }
  ```

---

## 📤 Detailed Output Details

### 1. Terminal Execution Response Summary:
```text
🚀 Initializing AWS Lambda Client (Endpoint: http://localhost:4566)...
⚙️ Updating configuration settings for function 'my-first-lambda'...
✅ Function Configuration Updated Successfully!
```

### 2. Full API Response JSON Output:
```json
{
  "FunctionName": "my-first-lambda",
  "FunctionArn": "arn:aws:lambda:us-east-1:000000000000:function:my-first-lambda",
  "Runtime": "python3.12",
  "Role": "arn:aws:iam::123456789012:role/lambda-execution-role",
  "Handler": "lambda_function.lambda_handler",
  "CodeSize": 540,
  "Description": "Updated Lambda configuration with enhanced memory & env variables",
  "Timeout": 30,
  "MemorySize": 256,
  "LastModified": "2026-08-25T15:59:12.000+0000",
  "CodeSha256": "vN3X5+P8zK7gU2M0a1QeW9v4J8z7L6K5j4H3g2F1e0D=",
  "Version": "$LATEST",
  "Environment": {
    "Variables": {
      "ENVIRONMENT": "production",
      "LOG_LEVEL": "DEBUG",
      "DATABASE_NAME": "app_db_prod",
      "MAX_CONNECTIONS": "100"
    }
  },
  "State": "Active"
}
```
