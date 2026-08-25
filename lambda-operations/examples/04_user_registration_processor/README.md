# 👤 Example 4: User Registration Data Validator & Processor

Welcome to **Example 4**! This beginner-friendly guide demonstrates how AWS Lambda validates input data payloads and generates structured user profile records.

---

## 🎯 What Does This Example Do?

1. Client sends user registration data (`username`, `email`, `role`) to Lambda.
2. Lambda validates required fields (checking email `@` symbol and minimum username length).
3. If valid, Lambda generates a unique `user_id` (e.g. `USR-A1B2C3D4`), appends ISO timestamps, and returns HTTP 201 Created user metadata.

---

## 📁 File Structure

* [`lambda_function.py`](file:///c:/code/aws-s3-and-lmbda-operations/lambda-operations/examples/04_user_registration_processor/lambda_function.py): Python Lambda function handler.
* [`user_payload.json`](file:///c:/code/aws-s3-and-lmbda-operations/lambda-operations/examples/04_user_registration_processor/user_payload.json): Input user registration JSON payload.
* [`run_example.py`](file:///c:/code/aws-s3-and-lmbda-operations/lambda-operations/examples/04_user_registration_processor/run_example.py): Automated Boto3 deployment & execution runner.

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
Compress-Archive -Path lambda_function.py -DestinationPath user_func.zip -Force

# Linux / macOS Bash
zip user_func.zip lambda_function.py
```

#### Step 2: Create the Lambda function
```bash
aws lambda create-function \
  --function-name user-registration-processor-example \
  --runtime python3.12 \
  --role arn:aws:iam::123456789012:role/lambda-role \
  --handler lambda_function.lambda_handler \
  --zip-file fileb://user_func.zip \
  --endpoint-url http://localhost:4566
```

#### Step 3: Invoke the function with user payload
```bash
# Windows PowerShell
aws lambda invoke `
  --function-name user-registration-processor-example `
  --payload file://user_payload.json `
  --cli-binary-format raw-in-base64-out `
  output.json `
  --endpoint-url http://localhost:4566

# Linux / macOS Bash
aws lambda invoke \
  --function-name user-registration-processor-example \
  --payload file://user_payload.json \
  --cli-binary-format raw-in-base64-out \
  output.json \
  --endpoint-url http://localhost:4566
```

---

## 📥 Sample Input Payload (`user_payload.json`)
```json
{
  "username": "alex_developer",
  "email": "alex.developer@example.com",
  "role": "ADMIN"
}
```

---

## 📤 Sample Response Output (`output.json`)
```json
{
  "statusCode": 201,
  "headers": {
    "Content-Type": "application/json"
  },
  "body": {
    "status": "USER_CREATED",
    "message": "User 'alex_developer' registered successfully!",
    "user": {
      "user_id": "USR-9F8E7D6C",
      "username": "alex_developer",
      "email": "alex.developer@example.com",
      "role": "ADMIN",
      "account_status": "ACTIVE",
      "created_at": "2026-08-25T16:42:00.000Z"
    }
  }
}
```
