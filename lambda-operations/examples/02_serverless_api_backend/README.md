# 🌐 Example 2: Serverless REST API Backend (API Gateway Proxy)

Welcome to **Example 2**! This guide demonstrates how AWS Lambda functions act as backend HTTP endpoints behind **AWS API Gateway**.

---

## 🎯 What Does This Example Do?

1. An HTTP request arrives from a mobile app, web browser, or Postman to `/products?category=electronics`.
2. **API Gateway** passes the HTTP method (`GET`), query parameters (`category=electronics`), and headers to Lambda as a JSON payload.
3. Lambda processes the parameters, filters product items, and returns an HTTP response object containing `statusCode`, `headers`, and JSON string `body`.

---

## 📁 File Structure

* [`lambda_function.py`](file:///c:/code/aws-s3-and-lmbda-operations/lambda-operations/examples/02_serverless_api_backend/lambda_function.py): Python Lambda function handler.
* [`sample_api_request.json`](file:///c:/code/aws-s3-and-lmbda-operations/lambda-operations/examples/02_serverless_api_backend/sample_api_request.json): Realistic API Gateway GET HTTP request payload.
* [`run_example.py`](file:///c:/code/aws-s3-and-lmbda-operations/lambda-operations/examples/02_serverless_api_backend/run_example.py): Automated Boto3 runner script.

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
Compress-Archive -Path lambda_function.py -DestinationPath api_func.zip -Force

# Linux / macOS Bash
zip api_func.zip lambda_function.py
```

#### Step 2: Create the Lambda function
```bash
aws lambda create-function \
  --function-name serverless-api-backend-example \
  --runtime python3.12 \
  --role arn:aws:iam::123456789012:role/lambda-role \
  --handler lambda_function.lambda_handler \
  --zip-file fileb://api_func.zip \
  --endpoint-url http://localhost:4566
```

#### Step 3: Invoke the function with API Gateway request payload
```bash
# Windows PowerShell
aws lambda invoke `
  --function-name serverless-api-backend-example `
  --payload file://sample_api_request.json `
  --cli-binary-format raw-in-base64-out `
  output.json `
  --endpoint-url http://localhost:4566

# Linux / macOS Bash
aws lambda invoke \
  --function-name serverless-api-backend-example \
  --payload file://sample_api_request.json \
  --cli-binary-format raw-in-base64-out \
  output.json \
  --endpoint-url http://localhost:4566
```

---

## 📥 Sample Input Payload (`sample_api_request.json`)
```json
{
  "httpMethod": "GET",
  "path": "/products",
  "queryStringParameters": {
    "category": "electronics"
  }
}
```

---

## 📤 Sample Response Output (`output.json`)
```json
{
  "statusCode": 200,
  "headers": {
    "Content-Type": "application/json",
    "Access-Control-Allow-Origin": "*",
    "X-Powered-By": "AWS-Lambda-Serverless"
  },
  "body": "{\"status\": \"SUCCESS\", \"message\": \"Retrieved products for category 'electronics'\", \"count\": 2, \"data\": [{\"id\": 101, \"name\": \"Wireless Headphones\", \"category\": \"electronics\", \"price\": 99.99}, {\"id\": 102, \"name\": \"Ergonomic Keyboard\", \"category\": \"electronics\", \"price\": 49.99}]}"
}
```
