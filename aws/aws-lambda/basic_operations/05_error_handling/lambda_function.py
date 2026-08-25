"""
AWS Lambda Operation 05: Error Handling & Custom Exceptions

Demonstrates robust error handling, custom exception catching, HTTP error status code mapping,
and structured error response formatting within AWS Lambda.
"""

import json
import traceback
from typing import Dict, Any


class InvalidPayloadException(Exception):
    """Custom exception raised for invalid input payload data."""
    pass


class BusinessLogicException(Exception):
    """Custom exception raised for domain logic failures."""
    pass


def process_order(order_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Processes an incoming order payload, validating required fields.

    :param order_data: Order payload dictionary.
    :return: Processed order summary.
    :raises InvalidPayloadException: If required fields are missing.
    :raises BusinessLogicException: If order amount is invalid.
    """
    if "order_id" not in order_data:
        raise InvalidPayloadException("Missing mandatory field 'order_id' in event payload.")

    amount = order_data.get("amount", 0.0)
    if not isinstance(amount, (int, float)) or amount <= 0:
        raise BusinessLogicException(f"Invalid order amount '{amount}'. Amount must be a positive number.")

    return {
        "order_id": order_data["order_id"],
        "status": "PROCESSED",
        "total_amount": amount
    }


def lambda_handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """
    AWS Lambda Handler Entrypoint with comprehensive exception handling.
    """
    print(f"[INFO] Processing request event: {json.dumps(event)}")

    try:
        # Business logic execution
        result = process_order(event)
        print(f"[SUCCESS] Order processed: {result}")

        return {
            "statusCode": 200,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({"status": "success", "data": result})
        }

    except InvalidPayloadException as e:
        print(f"[WARNING] Validation Error: {e}")
        return {
            "statusCode": 400,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({
                "status": "error",
                "error_type": "InvalidPayloadException",
                "message": str(e)
            })
        }

    except BusinessLogicException as e:
        print(f"[WARNING] Business Logic Error: {e}")
        return {
            "statusCode": 422,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({
                "status": "error",
                "error_type": "BusinessLogicException",
                "message": str(e)
            })
        }

    except Exception as e:
        print(f"[ERROR] Unhandled Server Exception: {e}")
        print(traceback.format_exc())
        return {
            "statusCode": 500,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({
                "status": "error",
                "error_type": "InternalServerError",
                "message": "An unexpected error occurred while processing the request."
            })
        }


if __name__ == "__main__":
    print("=== TEST 1: SUCCESSFUL EXECUTION ===")
    res1 = lambda_handler(event={"order_id": "ORD-101", "amount": 150.75}, context=None)
    print(json.dumps(res1, indent=2))

    print("\n=== TEST 2: INVALID PAYLOAD (HTTP 400) ===")
    res2 = lambda_handler(event={"amount": 50.0}, context=None)
    print(json.dumps(res2, indent=2))

    print("\n=== TEST 3: BUSINESS LOGIC ERROR (HTTP 422) ===")
    res3 = lambda_handler(event={"order_id": "ORD-102", "amount": -10.0}, context=None)
    print(json.dumps(res3, indent=2))
