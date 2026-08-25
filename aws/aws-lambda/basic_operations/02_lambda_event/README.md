# 02. Lambda Event Payload Parsing

## 1. Definition
The `event` parameter passed to an AWS Lambda handler is a JSON object containing all request data sent by the initiating trigger service (API Gateway, S3, EventBridge, SQS, or direct SDK invocations).

## 2. Why Is It Used?
Applications use event parsing to extract HTTP headers, query string parameters, POST bodies, path parameters, or event records to route logic dynamically within serverless functions.

## 3. AWS Concept
- **Event Schema Flexibility**: AWS Lambda does not impose a static event schema. The JSON format varies based on the invoking AWS service integration.
- **Proxy Integrations**: API Gateway passes raw HTTP requests wrapped inside standard proxy schema dictionaries.

## 4. Prerequisites
- Python 3.9+ runtime.

## 5. Input
- **API Gateway Event Payload**: `{"httpMethod": "POST", "path": "/api/v1/users", "body": "{\"user_id\": 42}"}`

## 6. Command
```bash
python lambda_function.py
```

## 7. Expected Output
```text
=== LOCAL TEST DRIVER: API GATEWAY EVENT ===
[INFO] Processing event payload of size 225 bytes.
[LOG] Event Analysis: {"trigger_type": "API Gateway HTTP Proxy", "http_method": "POST", "path": "/api/v1/users", "query_parameters": {"status": "active", "page": "1"}, "user_agent": "Mozilla/5.0 (Windows NT 10.0)", "parsed_body": {"user_id": 42, "email": "dev@example.com"}}

Lambda Response:
{
  "statusCode": 200,
  "headers": {
    "Content-Type": "application/json"
  },
  "body": "{\"status\": \"success\", \"event_summary\": {\"trigger_type\": \"API Gateway HTTP Proxy\", \"http_method\": \"POST\", \"path\": \"/api/v1/users\", \"query_parameters\": {\"status\": \"active\", \"page\": \"1\"}, \"user_agent\": \"Mozilla/5.0 (Windows NT 10.0)\", \"parsed_body\": {\"user_id\": 42, \"email\": \"dev@example.com\"}}}"
}
```

## 8. Code
The operation is implemented in [`lambda_function.py`](./lambda_function.py).

## 9. Code Breakdown
- **Line 11–38**: `parse_event()` checks keys to determine whether event originates from API Gateway or a direct SDK call.
- **Line 22–26**: Parses stringified `event['body']` into a Python dictionary via `json.loads()`.

## 10. Parameter Breakdown
- `queryStringParameters` *(dict)*: Key-value map of URL query strings (`?page=1`).
- `pathParameters` *(dict)*: Key-value map of path routing variables (`/users/{id}`).

## 11. AWS CLI Equivalent
```bash
aws lambda invoke --function-name ParseEventFunction --payload '{"httpMethod": "GET", "path": "/status"}' response.json
```

## 12. AWS Console Verification
1. Open [AWS Lambda Console](https://console.aws.amazon.com/lambda/).
2. Select function -> Click **Test** tab -> Choose **apigateway-aws-proxy** template to test API Gateway event processing.

## 13. Common Errors
- `json.decoder.JSONDecodeError`: Occurs when trying to call `json.loads()` on an unquoted or malformed event body string.

## 14. Troubleshooting
- Always handle non-string or `None` values for `queryStringParameters` or `headers` gracefully.

## 15. Security Notes
- Validate and sanitize input parameters extracted from event payloads before using in database queries to prevent injection attacks.

## 16. Cleanup
No special cleanup required.

## 17. Related Operations
- Previous: [01. Hello World](../01_hello_world/README.md)
- Next: [03. Lambda Context Object](../03_lambda_context/README.md)
