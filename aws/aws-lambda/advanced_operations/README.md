# AWS Lambda Advanced Operations

This module covers advanced AWS Lambda architectures, including shared layer packaging, IAM permission boundaries, structured CloudWatch logging, and automated deployment script pipelines.

---

## Operations Map

| # | Operation | Script | Documentation | Description |
|---|---|---|---|---|
| 09 | **Lambda Layers** | [`lambda_function.py`](./09_lambda_layers/lambda_function.py), [`layer_helper.py`](./09_lambda_layers/layer_helper.py) | [README](./09_lambda_layers/README.md) | Package and consume shared helper libraries mounted at `/opt/python`. |
| 10 | **Lambda Permissions** | [`lambda_function.py`](./10_lambda_permissions/lambda_function.py) | [README](./10_lambda_permissions/README.md) | Audit IAM execution role permissions and enforce least privilege principles. |
| 11 | **Lambda Logging** | [`lambda_function.py`](./11_lambda_logging/lambda_function.py) | [README](./11_lambda_logging/README.md) | Configure structured JSON logging for CloudWatch Logs & Logs Insights querying. |
| 12 | **Lambda Deployment** | [`deploy_script.py`](./12_lambda_deployment/deploy_script.py), [`lambda_function.py`](./12_lambda_deployment/lambda_function.py) | [README](./12_lambda_deployment/README.md) | Automated Boto3 in-memory ZIP packaging and cloud deployment pipeline. |

---

## Suggested Progression
Execute operations sequentially from `09_lambda_layers` to `12_lambda_deployment` to master advanced serverless deployment patterns.
