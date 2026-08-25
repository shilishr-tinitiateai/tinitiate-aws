"""
===============================================================================
EXAMPLE 3: Scheduled Cron Task (Amazon EventBridge / CloudWatch Timer)
===============================================================================
Description:
    This Lambda function is executed on a automated cron schedule (e.g., every 
    night at midnight) triggered by Amazon EventBridge. It simulates auditing 
    system resources, purging expired temporary files, and returning execution 
    metrics.

Dependencies:
    - json (Standard Library)
    - logging (Standard Library)
    - datetime (Standard Library)
===============================================================================
"""

# =============================================================================
# SECTION 1: IMPORTS & LOGGER
# =============================================================================
import json
import logging
import datetime

logger = logging.getLogger()
logger.setLevel(logging.INFO)

# =============================================================================
# SECTION 2: LAMBDA HANDLER FUNCTION
# =============================================================================
def lambda_handler(event, context):
    """
    AWS Lambda Handler for Scheduled Timer Events.
    """
    logger.info("⏱️ Scheduled Cron Task Triggered by Amazon EventBridge!")
    logger.info(f"Event Metadata: {json.dumps(event)}")

    # Extract event trigger attributes
    rule_name = event.get("resources", ["arn:aws:events:rule/nightly-cleanup"])[0].split("/")[-1]
    execution_time = event.get("time", datetime.datetime.utcnow().isoformat())

    logger.info(f"Executing Rule: '{rule_name}' at Timestamp: {execution_time}")

    # Simulated resource cleanup operational statistics
    cleanup_summary = {
        "rule_executed": rule_name,
        "execution_timestamp": execution_time,
        "temp_files_purged": 142,
        "storage_freed_mb": 512.4,
        "status": "COMPLETED",
        "next_scheduled_run": "24 hours"
    }

    response = {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json"
        },
        "body": {
            "message": "Scheduled cleanup task completed successfully!",
            "metrics": cleanup_summary
        }
    }

    logger.info(f"✅ Cleanup Job Summary: {json.dumps(cleanup_summary)}")
    return response
