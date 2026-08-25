"""
AWS Lambda Operation 04: Environment Variables

Demonstrates reading, configuring, and validating environment variables securely
within an AWS Lambda runtime using Python os.environ.
"""

import os
import json
from typing import Dict, Any


def get_config_from_env() -> Dict[str, Any]:
    """
    Reads configuration values from runtime environment variables with safe defaults.

    :return: Sanitized configuration dictionary.
    """
    app_env = os.environ.get("APP_ENV", "development")
    log_level = os.environ.get("LOG_LEVEL", "INFO")
    target_bucket = os.environ.get("S3_BUCKET_NAME", "my-default-lambda-bucket")
    api_key_raw = os.environ.get("API_KEY", "")

    # Mask sensitive credentials for safe logging output
    masked_api_key = f"{api_key_raw[:4]}****" if len(api_key_raw) > 4 else "NOT_SET"

    return {
        "app_env": app_env,
        "log_level": log_level,
        "s3_bucket_name": target_bucket,
        "api_key_status": "configured" if api_key_raw else "missing",
        "masked_api_key": masked_api_key
    }


def lambda_handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """
    AWS Lambda Handler Entrypoint.
    """
    print("[INFO] Fetching runtime configuration from environment variables...")

    config = get_config_from_env()
    print(f"[LOG] Loaded Configuration: {json.dumps(config)}")

    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps({
            "status": "success",
            "runtime_config": config
        })
    }


if __name__ == "__main__":
    print("=== LOCAL TEST DRIVER: ENVIRONMENT VARIABLES ===")

    # Set mock environment variables for local testing
    os.environ["APP_ENV"] = "production"
    os.environ["LOG_LEVEL"] = "DEBUG"
    os.environ["S3_BUCKET_NAME"] = "my-production-lambda-bucket-12345"
    os.environ["API_KEY"] = "secret_api_key_9876543210"

    result = lambda_handler(event={}, context=None)
    print("\nHandler Response:")
    print(json.dumps(result, indent=2))
