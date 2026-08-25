# ⏱️ Example 3: Scheduled Cron Task (Amazon EventBridge Timer)

Welcome to **Example 3**! This guide demonstrates how to schedule AWS Lambda functions to run automatically on a periodic timer (like a Linux cron job).

---

## 🎯 What Does This Example Do?

1. **Amazon EventBridge** triggers a scheduled rule every night at 12:00 AM (`cron(0 0 * * ? *)`).
2. The timer passes event metadata containing rule names and execution timestamps to Lambda.
3. Lambda executes the cleanup logic (purging temp logs, auditing database tables) and returns operational summary statistics.

---

## 📁 File Structure

* [`lambda_function.py`](file:///c:/code/aws-s3-and-lmbda-operations/lambda-operations/examples/03_scheduled_cloudwatch_cleaner/lambda_function.py): Python Lambda function handler.
* [`sample_timer_event.json`](file:///c:/code/aws-s3-and-lmbda-operations/lambda-operations/examples/03_scheduled_cloudwatch_cleaner/sample_timer_event.json): Mock EventBridge scheduled event payload.
* [`run_example.py`](file:///c:/code/aws-s3-and-lmbda-operations/lambda-operations/examples/03_scheduled_cloudwatch_cleaner/run_example.py): Automated Boto3 deployment & execution script.

---

## 💻 How to Run on ANY Computer (Windows, macOS, Linux)

### Option A: Run via Python Runner Script (Recommended)
```bash
python run_example.py
```

---

### Option B: Run via AWS CLI (Step-by-Step)

#### Step 1: Zip the Lambda function
```bash
# Windows PowerShell
Compress-Archive -Path lambda_function.py -DestinationPath cron_func.zip -Force

# Linux / macOS Bash
zip cron_func.zip lambda_function.py
```

#### Step 2: Create the Lambda function
```bash
aws lambda create-function \
  --function-name scheduled-cron-cleaner-example \
  --runtime python3.12 \
  --role arn:aws:iam::123456789012:role/lambda-role \
  --handler lambda_function.lambda_handler \
  --zip-file fileb://cron_func.zip \
  --endpoint-url http://localhost:4566
```

#### Step 3: Invoke the function with scheduled event payload
```bash
# Windows PowerShell
aws lambda invoke `
  --function-name scheduled-cron-cleaner-example `
  --payload file://sample_timer_event.json `
  --cli-binary-format raw-in-base64-out `
  output.json `
  --endpoint-url http://localhost:4566

# Linux / macOS Bash
aws lambda invoke \
  --function-name scheduled-cron-cleaner-example \
  --payload file://sample_timer_event.json \
  --cli-binary-format raw-in-base64-out \
  output.json \
  --endpoint-url http://localhost:4566
```

---

## 📥 Sample Input Payload (`sample_timer_event.json`)
```json
{
  "detail-type": "Scheduled Event",
  "source": "aws.events",
  "time": "2026-08-25T00:00:00Z",
  "resources": [
    "arn:aws:events:us-east-1:123456789012:rule/nightly-system-cleanup-rule"
  ]
}
```

---

## 📤 Sample Response Output (`output.json`)
```json
{
  "statusCode": 200,
  "body": {
    "message": "Scheduled cleanup task completed successfully!",
    "metrics": {
      "rule_executed": "nightly-system-cleanup-rule",
      "execution_timestamp": "2026-08-25T00:00:00Z",
      "temp_files_purged": 142,
      "storage_freed_mb": 512.4,
      "status": "COMPLETED",
      "next_scheduled_run": "24 hours"
    }
  }
}
```
