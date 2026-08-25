"""
===============================================================================
MODULE: AWS Lambda Function Handler (Version 1.0)
===============================================================================
Description:
    This module contains the primary handler function that executes inside the 
    AWS Lambda runtime environment. It receives event payloads, logs execution 
    details to CloudWatch, extracts input parameters, and returns a structured 
    HTTP-compliant JSON response.

Dependencies:
    - json (Standard Library)
    - logging (Standard Library)

Usage:
    Triggered automatically by AWS Lambda when invoked by CLI, API Gateway, 
    S3 events, or scheduled timers.
===============================================================================
"""

# =============================================================================
# SECTION 1: IMPORTS
# =============================================================================
import json
import logging

# =============================================================================
# SECTION 2: LOGGER CONFIGURATION
# =============================================================================
# Configure standard Python logger for AWS CloudWatch integration
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# =============================================================================
# SECTION 3: LAMBDA HANDLER FUNCTION
# =============================================================================
def lambda_handler(event, context):
    """
    Primary AWS Lambda Entry Point Handler.

    Parameters:
        event (dict): Event data passed to the function during invocation.
        context (LambdaContext): Runtime metadata provided by AWS Lambda.

    Returns:
        dict: HTTP-compliant dictionary containing status code, headers, and body.
    """
    logger.info("⚡ Lambda function execution started.")
    logger.info(f"📩 Received Event Payload: {json.dumps(event)}")

    # Extract 'name' parameter from event payload, defaulting to 'World' if missing or non-dict
    user_name = event.get("name", "World") if isinstance(event, dict) else "World"
    message = f"Hello, {user_name}! AWS Lambda function executed successfully."

    # Construct standard response object
    response = {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json"
        },
        "body": {
            "message": message,
            "input_received": event,
            "status": "SUCCESS"
        }
    }

    logger.info(f"✅ Execution completed successfully. Response: {json.dumps(response)}")
    return response
