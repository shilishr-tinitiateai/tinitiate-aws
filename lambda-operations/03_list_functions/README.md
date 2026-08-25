# ⚡ 03. List Lambda Functions (`list-functions`)

This directory contains the Python automation script and AWS CLI commands for **Listing All Lambda Functions** in your AWS account and region.

---

## 📁 File Overview

* [`list_functions.py`](file:///c:/code/aws-s3-and-lmbda-operations/lambda-operations/03_list_functions/list_functions.py): Python Boto3 script that queries the AWS Lambda service for all deployed functions and prints formatted metadata.

---

## 🐍 Detailed Section-by-Section Explanation of Code

### Explanation of `list_functions.py`

* **Module Banner & Header**: Docstring describing module summary, dependencies (`boto3`), and execution instructions.
* **`SECTION 1: IMPORTS`**: Imports `boto3`, `json`, and `os`.
* **`SECTION 2: GLOBAL CONFIGURATION & ENVIRONMENT VARIABLES`**: Configures `ENDPOINT_URL` and `REGION_NAME`.
* **`SECTION 3: MAIN EXECUTION FUNCTION`**:
  * `lambda_client = boto3.client("lambda", ...)`: Instantiates the Boto3 Lambda client.
  * `response = lambda_client.list_functions()`: Dispatches request to `ListFunctions` API.
  * `functions = response.get("Functions", [])`: Extracts array list of function metadata objects.
  * `for fn in functions:`: Loops through function metadata objects and prints attributes (`FunctionName`, `Runtime`, `Handler`, `CodeSize`, `MemorySize`, `Timeout`, `FunctionArn`).
* **`SECTION 4: SCRIPT ENTRY POINT`**: Runs `main()` when executed as standalone script.

---

## 🛠️ AWS CLI Command

### Standard List Command:
```bash
aws lambda list-functions --endpoint-url http://localhost:4566
```

### Filtered List Command (JMESPath Output Query):
```bash
aws lambda list-functions \
  --query "Functions[*].{Name:FunctionName, Runtime:Runtime, Memory:MemorySize, Timeout:Timeout}" \
  --output table \
  --endpoint-url http://localhost:4566
```

---

## 🔍 Detailed AWS CLI Command Breakdown

| Parameter / Flag | Description & Purpose |
| :--- | :--- |
| `aws lambda list-functions` | Subcommand that invokes the ListFunctions API call on AWS Lambda service. |
| `--master-region us-east-1` *(Optional)* | Filters Lambda edge functions created by AWS Lambda@Edge. |
| `--max-items 10` *(Optional)* | Limits the number of functions returned per API pagination call. |
| `--query "..."` *(Optional)* | JMESPath client-side query string to select and rename specific JSON attributes. |
| `--output table` *(Optional)* | Formats returned JSON response into an ASCII table (`table`, `json`, `text`, `yaml`). |
| `--endpoint-url http://localhost:4566` | Target endpoint URL for LocalStack emulator. **Omit for AWS Cloud**. |

---

## ✏️ Changes You Should Make in the Command

1. **`--output`**: Change `table` to `json` or `text` based on script requirements.
2. **`--max-items`**: Add `--max-items 50` if pagination control is needed for accounts with hundreds of functions.
3. **`--endpoint-url`**: **Remove** `--endpoint-url http://localhost:4566` when listing real AWS Cloud resources.

---

## 📥 Detailed Input Details

* **Input Parameters**: None (Lists all functions in configured region).
* **Optional Filters**: Max items, marker pagination token, or query projection expressions.

---

## 📤 Detailed Output Details

### 1. Formatted Table Output (`--output table`):
```text
-------------------------------------------------------------------------
|                             ListFunctions                             |
+-----------------+----------+------------------+-----------------------+
|     Memory      |  Name    |     Runtime      |        Timeout        |
+-----------------+----------+------------------+-----------------------+
|  128            |  my-func |  python3.12      |  15                   |
+-----------------+----------+------------------+-----------------------+
```

### 2. Standard JSON Response Output:
```json
{
  "Functions": [
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
      "Version": "$LATEST"
    }
  ]
}
```
