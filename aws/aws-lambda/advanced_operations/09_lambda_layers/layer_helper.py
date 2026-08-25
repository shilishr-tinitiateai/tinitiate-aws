"""
Lambda Layer Shared Helper Module.

This file represents code packaged inside an AWS Lambda Layer (e.g. at /opt/python/layer_helper.py).
Lambda layers allow sharing reusable code libraries across multiple functions.
"""

from typing import Dict, Any


def format_response_payload(data: Any, status_code: int = 200, message: str = "Success") -> Dict[str, Any]:
    """
    Standardized payload formatter provided by the Lambda Layer.

    :param data: Output payload object.
    :param status_code: HTTP status code.
    :param message: Response message string.
    :return: Standardized API response schema dict.
    """
    return {
        "statusCode": status_code,
        "headers": {
            "Content-Type": "application/json",
            "X-Layer-Version": "1.0.0"
        },
        "body": {
            "status": "success" if status_code < 400 else "error",
            "message": message,
            "layer_metadata": {
                "shared_library": "layer_helper.py",
                "version": "1.0.0"
            },
            "data": data
        }
    }
