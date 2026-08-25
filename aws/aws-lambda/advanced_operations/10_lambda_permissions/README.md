# 10. Lambda IAM Execution Roles & Permissions

## 1. Definition
An AWS Lambda Execution Role is an IAM role that grants your serverless function permissions to securely access AWS resources (such as S3 buckets, CloudWatch Logs, DynamoDB tables, or KMS keys).

## 2. Why Is It Used?
By default, an AWS Lambda function has zero permissions to access any external AWS service. Attaching a least-privilege IAM Execution Role ensures functions only execute authorized API actions on specific resources.

## 3. AWS Concept
- **Execution Role**: IAM Role assumed by the Lambda runtime environment when executing function code (`sts:AssumeRole`).
- **AWSLambdaBasicExecutionRole**: Managed IAM policy granting basic CloudWatch log writing permissions (`logs:CreateLogGroup`, `logs:CreateLogStream`, `logs:PutLogEvents`).
- **Least Privilege**: Restricting IAM policy statements to explicit S3 bucket ARNs rather than wildcard `Resource: "*"` statements.

## 4. Prerequisites
- Configured IAM Execution Role in AWS Account.

## 5. Input
- Target S3 Bucket: `my-learning-s3-bucket-unique-12345`

## 6. Command
```bash
python lambda_function.py
```

## 7. Expected Output
```text
=== LOCAL TEST DRIVER: LAMBDA PERMISSIONS AUDIT ===
[INFO] Auditing IAM Execution Role permissions for S3 bucket 'test-audit-bucket'...
[PERMISSION SUCCESS] s3:ListBucket granted on bucket 'test-audit-bucket'.
[PERMISSION DENIED] s3:PutObject denied on bucket 'test-audit-bucket'.

Audit Response:
{
  "statusCode": 200,
  "headers": {
    "Content-Type": "application/json"
  },
  "body": "{\"status\": \"audit_complete\", \"permissions\": {\"bucket\": \"test-audit-bucket\", \"s3:ListBucket\": \"ALLOWED\", \"s3:PutObject\": \"DENIED (Missing s3:PutObject IAM action)\"}}"
}
```

## 8. Code
Implemented in [`lambda_function.py`](./lambda_function.py).

## 9. Code Breakdown
- **Line 26–36**: Tests `s3:ListBucket` permission and catches `AccessDenied` exception.
- **Line 39–50**: Tests `s3:PutObject` write permission independently.

## 10. Parameter Breakdown
- `s3:GetObject` *(IAM Action)*: Permission to read object data.
- `s3:PutObject` *(IAM Action)*: Permission to write object data.

## 11. AWS Minimum Policy Document
Below is the minimal least-privilege JSON policy document required for an S3-processing Lambda function:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "logs:CreateLogGroup",
        "logs:CreateLogStream",
        "logs:PutLogEvents"
      ],
      "Resource": "arn:aws:logs:*:*:*"
    },
    {
      "Effect": "Allow",
      "Action": [
        "s3:GetObject",
        "s3:PutObject"
      ],
      "Resource": "arn:aws:s3:::my-learning-s3-bucket-unique-12345/*"
    }
  ]
}
```

## 12. AWS Console Verification
1. Open [AWS Lambda Console](https://console.aws.amazon.com/lambda/).
2. Select your function -> Open **Configuration** tab -> Click **Permissions** section.
3. Click the Execution Role link to open the IAM console and view attached policy statements.

## 13. Common Errors
- `AccessDeniedException`: Lambda execution role lacks necessary IAM policy action.

## 14. Troubleshooting
- Avoid attaching `AdministratorAccess` or `AmazonS3FullAccess` to production Lambda functions. Grant minimum specific bucket access.

## 15. Security Notes
- Regularly review IAM execution roles using AWS IAM Access Analyzer.

## 16. Cleanup
Delete custom IAM role in IAM console when function is deleted.

## 17. Related Operations
- Previous: [09. Lambda Layers](../09_lambda_layers/README.md)
- Next: [11. Structured Lambda Logging](../11_lambda_logging/README.md)
