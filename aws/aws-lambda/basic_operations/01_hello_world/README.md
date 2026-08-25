# 01. Lambda Hello World

## 1. Definition
The Hello World function represents the foundational boilerplate entrypoint signature (`lambda_handler(event, context)`) required by the AWS Lambda Python runtime.

## 2. Why Is It Used?
Every serverless microservice function written for AWS Lambda requires a standardized handler method that receives input data (`event`) and execution runtime metadata (`context`), returning a structured response dictionary.

## 3. AWS Concept
- **Handler**: The entrypoint function in your code that AWS Lambda invokes when triggered (e.g., `lambda_function.lambda_handler`).
- **Event**: JSON-formatted payload containing trigger data.
- **Context**: AWS-provided object exposing execution environment parameters (`aws_request_id`, `function_name`, `get_remaining_time_in_millis()`).
- **Stateless Execution**: Lambda functions run in ephemeral microVM containers (Firecracker) managed automatically by AWS.

## 4. Prerequisites
- Python 3.9+ runtime environment.
- Configured AWS CLI (if deploying to AWS cloud).

## 5. Input
- **Sample Event**: `{"message": "Hello from Local Python Test!", "name": "Cloud Architect"}`

## 6. Command
```bash
# Local Execution Test:
python lambda_function.py
```

## 7. Expected Output
```text
=== LOCAL LAMBDA TEST DRIVER ===
[INFO] Lambda execution initiated.
[LOG] Generated Greeting: 'Hello from Local Python Test! Welcome, Cloud Architect!'

Lambda Response:
{
  "statusCode": 200,
  "headers": {
    "Content-Type": "application/json",
    "X-Custom-Header": "AWS-Lambda-Python"
  },
  "body": "{\"status\": \"success\", \"message\": \"Hello from Local Python Test! Welcome, Cloud Architect!\", \"environment\": \"AWS Lambda Runtime\", \"input_event\": {\"message\": \"Hello from Local Python Test!\", \"name\": \"Cloud Architect\"}}"
}
```

## 8. Code
The function signature is defined in [`lambda_function.py`](./lambda_function.py).

## 9. Code Breakdown
- **Line 10**: Signature `def lambda_handler(event, context):` matching AWS Lambda configuration defaults.
- **Line 20–21**: Safely retrieves keys from dictionary `event` using `.get()`.
- **Line 28–35**: Constructs standard API Gateway proxy response schema containing `statusCode`, `headers`, and JSON-stringified `body`.
- **Line 38–56**: Local test driver mock invoking the handler locally.

## 10. Parameter Breakdown
- `event` *(dict)*: Input event data passed during function invocation.
- `context` *(LambdaContext)*: Object providing runtime status metadata.

## 11. AWS CLI Equivalent
```bash
# Invoke deployed Lambda function via CLI:
aws lambda invoke --function-name HelloFunction --payload '{"name": "Developer"}' response.json
```

## 12. AWS Console Verification
1. Open the [AWS Lambda Console](https://console.aws.amazon.com/lambda/).
2. Create a function named `HelloFunction` using Python 3.12 runtime.
3. Paste contents of `lambda_function.py` into the code editor.
4. Click **Test** -> Configure test event -> Click **Test** to view execution logs in CloudWatch.

## 13. Common Errors
- `Unhandled`: Syntax error or unhandled Exception in Python handler code.
- `ImportModuleError`: Handler name in AWS Console configuration does not match Python file name (`lambda_function.py` vs `index.py`).

## 14. Troubleshooting
- Check that the Handler field in AWS Lambda configuration is set to `lambda_function.lambda_handler`.

## 15. Security Notes
- Lambda function execution is restricted by the IAM Execution Role attached to the function.

## 16. Cleanup
Delete test Lambda function in Console or via CLI: `aws lambda delete-function --function-name HelloFunction`.

## 17. Related Operations
- Next: [02. Lambda Event Handling](../02_lambda_event/README.md)
- Root Lambda Operations: [AWS Lambda Overview](../../README.md)
