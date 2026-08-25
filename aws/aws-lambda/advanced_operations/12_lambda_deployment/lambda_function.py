"""
AWS Lambda Operation 12: Target Production Function Code

This file represents the production lambda function code to be packaged into a ZIP archive
and deployed to AWS Lambda programmatically via deploy_script.py.
"""

import json
from typing import Dict, Any


def lambda_handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """
    Deployed AWS Lambda Function Handler.
    """
    print("[INFO] Deployed Lambda Function executing in AWS Cloud environment.")

    action = event.get("action", "default_status")
    
    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json",
            "X-Deployment-Method": "Boto3-Automated-Script"
        },
        "body": json.dumps({
            "status": "active",
            "message": "Hello from automated Boto3-deployed AWS Lambda function!",
            "received_action": action
        })
    }


if __name__ == "__main__":
    print("=== LOCAL TEST EXECUTION ===")
    res = lambda_handler(event={"action": "local_dry_run"}, context=None)
    print(json.dumps(res, indent=2))
