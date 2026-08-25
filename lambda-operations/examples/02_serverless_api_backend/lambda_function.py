"""
===============================================================================
EXAMPLE 2: Serverless REST API Backend (API Gateway Proxy Integration)
===============================================================================
Description:
    This Lambda function acts as a serverless backend API behind AWS API Gateway. 
    It inspects HTTP methods (GET, POST, DELETE), parses URL query string 
    parameters, parses JSON request bodies, and returns structured API Gateway 
    proxy response formats.

Dependencies:
    - json (Standard Library)
    - logging (Standard Library)
===============================================================================
"""

# =============================================================================
# SECTION 1: IMPORTS & LOGGER
# =============================================================================
import json
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

# =============================================================================
# SECTION 2: LAMBDA HANDLER FUNCTION
# =============================================================================
def lambda_handler(event, context):
    """
    AWS Lambda Handler for API Gateway REST HTTP Requests.
    """
    logger.info("🌐 Received HTTP Request from API Gateway")
    logger.info(f"Full Request Event: {json.dumps(event)}")

    # Extract HTTP details
    http_method = event.get("httpMethod", "GET")
    path = event.get("path", "/products")
    query_params = event.get("queryStringParameters") or {}
    headers = event.get("headers") or {}

    logger.info(f"Method: {http_method} | Path: {path} | Query Params: {query_params}")

    # Process based on HTTP method
    if http_method == "GET":
        category = query_params.get("category", "all")
        items = [
            {"id": 101, "name": "Wireless Headphones", "category": "electronics", "price": 99.99},
            {"id": 102, "name": "Ergonomic Keyboard", "category": "electronics", "price": 49.99},
            {"id": 103, "name": "Developer Coffee Mug", "category": "swag", "price": 14.99}
        ]
        
        if category != "all":
            items = [item for item in items if item["category"] == category]

        body = {
            "status": "SUCCESS",
            "message": f"Retrieved products for category '{category}'",
            "count": len(items),
            "data": items
        }
        status_code = 200

    elif http_method == "POST":
        raw_body = event.get("body", "{}")
        try:
            payload = json.loads(raw_body) if isinstance(raw_body, str) else raw_body
        except Exception:
            payload = {}

        product_name = payload.get("name", "New Item")
        price = payload.get("price", 0.0)

        body = {
            "status": "CREATED",
            "message": f"Product '{product_name}' created successfully!",
            "item": {
                "id": 201,
                "name": product_name,
                "price": price,
                "created": True
            }
        }
        status_code = 201

    else:
        body = {"status": "ERROR", "message": f"HTTP Method '{http_method}' not supported"}
        status_code = 405

    response = {
        "statusCode": status_code,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",
            "X-Powered-By": "AWS-Lambda-Serverless"
        },
        "body": json.dumps(body)
    }

    logger.info(f"✅ Response Status: {status_code}")
    return response
