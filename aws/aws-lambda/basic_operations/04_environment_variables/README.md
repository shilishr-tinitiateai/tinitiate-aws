# 04. Lambda Environment Variables

## 1. Definition
Environment variables allow developers to pass dynamic configuration settings (such as S3 bucket names, log levels, API endpoints, or feature flags) to an AWS Lambda function without modifying source code.

## 2. Why Is It Used?
Environment variables separate code from configuration. The exact same Lambda package zip artifact can be deployed across Development, Staging, and Production environments simply by modifying environment variable parameters.

## 3. AWS Concept
- `os.environ`: Standard Python module to access runtime environment variables.
- **KMS Encryption**: AWS Lambda automatically encrypts environment variables at rest using AWS Key Management Service (KMS).

## 4. Prerequisites
- Python 3.9+ runtime.

## 5. Input
- **Environment Variables**: `APP_ENV=production`, `LOG_LEVEL=DEBUG`, `S3_BUCKET_NAME=my-prod-bucket`

## 6. Command
```bash
python lambda_function.py
```

## 7. Expected Output
```text
=== LOCAL TEST DRIVER: ENVIRONMENT VARIABLES ===
[INFO] Fetching runtime configuration from environment variables...
[LOG] Loaded Configuration: {"app_env": "production", "log_level": "DEBUG", "s3_bucket_name": "my-production-lambda-bucket-12345", "api_key_status": "configured", "masked_api_key": "secr****"}

Handler Response:
{
  "statusCode": 200,
  "headers": {
    "Content-Type": "application/json"
  },
  "body": "{\"status\": \"success\", \"runtime_config\": {\"app_env\": \"production\", \"log_level\": \"DEBUG\", \"s3_bucket_name\": \"my-production-lambda-bucket-12345\", \"api_key_status\": \"configured\", \"masked_api_key\": \"secr****\"}}"
}
```

## 8. Code
The operation is implemented in [`lambda_function.py`](./lambda_function.py).

## 9. Code Breakdown
- **Line 16–19**: Reads `os.environ.get("KEY", "default")` with fallback defaults.
- **Line 22**: Masks sensitive string prefixes for safe logging output.

## 10. Parameter Breakdown
- `APP_ENV` *(string)*: Deployment environment string.
- `S3_BUCKET_NAME` *(string)*: Target S3 bucket name.

## 11. AWS CLI Equivalent
```bash
# Update Lambda environment variables via AWS CLI:
aws lambda update-function-configuration --function-name ConfigFunction --environment "Variables={APP_ENV=production,LOG_LEVEL=DEBUG,S3_BUCKET_NAME=my-prod-bucket}"
```

## 12. AWS Console Verification
1. Open [AWS Lambda Console](https://console.aws.amazon.com/lambda/).
2. Select your function and open the **Configuration** tab.
3. Click **Environment variables** section to view or edit key-value pairs.

## 13. Common Errors
- `KeyError`: Occurs if accessing `os.environ["KEY"]` directly when the environment variable is not defined. Always use `os.environ.get("KEY", "default")`.

## 14. Troubleshooting
- For highly sensitive secrets (database passwords, private keys), use **AWS Secrets Manager** or **AWS Systems Manager Parameter Store** instead of plain environment variables.

## 15. Security Notes
- Never log unmasked API secrets, database passwords, or auth tokens to CloudWatch Logs.

## 16. Cleanup
No special cleanup required.

## 17. Related Operations
- Previous: [03. Lambda Context Object](../03_lambda_context/README.md)
- Next: [05. Error Handling](../05_error_handling/README.md)
