# ⚡ 07. Delete Lambda Function (`delete-function`)

This directory contains the Python automation script and AWS CLI commands for **Deleting an AWS Lambda Function** and its associated published versions/aliases.

---

## 📁 File Overview

* [`delete_function.py`](file:///c:/code/aws-s3-and-lmbda-operations/lambda-operations/07_delete_function/delete_function.py): Python Boto3 script that triggers `delete_function` API to permanently remove a Lambda function.

---

## 🐍 Detailed Section-by-Section Explanation of Code

### Explanation of `delete_function.py`

* **Module Banner & Header**: Standard module docstring defining purpose, SDK dependencies (`boto3`), and invocation script usage.
* **`SECTION 1: IMPORTS`**:
  * `import boto3`: Imports AWS SDK for Python.
  * `import os`: Imports standard OS environment interaction library.
* **`SECTION 2: GLOBAL CONFIGURATION & ENVIRONMENT VARIABLES`**:
  * `ENDPOINT_URL`: Endpoint URL defaulting to `http://localhost:4566` (LocalStack emulator).
  * `REGION_NAME`: AWS region identifier (`us-east-1`).
  * `FUNCTION_NAME`: Target Lambda function name (`my-first-lambda`).
* **`SECTION 3: MAIN EXECUTION FUNCTION`**:
  * `lambda_client = boto3.client("lambda", ...)`: Instantiates connection to AWS Lambda API.
  * `response = lambda_client.delete_function(FunctionName=FUNCTION_NAME)`: Sends HTTP DELETE request to AWS Lambda service.
  * `http_status = response.get('ResponseMetadata', {}).get('HTTPStatusCode')`: Safely extracts HTTP status code (204 = Success / No Content).
  * `except lambda_client.exceptions.ResourceNotFoundException`: Gracefully handles missing/already deleted functions.
* **`SECTION 4: SCRIPT ENTRY POINT`**: Direct main execution block (`if __name__ == "__main__": main()`).

---

## 🛠️ AWS CLI Command

```bash
aws lambda delete-function \
  --function-name my-first-lambda \
  --endpoint-url http://localhost:4566
```

---

## 🔍 Detailed AWS CLI Command Breakdown

| Parameter / Flag | Description & Purpose |
| :--- | :--- |
| `aws lambda delete-function` | Subcommand that invokes the DeleteFunction API call on AWS Lambda service. |
| `--function-name my-first-lambda` | Name, ARN, or qualified alias of the Lambda function to permanently delete. |
| `--qualifier 1` *(Optional)* | Deletes a specific published version instead of deleting the entire function resource. |
| `--endpoint-url http://localhost:4566` | Directs command to LocalStack emulator. **Omit for real AWS Cloud**. |

---

## ✏️ Changes You Should Make in the Command

1. **`--function-name`**: Replace `my-first-lambda` with the name of the function you wish to delete.
2. **`--qualifier`**: Optional - specify version number (e.g. `--qualifier 1`) to delete only that version.
3. **`--endpoint-url`**: **Remove** `--endpoint-url http://localhost:4566` when deleting real AWS Cloud resources.

---

## 📥 Detailed Input Details

* **Input Parameters**:
  ```json
  {
    "FunctionName": "my-first-lambda"
  }
  ```

---

## 📤 Detailed Output Details

### 1. Terminal / Script Execution Output:
```text
🚀 Initializing AWS Lambda Client (Endpoint: http://localhost:4566)...
🗑️ Deleting Lambda function 'my-first-lambda'...
✅ Function 'my-first-lambda' deleted successfully!
📊 Response Metadata (HTTP Status Code): 204
```

### 2. AWS CLI Response Output:
AWS CLI returns no text body on successful deletion (HTTP 204 No Content status code).
