"""
AWS Lambda Operation 01: Hello World

Demonstrates standard AWS Lambda handler structure, event payload processing,
context object inspection, and status code 200 HTTP response formatting.
"""

import json
from typing import Dict, Any


def lambda_handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """
    AWS Lambda Function Entrypoint Handler.

    :param event: AWS event dictionary (e.g. API Gateway HTTP payload, S3 trigger, or custom JSON).
    :param context: Runtime context object containing metadata (function name, request ID, memory limit).
    :return: Formatted API Gateway proxy integration dictionary response.
    """
    print("[INFO] Lambda execution initiated.")
    
    # Extract greeting message or fallback default
    message = event.get("message", "Hello World from AWS Lambda!")
    name = event.get("name", "Developer")

    greeting = f"{message} Welcome, {name}!"
    print(f"[LOG] Generated Greeting: '{greeting}'")

    response_body = {
        "status": "success",
        "message": greeting,
        "environment": "AWS Lambda Runtime",
        "input_event": event
    }

    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json",
            "X-Custom-Header": "AWS-Lambda-Python"
        },
        "body": json.dumps(response_body)
    }


# Local Test Execution Driver
if __name__ == "__main__":
    print("=== LOCAL LAMBDA TEST DRIVER ===")
    
    # Mock Event Payload
    sample_event = {
        "message": "Hello from Local Python Test!",
        "name": "Cloud Architect"
    }

    # Mock Context Object
    class MockContext:
        function_name = "local_hello_world_test"
        function_version = "$LATEST"
        aws_request_id = "test-req-12345-67890"
        memory_limit_in_mb = 128

        def get_remaining_time_in_millis(self):
            return 30000

    result = lambda_handler(event=sample_event, context=MockContext())
    print("\nLambda Response:")
    print(json.dumps(result, indent=2))
