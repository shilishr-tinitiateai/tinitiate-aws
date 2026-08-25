# 11. Structured CloudWatch Logging

## 1. Definition
Structured Logging serializes all application log messages into single-line JSON formatted string objects before emitting them to standard output (`stdout`), where AWS Lambda automatically routes them to AWS CloudWatch Logs.

## 2. Why Is It Used?
Structured JSON logs allow development and DevOps teams to run high-speed SQL-like query searches across millions of log records using **CloudWatch Logs Insights** (e.g., querying `@message.level = "ERROR"` or `@message.metadata.user_id = 404`).

## 3. AWS Concept
- **Log Stream Routing**: Anything printed to `sys.stdout` or logged via Python's `logging` module is captured by the Lambda runtime and pushed to `/aws/lambda/<function-name>` in CloudWatch Logs.
- **Log Groups & Streams**: CloudWatch organizes logs into Log Groups (per function) and Log Streams (per container instance execution).

## 4. Prerequisites
- Python 3.9+ runtime.
- IAM permissions: `logs:CreateLogGroup`, `logs:CreateLogStream`, `logs:PutLogEvents`.

## 5. Input
- Sample Event: `{"user_id": 404}`

## 6. Command
```bash
python lambda_function.py
```

## 7. Expected Output
```text
=== LOCAL TEST DRIVER: STRUCTURED LOGGING ===

--- Test 1: Info & Warning Logging ---
INFO:root:{"timestamp_utc": "2026-08-25T12:00:00Z", "level": "INFO", "message": "Lambda execution started", "request_id": "local-request-id", "function_name": "local_logging_function", "metadata": {"input_event": {"user_id": 404}}}
INFO:root:{"timestamp_utc": "2026-08-25T12:00:00Z", "level": "INFO", "message": "Processing completed successfully", "request_id": "local-request-id", "function_name": "local_logging_function", "metadata": {"user_id": 404, "status": "OK"}}

--- Test 2: Error Stack Trace Logging ---
ERROR:root:{"timestamp_utc": "2026-08-25T12:00:00Z", "level": "ERROR", "message": "Execution failed: Simulated runtime error for CloudWatch log tracking!", "request_id": "local-request-id", "function_name": "local_logging_function", "metadata": {"error_type": "ValueError", "stack_trace": "Traceback (most recent call last):\n  File \"...\", line 52, in lambda_handler\n    raise ValueError(...)\nValueError: Simulated runtime error..."}}
```

## 8. Code
Implemented in [`lambda_function.py`](./lambda_function.py).

## 9. Code Breakdown
- **Line 21–35**: `log_structured()` serializes metadata attributes into JSON string representation.
- **Line 47–67**: Emits `INFO`, `WARNING`, and `ERROR` logs with full exception stack trace capture.

## 10. Parameter Breakdown
- `LOG_LEVEL` *(env var)*: Controls logging verbosity (`DEBUG`, `INFO`, `WARNING`, `ERROR`).

## 11. AWS CLI Equivalent
```bash
# Query logs using CloudWatch Logs Insights via CLI:
aws logs start-query --log-group-name /aws/lambda/StructuredLoggingFunction --start-time 1700000000 --end-time 1700003600 --query-string "fields @timestamp, message.level, message.message | filter message.level = 'ERROR'"
```

## 12. AWS Console Verification
1. Open [AWS CloudWatch Console](https://console.aws.amazon.com/cloudwatch/).
2. Click **Logs** -> **Logs Insights**.
3. Select log group `/aws/lambda/StructuredLoggingFunction` and run JSON queries.

## 13. Common Errors
- **Unstructured Multi-line Logs**: Printing raw unformatted multi-line stack traces splits a single exception across multiple separate log entries in CloudWatch, confusing log parsers.

## 14. Troubleshooting
- Set `LOG_LEVEL=DEBUG` in environment variables during troubleshooting, and change to `INFO` or `WARN` in production to optimize CloudWatch ingestion costs.

## 15. Security Notes
- Ensure PII (Personally Identifiable Information) data like credit card numbers or passwords are filtered out before calling `log_structured()`.

## 16. Cleanup
Delete log group in CloudWatch Console.

## 17. Related Operations
- Previous: [10. Lambda IAM Permissions](../10_lambda_permissions/README.md)
- Next: [12. Lambda Packaging & Deployment](../12_lambda_deployment/README.md)
