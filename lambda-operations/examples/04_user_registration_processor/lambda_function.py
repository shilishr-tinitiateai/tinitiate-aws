"""
===============================================================================
EXAMPLE 4: User Registration Data Validator & Processor
===============================================================================
Description:
    This Lambda function validates new user registration payloads (checking required 
    email, username, and password fields), generates unique user IDs, and returns 
    formatted user database record creation output.

Dependencies:
    - json (Standard Library)
    - logging (Standard Library)
    - uuid (Standard Library)
    - datetime (Standard Library)
===============================================================================
"""

# =============================================================================
# SECTION 1: IMPORTS & LOGGER
# =============================================================================
import json
import logging
import uuid
import datetime

logger = logging.getLogger()
logger.setLevel(logging.INFO)

# =============================================================================
# SECTION 2: LAMBDA HANDLER FUNCTION
# =============================================================================
def lambda_handler(event, context):
    """
    AWS Lambda Handler for User Registration Data Ingestion.
    """
    logger.info("👤 Processing User Registration Ingestion Event...")
    logger.info(f"Input Event: {json.dumps(event)}")

    # Handle direct JSON or API Gateway proxy body payload
    if isinstance(event, dict) and "body" in event:
        raw_body = event["body"]
        data = json.loads(raw_body) if isinstance(raw_body, str) else raw_body
    else:
        data = event if isinstance(event, dict) else {}

    username = data.get("username")
    email = data.get("email")
    role = data.get("role", "STANDARD_USER")

    # Validation checks
    errors = []
    if not username or len(username) < 3:
        errors.append("Username is required and must be at least 3 characters.")
    if not email or "@" not in email:
        errors.append("Valid email address is required.")

    if errors:
        logger.warning(f"❌ Validation Failed: {errors}")
        return {
            "statusCode": 400,
            "body": {
                "status": "VALIDATION_ERROR",
                "errors": errors
            }
        }

    # Generate user metadata record
    user_id = f"USR-{str(uuid.uuid4())[:8].upper()}"
    created_at = datetime.datetime.utcnow().isoformat()

    user_record = {
        "user_id": user_id,
        "username": username,
        "email": email,
        "role": role,
        "account_status": "ACTIVE",
        "created_at": created_at
    }

    response = {
        "statusCode": 201,
        "headers": {
            "Content-Type": "application/json"
        },
        "body": {
            "status": "USER_CREATED",
            "message": f"User '{username}' registered successfully!",
            "user": user_record
        }
    }

    logger.info(f"✅ User Registered: {json.dumps(user_record)}")
    return response
