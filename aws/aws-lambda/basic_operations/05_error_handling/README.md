# 05. Lambda Error Handling

## 1. Definition
Error handling in AWS Lambda captures custom runtime exceptions, maps business errors to HTTP status codes (400, 422, 500), and outputs structured JSON error responses.

## 2. Why Is It Used?
Unhandled exceptions in Lambda cause functions to fail abruptly, logging stack trace errors to CloudWatch and causing API Gateway to return generic HTTP 502 Bad Gateway errors. Graceful error handling returns actionable diagnostic feedback to clients.

## 3. AWS Concept
- **Handled Errors**: Exceptions caught inside `try/except` blocks in `lambda_handler`, returning a structured response dictionary.
- **Unhandled Errors**: Uncaught exceptions where Python crashes. Lambda logs `[ERROR] Task timed out` or `Runtime.UnhandledException` to CloudWatch and increments the CloudWatch `Errors` metric.

## 4. Prerequisites
- Python 3.9+ runtime.

## 5. Input
- **Valid Order**: `{"order_id": "ORD-101", "amount": 150.75}`
- **Invalid Payload**: `{"amount": 50.0}` (Missing `order_id`)

## 6. Command
```bash
python lambda_function.py
```

## 7. Expected Output
```text
=== TEST 1: SUCCESSFUL EXECUTION ===
[INFO] Processing request event: {"order_id": "ORD-101", "amount": 150.75}
[SUCCESS] Order processed: {'order_id': 'ORD-101', 'status': 'PROCESSED', 'total_amount': 150.75}

=== TEST 2: INVALID PAYLOAD (HTTP 400) ===
[INFO] Processing request event: {"amount": 50.0}
[WARNING] Validation Error: Missing mandatory field 'order_id' in event payload.
{
  "statusCode": 400,
  "headers": {
    "Content-Type": "application/json"
  },
  "body": "{\"status\": \"error\", \"error_type\": \"InvalidPayloadException\", \"message\": \"Missing mandatory field 'order_id' in event payload.\"}"
}
```

## 8. Code
The operation is implemented in [`lambda_function.py`](./lambda_function.py).

## 9. Code Breakdown
- **Line 10–16**: Defines custom exception classes (`InvalidPayloadException`, `BusinessLogicException`).
- **Line 46–85**: Catches specific exception types in `lambda_handler` returning custom HTTP 400/422/500 JSON bodies.

## 10. Parameter Breakdown
- `statusCode` *(int)*: HTTP status code (`200` OK, `400` Bad Request, `422` Unprocessable Entity, `500` Internal Error).

## 11. AWS CLI Equivalent
```bash
# Invoke Lambda and inspect FunctionError field:
aws lambda invoke --function-name ErrorHandlingFunction --payload '{"amount": -5}' response.json
```

## 12. AWS Console Verification
1. Open [AWS Lambda Console](https://console.aws.amazon.com/lambda/).
2. Open **Monitor** tab -> View **Error count and success rate (%)** CloudWatch metrics dashboard.

## 13. Common Errors
- `Runtime.UnhandledException`: Occurs when an uncaught exception escapes the handler.

## 14. Troubleshooting
- Inspect `traceback.format_exc()` output in CloudWatch logs to diagnose the exact root cause line for unhandled 500 errors.

## 15. Security Notes
- Avoid returning raw database exception stack traces directly in client response bodies to prevent internal architecture disclosure.

## 16. Cleanup
No special cleanup required.

## 17. Related Operations
- Previous: [04. Environment Variables](../04_environment_variables/README.md)
- Next: [S3 Integration Overview](../../s3_integration/README.md)
