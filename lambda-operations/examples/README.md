# 🚀 AWS Lambda Operations - Real-World Beginner Examples

Welcome to the **AWS Lambda Real-World Examples Directory**! This folder contains 4 complete, production-ready, beginner-friendly Lambda application examples.

---

## 📁 Examples Directory Index

| Example Folder | Application Scenario | Event Source | Key Technical Focus | Link to Guide |
| :--- | :--- | :--- | :--- | :--- |
| **`01_s3_thumbnail_generator/`** | S3 File Upload & Thumbnail Processor | Amazon S3 Trigger | S3 Event Record parsing, URL decoding, metadata logs | [`01_s3_thumbnail_generator/README.md`](file:///c:/code/aws-s3-and-lmbda-operations/lambda-operations/examples/01_s3_thumbnail_generator/README.md) |
| **`02_serverless_api_backend/`** | REST API Backend Gateway | Amazon API Gateway | HTTP Method handling, Query parameter parsing, JSON body formatting | [`02_serverless_api_backend/README.md`](file:///c:/code/aws-s3-and-lmbda-operations/lambda-operations/examples/02_serverless_api_backend/README.md) |
| **`03_scheduled_cloudwatch_cleaner/`** | Scheduled Resource Audit & Cleaner | Amazon EventBridge (Cron Timer) | EventBridge scheduled triggers, ISO timestamp logging, cleanup metrics | [`03_scheduled_cloudwatch_cleaner/README.md`](file:///c:/code/aws-s3-and-lmbda-operations/lambda-operations/examples/03_scheduled_cloudwatch_cleaner/README.md) |
| **`04_user_registration_processor/`** | User Signup Data Validator & Ingestion | Direct Invocation / Webhook | Input field validation, UUID generation, structured user metadata creation | [`04_user_registration_processor/README.md`](file:///c:/code/aws-s3-and-lmbda-operations/lambda-operations/examples/04_user_registration_processor/README.md) |

---

## ⚡ Quick Execution Guide (Run Any Example on Any Computer)

Every example folder includes an automated Python runner (`run_example.py`) that packages code, deploys to LocalStack/AWS, invokes the function with sample payloads, and prints formatted output.

### Run Example 1 (S3 Thumbnail Generator):
```bash
python examples/01_s3_thumbnail_generator/run_example.py
```

### Run Example 2 (Serverless REST API Backend):
```bash
python examples/02_serverless_api_backend/run_example.py
```

### Run Example 3 (Scheduled Cron Cleaner Task):
```bash
python examples/03_scheduled_cloudwatch_cleaner/run_example.py
```

### Run Example 4 (User Registration Processor):
```bash
python examples/04_user_registration_processor/run_example.py
```

---

## 🌐 Cross-System & Cross-Platform Support

* **Local Emulator (LocalStack/Floci)**: Set environment variable `AWS_ENDPOINT_URL=http://localhost:4566`.
* **Real AWS Cloud**: Unset `AWS_ENDPOINT_URL` or remove `--endpoint-url http://localhost:4566` from CLI commands.
* **OS Support**: Windows (PowerShell), macOS (Zsh/Bash), Linux (Ubuntu).
