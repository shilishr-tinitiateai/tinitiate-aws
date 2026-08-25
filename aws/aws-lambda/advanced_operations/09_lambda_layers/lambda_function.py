"""
AWS Lambda Operation 09: Lambda Layers Integration

Demonstrates consuming shared library modules provided by AWS Lambda Layers (/opt/python).
Includes fallback local import handling for cross-platform local execution and testing.
"""

import sys
import json
from pathlib import Path
from typing import Dict, Any

# Attempt to import shared layer helper from AWS Lambda Layer path (/opt/python) or local directory
try:
    # In AWS Lambda runtime with attached layer, layers mount under /opt/python
    sys.path.append("/opt/python")
    from layer_helper import format_response_payload
except ImportError:
    # Fallback to local import for local machine testing
    from layer_helper import format_response_payload


def lambda_handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """
    AWS Lambda Handler Entrypoint consuming Layer dependencies.
    """
    print("[INFO] Invoking Lambda function with Layer dependency...")

    sample_user_data = {
        "user_id": event.get("user_id", 101),
        "role": "Cloud Architect",
        "permissions": ["s3:Read", "lambda:Invoke"]
    }

    # Consume function exported by the attached Lambda Layer
    formatted_result = format_response_payload(
        data=sample_user_data,
        status_code=200,
        message="Successfully processed user request using Lambda Layer helper!"
    )

    print(f"[LOG] Result produced by Layer: {json.dumps(formatted_result)}")

    return {
        "statusCode": formatted_result["statusCode"],
        "headers": formatted_result["headers"],
        "body": json.dumps(formatted_result["body"])
    }


if __name__ == "__main__":
    print("=== LOCAL TEST DRIVER: LAMBDA LAYERS ===")
    res = lambda_handler(event={"user_id": 202}, context=None)
    print("\nHandler Response:")
    print(json.dumps(res, indent=2))
