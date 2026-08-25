"""
===============================================================================
MODULE: AWS Lambda Function Handler (Version 2.0 - Updated)
===============================================================================
Description:
    Updated version of the Lambda handler featuring ISO UTC timestamping, 
    enhanced log output, application version tagging ("2.0.0"), and custom 
    HTTP header returns.

Dependencies:
    - json (Standard Library)
    - logging (Standard Library)
    - datetime (Standard Library)

Usage:
    Packaged into a ZIP archive as `lambda_function.py` and uploaded to AWS 
    Lambda via the update-function-code operation.
===============================================================================
"""

# =============================================================================
# SECTION 1: IMPORTS
# =============================================================================
import json
import logging
import datetime

# =============================================================================
# SECTION 2: LOGGER CONFIGURATION
# =============================================================================
# Configure standard logger for CloudWatch integration
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# =============================================================================
# SECTION 3: UPDATED LAMBDA HANDLER FUNCTION (v2)
# =============================================================================
def lambda_handler(event, context):
    """
    Updated AWS Lambda Entry Point Handler v2.0.

    Parameters:
        event (dict): Incoming event payload object.
        context (LambdaContext): AWS Lambda context object.

    Returns:
        dict: Enhanced HTTP response with ISO UTC timestamp & custom headers.
    """
    logger.info("⚡ Executing Updated Lambda Function Handler v2.0")
    
    # Capture current UTC execution timestamp
    timestamp = datetime.datetime.utcnow().isoformat()
    user_name = event.get("name", "Valued Developer") if isinstance(event, dict) else "Valued Developer"
    
    response_body = {
        "version": "2.0.0",
        "timestamp": timestamp,
        "message": f"Hello {user_name}! Your Lambda code has been updated to version 2.0.",
        "received_payload": event,
        "features": ["Enhanced Logging", "UTC Timestamping", "Version Tagging"]
    }

    response = {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json",
            "X-Lambda-Version": "2.0.0"
        },
        "body": response_body
    }

    logger.info(f"✅ Execution v2.0 completed successfully at {timestamp}")
    return response
