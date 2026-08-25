# 09. AWS Lambda Layers

## 1. Definition
AWS Lambda Layers are `.zip` archives containing external dependencies, custom heavy libraries (e.g. `boto3`, `requests`, `pandas`), custom runtimes, or shared code modules mounted under `/opt` in the Lambda execution environment.

## 2. Why Is It Used?
Lambda Layers separate core application business logic from heavy third-party dependencies, drastically reducing deployment ZIP package sizes (from 50 MB down to 5 KB), speeding up deployment build times, and promoting code reuse across multiple Lambda functions.

## 3. AWS Concept
- `/opt`: The directory where AWS Lambda unzips and mounts attached layers.
- Python Layer Directory Structure: Third-party packages or shared helper modules must be placed inside a `python/` directory inside the Layer zip file (e.g., `python/layer_helper.py` or `python/lib/python3.12/site-packages/`).

## 4. Prerequisites
- Python 3.9+ runtime.
- AWS CLI (for publishing layer versions).

## 5. Input
- Shared helper module: `layer_helper.py`

## 6. Command
```bash
# Local Execution Test:
python lambda_function.py
```

## 7. Expected Output
```text
=== LOCAL TEST DRIVER: LAMBDA LAYERS ===
[INFO] Invoking Lambda function with Layer dependency...
[LOG] Result produced by Layer: {"statusCode": 200, "headers": {"Content-Type": "application/json", "X-Layer-Version": "1.0.0"}, "body": {"status": "success", "message": "Successfully processed user request using Lambda Layer helper!", "layer_metadata": {"shared_library": "layer_helper.py", "version": "1.0.0"}, "data": {"user_id": 202, "role": "Cloud Architect", "permissions": ["s3:Read", "lambda:Invoke"]}}}

Handler Response:
{
  "statusCode": 200,
  "headers": {
    "Content-Type": "application/json",
    "X-Layer-Version": "1.0.0"
  },
  "body": "{\"status\": \"success\", \"message\": \"Successfully processed user request using Lambda Layer helper!\", \"layer_metadata\": {\"shared_library\": \"layer_helper.py\", \"version\": \"1.0.0\"}, \"data\": {\"user_id\": 202, \"role\": \"Cloud Architect\", \"permissions\": [\"s3:Read\", \"lambda:Invoke\"]}}"
}
```

## 8. Code
Implemented in [`layer_helper.py`](./layer_helper.py) and [`lambda_function.py`](./lambda_function.py).

## 9. Code Breakdown
- **Line 12–18 in `lambda_function.py`**: Imports `layer_helper` from `/opt/python` path with local fallback.
- **Line 14 in `layer_helper.py`**: Exports `format_response_payload()` helper function across Lambda executions.

## 10. Parameter Breakdown
- `/opt/python`: Default Python module import search path automatically added to `sys.path` by AWS Lambda runtime.

## 11. AWS CLI Equivalent
```bash
# Package layer zip structure:
zip -r my_layer.zip python/

# Publish layer version to AWS:
aws lambda publish-layer-version --layer-name SharedHelperLayer --zip-file fileb://my_layer.zip --compatible-runtimes python3.12
```

## 12. AWS Console Verification
1. Open [AWS Lambda Console](https://console.aws.amazon.com/lambda/).
2. Click **Layers** -> Create layer -> Upload `my_layer.zip`.
3. Open your function -> Scroll to **Layers** section -> Click **Add a layer** -> Choose custom layer.

## 13. Common Errors
- `Unable to import module 'lambda_function'`: Occurs if directory structure inside the Layer zip is incorrect (e.g. missing top-level `python/` folder).

## 14. Troubleshooting
- Ensure compiled C-extension packages (e.g. `numpy`, `pandas`) are compiled inside a Linux environment matching the AWS Lambda execution architecture (x86_64 or arm64).

## 15. Security Notes
- Monitor attached layer version ARNs to ensure outdated third-party library versions are updated across functions.

## 16. Cleanup
Delete published layer version: `aws lambda delete-layer-version --layer-name SharedHelperLayer --version-number 1`.

## 17. Related Operations
- Previous: [S3 Integration Overview](../../s3_integration/README.md)
- Next: [10. Lambda IAM Permissions](../10_lambda_permissions/README.md)
