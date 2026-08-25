"""
AWS Lambda Operation 02: Event Payload Parsing

Demonstrates parsing incoming trigger event objects (API Gateway HTTP events,
query parameters, path variables, and direct JSON invocation payloads).
"""

import json
from typing import Dict, Any


def parse_event(event: Dict[str, Any]) -> Dict[str, Any]:
    """
    Parses and extracts structured data from various AWS event schema types.

    :param event: Incoming event dictionary.
    :return: Extracted metadata dictionary.
    """
    extracted_data = {}

    # Case 1: API Gateway REST/HTTP Proxy Event
    if "httpMethod" in event or "requestContext" in event:
        http_method = event.get("httpMethod", event.get("requestContext", {}).get("http", {}).get("method"))
        path = event.get("path", event.get("rawPath", "/"))
        query_params = event.get("queryStringParameters") or {}
        headers = event.get("headers") or {}
        
        body_raw = event.get("body", "{}")
        try:
            body = json.loads(body_raw) if isinstance(body_raw, str) else body_raw
        except json.JSONDecodeError:
            body = {"raw": body_raw}

        extracted_data = {
            "trigger_type": "API Gateway HTTP Proxy",
            "http_method": http_method,
            "path": path,
            "query_parameters": query_params,
            "user_agent": headers.get("User-Agent", "Unknown"),
            "parsed_body": body
        }

    # Case 2: Direct JSON Invocation / Custom Trigger Event
    else:
        extracted_data = {
            "trigger_type": "Direct SDK / CLI Invocation",
            "payload_keys": list(event.keys()),
            "custom_payload": event
        }

    return extracted_data


def lambda_handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """
    AWS Lambda Handler Entrypoint.
    """
    print(f"[INFO] Processing event payload of size {len(json.dumps(event))} bytes.")

    parsed_info = parse_event(event)
    print(f"[LOG] Event Analysis: {json.dumps(parsed_info)}")

    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps({
            "status": "success",
            "event_summary": parsed_info
        })
    }


if __name__ == "__main__":
    print("=== LOCAL TEST DRIVER: API GATEWAY EVENT ===")
    api_gateway_event = {
        "httpMethod": "POST",
        "path": "/api/v1/users",
        "queryStringParameters": {"status": "active", "page": "1"},
        "headers": {"User-Agent": "Mozilla/5.0 (Windows NT 10.0)"},
        "body": json.dumps({"user_id": 42, "email": "dev@example.com"})
    }

    res1 = lambda_handler(event=api_gateway_event, context=None)
    print(json.dumps(res1, indent=2))

    print("\n=== LOCAL TEST DRIVER: DIRECT JSON EVENT ===")
    direct_event = {"action": "process_data", "batch_id": "batch-999"}
    res2 = lambda_handler(event=direct_event, context=None)
    print(json.dumps(res2, indent=2))
