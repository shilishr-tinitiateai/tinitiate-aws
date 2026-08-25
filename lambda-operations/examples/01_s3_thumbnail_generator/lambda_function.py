"""
===============================================================================
EXAMPLE 1: S3 Event Trigger - Automated File & Thumbnail Processor
===============================================================================
Description:
    This Lambda function is triggered automatically when a new file/image is 
    uploaded to an AWS S3 bucket. It extracts S3 event metadata (bucket name, 
    file key, size, timestamp), processes the file metadata, and returns a 
    structured status response.

Dependencies:
    - json (Standard Library)
    - logging (Standard Library)
    - urllib.parse (Standard Library)
===============================================================================
"""

# =============================================================================
# SECTION 1: IMPORTS
# =============================================================================
import json
import logging
import urllib.parse

# =============================================================================
# SECTION 2: LOGGER CONFIGURATION
# =============================================================================
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# =============================================================================
# SECTION 3: LAMBDA HANDLER FUNCTION
# =============================================================================
def lambda_handler(event, context):
    """
    AWS Lambda Handler for S3 File Upload Triggers.

    Parameters:
        event (dict): S3 Event notification dictionary containing Records array.
        context (LambdaContext): Runtime metadata provided by AWS.

    Returns:
        dict: Processing summary and metadata response object.
    """
    logger.info("🚀 S3 Event Trigger Received!")
    logger.info(f"Raw Event Payload: {json.dumps(event)}")

    # Extract S3 record details safely
    records = event.get("Records", [])
    if not records:
        logger.warning("⚠️ No S3 Records found in event payload.")
        return {
            "statusCode": 400,
            "body": {"message": "Invalid event: Missing S3 Records"}
        }

    processed_files = []
    
    for record in records:
        s3_data = record.get("s3", {})
        bucket_name = s3_data.get("bucket", {}).get("name", "unknown-bucket")
        # URL decode object key (handles spaces and special characters like '+')
        raw_key = s3_data.get("object", {}).get("key", "unknown-key")
        object_key = urllib.parse.unquote_plus(raw_key)
        object_size = s3_data.get("object", {}).get("size", 0)
        event_time = record.get("eventTime", "N/A")

        logger.info(f"📄 Processing File: '{object_key}' from Bucket: '{bucket_name}' ({object_size} bytes)")

        # Simulated thumbnail processing logic
        file_info = {
            "bucket": bucket_name,
            "original_key": object_key,
            "thumbnail_key": f"thumbnails/thumb_{object_key.split('/')[-1]}",
            "file_size_bytes": object_size,
            "processed_at": event_time,
            "status": "THUMBNAIL_CREATED"
        }
        processed_files.append(file_info)

    response = {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json"
        },
        "body": {
            "message": "S3 File Event Processed Successfully!",
            "total_files_processed": len(processed_files),
            "files": processed_files
        }
    }

    logger.info(f"✅ S3 Processing Complete: {json.dumps(response)}")
    return response
