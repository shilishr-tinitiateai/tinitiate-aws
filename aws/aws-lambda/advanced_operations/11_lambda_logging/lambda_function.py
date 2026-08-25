"""
AWS Lambda Operation 11: Structured CloudWatch Logging

Demonstrates configuring Python's standard logging module for structured JSON logging
compatible with AWS CloudWatch Logs and CloudWatch Logs Insights.
"""

import os
import json
import logging
import traceback
from typing import Dict, Any

# Configure structured logger
logger = logging.getLogger()
log_level_str = os.environ.get("LOG_LEVEL", "INFO").upper()
logger.setLevel(getattr(logging, log_level_str, logging.INFO))


def log_structured(level: str, message: str, context: Any = None, **kwargs):
    """
    Emits a structured JSON log entry to stdout for CloudWatch ingestion.

    :param level: Log level ('INFO', 'WARNING', 'ERROR', 'DEBUG').
    :param message: Log message string.
    :param context: Lambda context object.
    :param kwargs: Additional metadata key-value pairs.
    """
    log_entry = {
        "timestamp_utc": "2026-08-25T12:00:00Z",
        "level": level.upper(),
        "message": message,
        "request_id": getattr(context, "aws_request_id", "local-request-id"),
        "function_name": getattr(context, "function_name", "local_logging_function"),
        "metadata": kwargs
    }
    
    log_json = json.dumps(log_entry)
    
    if level.upper() == "ERROR":
        logger.error(log_json)
    elif level.upper() == "WARNING":
        logger.warning(log_json)
    elif level.upper() == "DEBUG":
        logger.debug(log_json)
    else:
        logger.info(log_json)


def lambda_handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """
    AWS Lambda Handler Entrypoint with Structured Logging.
    """
    log_structured("INFO", "Lambda execution started", context=context, input_event=event)

    user_id = event.get("user_id")
    if not user_id:
        log_structured("WARNING", "User ID omitted in request payload", context=context, event_keys=list(event.keys()))

    try:
        if event.get("simulate_error"):
            raise ValueError("Simulated runtime error for CloudWatch log tracking!")

        log_structured("INFO", "Processing completed successfully", context=context, user_id=user_id, status="OK")
        
        return {
            "statusCode": 200,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({"status": "success", "user_id": user_id})
        }

    except Exception as e:
        log_structured(
            "ERROR",
            f"Execution failed: {str(e)}",
            context=context,
            error_type=type(e).__name__,
            stack_trace=traceback.format_exc()
        )
        return {
            "statusCode": 500,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({"status": "error", "message": str(e)})
        }


if __name__ == "__main__":
    print("=== LOCAL TEST DRIVER: STRUCTURED LOGGING ===")
    
    print("\n--- Test 1: Info & Warning Logging ---")
    lambda_handler(event={"user_id": 404}, context=None)

    print("\n--- Test 2: Error Stack Trace Logging ---")
    lambda_handler(event={"simulate_error": True}, context=None)
