"""
AWS Lambda Operation 06: S3 Event Trigger Notification

Demonstrates parsing S3 Event Notification records (ObjectCreated:Put) received
by Lambda when a file is uploaded to an S3 bucket.
"""

import json
import urllib.parse
from typing import Dict, Any, List


def parse_s3_event(event: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Parses S3 event records from incoming event notification payload.

    :param event: AWS Event notification dictionary.
    :return: List of extracted record summaries.
    """
    records_summary = []
    
    if "Records" not in event:
        print("[WARNING] Event does not contain an S3 'Records' list.")
        return []

    for record in event["Records"]:
        event_name = record.get("eventName", "Unknown")
        event_time = record.get("eventTime", "N/A")
        aws_region = record.get("awsRegion", "us-east-1")

        s3_info = record.get("s3", {})
        bucket_name = s3_info.get("bucket", {}).get("name", "Unknown")
        
        # Object key in S3 event notification is URL-encoded (e.g., spaces become +)
        raw_key = s3_info.get("object", {}).get("key", "Unknown")
        object_key = urllib.parse.unquote_plus(raw_key)
        object_size = s3_info.get("object", {}).get("size", 0)
        e_tag = s3_info.get("object", {}).get("eTag", "N/A")

        record_detail = {
            "event_name": event_name,
            "event_time": event_time,
            "aws_region": aws_region,
            "bucket_name": bucket_name,
            "object_key": object_key,
            "object_size_bytes": object_size,
            "e_tag": e_tag
        }
        records_summary.append(record_detail)
        
        print(f"[LOG] S3 Event: {event_name} | Bucket: s3://{bucket_name} | Key: '{object_key}' | Size: {object_size} bytes")

    return records_summary


def lambda_handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """
    AWS Lambda Handler Entrypoint for S3 Triggers.
    """
    print(f"[INFO] S3 Trigger function invoked with {len(event.get('Records', []))} record(s).")

    parsed_records = parse_s3_event(event)

    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps({
            "status": "success",
            "processed_records_count": len(parsed_records),
            "records": parsed_records
        })
    }


if __name__ == "__main__":
    print("=== LOCAL TEST DRIVER: S3 EVENT TRIGGER ===")
    
    # Standard S3 Event Notification Schema payload sent by AWS S3 to Lambda
    mock_s3_event = {
        "Records": [
            {
                "eventVersion": "2.1",
                "eventSource": "aws:s3",
                "awsRegion": "us-east-1",
                "eventTime": "2026-08-25T12:00:00.000Z",
                "eventName": "ObjectCreated:Put",
                "s3": {
                    "s3SchemaVersion": "1.0",
                    "configurationId": "testConfigRule",
                    "bucket": {
                        "name": "my-learning-s3-bucket-unique-12345",
                        "arn": "arn:aws:s3:::my-learning-s3-bucket-unique-12345"
                    },
                    "object": {
                        "key": "incoming%2Fsample+file.txt",
                        "size": 215,
                        "eTag": "d41d8cd98f00b204e9800998ecf8427e"
                    }
                }
            }
        ]
    }

    res = lambda_handler(event=mock_s3_event, context=None)
    print("\nHandler Response:")
    print(json.dumps(res, indent=2))
