# 03. Lambda Context Object

## 1. Definition
The `context` object passed to the AWS Lambda handler provides runtime execution metadata and system methods supplied directly by the AWS Lambda execution environment.

## 2. Why Is It Used?
Developers inspect the context object to trace unique request IDs (`aws_request_id`), monitor remaining function timeout execution time (`get_remaining_time_in_millis()`), and log CloudWatch stream identifiers for debugging.

## 3. AWS Concept
- `aws_request_id`: Globally unique identifier assigned to every Lambda invocation call.
- `get_remaining_time_in_millis()`: Returns the number of milliseconds remaining before Lambda hits its configured timeout limit and terminates execution.
- `memory_limit_in_mb`: Allocated RAM configured for the function execution environment (128 MB to 10,240 MB).

## 4. Prerequisites
- Python 3.9+ runtime.

## 5. Input
- Context object passed automatically by AWS Lambda runtime during invocation.

## 6. Command
```bash
python lambda_function.py
```

## 7. Expected Output
```text
=== LOCAL LAMBDA CONTEXT TEST DRIVER ===
[INFO] Inspecting Lambda Context Object...
[LOG] Context Details:
{
  "function_name": "ContextInspectionFunction",
  "function_version": "$LATEST",
  "invoked_function_arn": "arn:aws:lambda:us-east-1:123456789012:function:ContextInspectionFunction",
  "memory_limit_in_mb": 512,
  "aws_request_id": "c6b4192b-8a71-469b-8919-abcdef123456",
  "log_group_name": "/aws/lambda/ContextInspectionFunction",
  "log_stream_name": "2026/08/25/[$LATEST]a1b2c3d4e5f6",
  "remaining_time_ms_start": 30000,
  "remaining_time_ms_after_work": 29949
}

Handler Response:
{
  "statusCode": 200,
  "headers": {
    "Content-Type": "application/json"
  },
  "body": "{\"status\": \"success\", \"context_metadata\": {\"function_name\": \"ContextInspectionFunction\", \"function_version\": \"$LATEST\", \"invoked_function_arn\": \"arn:aws:lambda:us-east-1:123456789012:function:ContextInspectionFunction\", \"memory_limit_in_mb\": 512, \"aws_request_id\": \"c6b4192b-8a71-469b-8919-abcdef123456\", \"log_group_name\": \"/aws/lambda/ContextInspectionFunction\", \"log_stream_name\": \"2026/08/25/[$LATEST]a1b2c3d4e5f6\", \"remaining_time_ms_start\": 30000, \"remaining_time_ms_after_work\": 29949}}"
}
```

## 8. Code
The operation is implemented in [`lambda_function.py`](./lambda_function.py).

## 9. Code Breakdown
- **Line 20–28**: Safely reads context properties using Python `getattr()` to prevent AttributeError when testing locally.
- **Line 31–34**: Calls `context.get_remaining_time_in_millis()` to measure execution time consumption.

## 10. Parameter Breakdown
- `aws_request_id` *(string)*: Unique identifier for invocation tracing.
- `function_name` *(string)*: Name of the executed Lambda function.
- `memory_limit_in_mb` *(int)*: Allocated memory limit.

## 11. AWS CLI Equivalent
```bash
# View log stream and request ID details via CloudWatch CLI:
aws logs tail /aws/lambda/ContextInspectionFunction --follow
```

## 12. AWS Console Verification
1. Open [AWS Lambda Console](https://console.aws.amazon.com/lambda/).
2. Execute test invocation -> Expand **Details** section under **Execution result** to view Request ID, Billed Duration, and Max Memory Used.

## 13. Common Errors
- `AttributeError`: Occurs when accessing context attributes directly without checking existence when running outside the AWS environment.

## 14. Troubleshooting
- Use `get_remaining_time_in_millis()` inside long loops to perform graceful shutdown before Lambda encounters a hard timeout cutoff.

## 15. Security Notes
- `aws_request_id` is useful for correlating distributed application logs in CloudWatch or AWS X-Ray without logging sensitive PII data.

## 16. Cleanup
No special cleanup required.

## 17. Related Operations
- Previous: [02. Lambda Event Payload Parsing](../02_lambda_event/README.md)
- Next: [04. Environment Variables](../04_environment_variables/README.md)
