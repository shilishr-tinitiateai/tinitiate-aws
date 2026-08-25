# AWS Lambda Basic Operations

This module covers foundational serverless development concepts using Python in AWS Lambda.

---

## Operations Map

| # | Operation | Script | Documentation | Description |
|---|---|---|---|---|
| 01 | **Hello World** | [`lambda_function.py`](./01_hello_world/lambda_function.py) | [README](./01_hello_world/README.md) | Standard Lambda handler signature, response schema, and local test driver. |
| 02 | **Event Payload Parsing** | [`lambda_function.py`](./02_lambda_event/lambda_function.py) | [README](./02_lambda_event/README.md) | Parse API Gateway HTTP events, query params, headers, and direct JSON events. |
| 03 | **Context Object Inspection** | [`lambda_function.py`](./03_lambda_context/lambda_function.py) | [README](./03_lambda_context/README.md) | Inspect request ID, memory allocation, log groups, and remaining runtime. |
| 04 | **Environment Variables** | [`lambda_function.py`](./04_environment_variables/lambda_function.py) | [README](./04_environment_variables/README.md) | Read runtime configuration parameters via `os.environ` securely. |
| 05 | **Error Handling** | [`lambda_function.py`](./05_error_handling/lambda_function.py) | [README](./05_error_handling/README.md) | Handle custom exceptions, map status codes (400/422/500), and format error responses. |

---

## Suggested Progression
Execute operations sequentially from `01_hello_world` to `05_error_handling` to master core AWS Lambda handler concepts.
