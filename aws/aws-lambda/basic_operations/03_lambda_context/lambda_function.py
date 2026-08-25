"""
AWS Lambda Operation 03: Context Object Inspection

Demonstrates inspecting execution metadata from the AWS Lambda context object,
including remaining runtime execution time, memory allocation, request IDs, and CloudWatch log groups.
"""

import json
import time
from typing import Dict, Any


def inspect_context(context: Any) -> Dict[str, Any]:
    """
    Extracts metadata properties from the AWS Lambda context object.

    :param context: LambdaContext runtime object.
    :return: Dictionary containing extracted metadata properties.
    """
    if not context:
        return {"status": "No context provided (Local execution without mock)"}

    # Extract metadata properties safely
    info = {
        "function_name": getattr(context, "function_name", "N/A"),
        "function_version": getattr(context, "function_version", "N/A"),
        "invoked_function_arn": getattr(context, "invoked_function_arn", "N/A"),
        "memory_limit_in_mb": getattr(context, "memory_limit_in_mb", "N/A"),
        "aws_request_id": getattr(context, "aws_request_id", "N/A"),
        "log_group_name": getattr(context, "log_group_name", "N/A"),
        "log_stream_name": getattr(context, "log_stream_name", "N/A"),
    }

    # Calculate remaining execution time if method exists
    if hasattr(context, "get_remaining_time_in_millis"):
        info["remaining_time_ms_start"] = context.get_remaining_time_in_millis()
        time.sleep(0.05) # Simulate minor computation work
        info["remaining_time_ms_after_work"] = context.get_remaining_time_in_millis()

    return info


def lambda_handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """
    AWS Lambda Handler Entrypoint.
    """
    print("[INFO] Inspecting Lambda Context Object...")

    context_details = inspect_context(context)
    print(f"[LOG] Context Details:\n{json.dumps(context_details, indent=2)}")

    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps({
            "status": "success",
            "context_metadata": context_details
        })
    }


if __name__ == "__main__":
    print("=== LOCAL LAMBDA CONTEXT TEST DRIVER ===")

    # Mock AWS Lambda Context Object
    class MockLambdaContext:
        function_name = "ContextInspectionFunction"
        function_version = "$LATEST"
        invoked_function_arn = "arn:aws:lambda:us-east-1:123456789012:function:ContextInspectionFunction"
        memory_limit_in_mb = 512
        aws_request_id = "c6b4192b-8a71-469b-8919-abcdef123456"
        log_group_name = "/aws/lambda/ContextInspectionFunction"
        log_stream_name = "2026/08/25/[$LATEST]a1b2c3d4e5f6"

        def __init__(self):
            self._start_time = time.time()
            self._timeout_seconds = 30.0

        def get_remaining_time_in_millis(self) -> int:
            elapsed = time.time() - self._start_time
            remaining = self._timeout_seconds - elapsed
            return max(int(remaining * 1000), 0)

    result = lambda_handler(event={}, context=MockLambdaContext())
    print("\nHandler Response:")
    print(json.dumps(result, indent=2))
