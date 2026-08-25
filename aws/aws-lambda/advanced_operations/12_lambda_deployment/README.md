# 12. Lambda Packaging & Automated Deployment

## 1. Definition
Automated Lambda Deployment packages function source code files (and dependencies) into a `.zip` file artifact and deploys it to the AWS Lambda service via Boto3 API calls (`create_function` / `update_function_code`) or CI/CD build scripts.

## 2. Why Is It Used?
Instead of manually copy-pasting code into the AWS Web Console, automated deployment scripts ensure repeatable, source-controlled, continuous delivery (CD) of serverless code from local development environments and GitHub Actions pipelines.

## 3. AWS Concept
- **Deployment Packaging**: Lambda requires Python handler files to be placed at the root of a `.zip` archive.
- `update_function_code()`: Updates the executable code payload of an existing Lambda function without modifying configuration settings.
- `create_function()`: Provisions a new Lambda function with runtime (`python3.12`), handler pointer (`lambda_function.lambda_handler`), memory, and IAM execution role.

## 4. Prerequisites
- Target function code (`lambda_function.py`).
- IAM permissions: `lambda:CreateFunction`, `lambda:UpdateFunctionCode`, `lambda:InvokeFunction`, `iam:PassRole`.

## 5. Input
- **Function Name**: `MySampleLambdaFunction`
- **Source File**: `lambda_function.py`
- **IAM Role ARN**: `arn:aws:iam::123456789012:role/service-role/MyLambdaExecutionRole`

## 6. Command
```bash
# Package and deploy via Boto3 automated script:
python deploy_script.py --name MySampleLambdaFunction
```

## 7. Expected Output
```text
[INFO] Packaging deployment ZIP archive from 'c:\code\aws\aws-lambda\advanced_operations\12_lambda_deployment\lambda_function.py'...
[SUCCESS] ZIP package generated (428 bytes).
[INFO] Deploying Lambda function 'MySampleLambdaFunction' to region 'us-east-1'...
       [Attempt] Updating existing function code for 'MySampleLambdaFunction'...
[SUCCESS] Function code updated successfully!
         Function ARN: arn:aws:lambda:us-east-1:123456789012:function:MySampleLambdaFunction
         Version:      4
```

## 8. Code
Implemented in [`deploy_script.py`](./deploy_script.py) and [`lambda_function.py`](./lambda_function.py).

## 9. Code Breakdown
- **Line 26–36 in `deploy_script.py`**: Constructs in-memory ZIP buffer using Python `zipfile.ZipFile` module.
- **Line 46–55**: Calls `lambda_client.update_function_code(FunctionName=..., ZipFile=zip_bytes)`.
- **Line 60–73**: Falls back to `lambda_client.create_function(...)` if function does not exist.
- **Line 87–96**: Demonstrates remote execution test via `lambda_client.invoke(...)`.

## 10. Parameter Breakdown
- `ZipFile` *(bytes)*: Raw byte sequence of zip archive containing `lambda_function.py`.
- `Handler` *(string)*: Entrypoint function string (`filename.function_name`).

## 11. AWS CLI Equivalent
```bash
# Package zip via CLI:
zip function.zip lambda_function.py

# Update function code via CLI:
aws lambda update-function-code --function-name MySampleLambdaFunction --zip-file fileb://function.zip
```

## 12. AWS Console Verification
1. Open [AWS Lambda Console](https://console.aws.amazon.com/lambda/).
2. Select `MySampleLambdaFunction`.
3. Open **Code** tab and verify `Last modified` timestamp reflects recent automated update.

## 13. Common Errors
- `InvalidParameterValueException`: Occurs if IAM execution role lacks trust policy allowing `lambda.amazonaws.com` to assume the role.

## 14. Troubleshooting
- Ensure `lambda_function.py` is located at the root of the ZIP file structure and not nested inside a subfolder.

## 15. Security Notes
- Protect IAM deployment credentials using secret environment variables in CI/CD build environments.

## 16. Cleanup
Delete deployed Lambda function:
```bash
aws lambda delete-function --function-name MySampleLambdaFunction
```

## 17. Related Operations
- Previous: [11. Structured Lambda Logging](../11_lambda_logging/README.md)
- Next: [Repository Main Homepage Overview](../../../README.md)
