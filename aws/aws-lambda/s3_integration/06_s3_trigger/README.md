# 06. Lambda S3 Event Trigger Notification

## 1. Definition
An S3 Event Trigger Notification automatically invokes an AWS Lambda function whenever a designated object event occurs in an S3 bucket (e.g. `s3:ObjectCreated:*` or `s3:ObjectRemoved:*`).

## 2. Why Is It Used?
S3 Event Notifications enable event-driven architectures where uploading a file automatically initiates downstream background workflows (e.g., thumbnail generation, log ingestion, CSV parsing, data lake enrichment) without polling.

## 3. AWS Concept
- **Event Notification**: AWS S3 generates an event payload containing `Records` array with bucket and key details.
- **URL Unquoting**: Object keys in S3 event payloads are URL-encoded (`sample+file.txt` -> `sample file.txt`). `urllib.parse.unquote_plus()` must be used to decode key strings.

## 4. Prerequisites
- Target S3 bucket created.
- Lambda function deployed with IAM permission: `s3:GetObject`.
- S3 Bucket Notification configuration linking event to Lambda ARN.

## 5. Input
- **S3 Event Record**: `{"eventName": "ObjectCreated:Put", "s3": {"bucket": {"name": "my-bucket"}, "object": {"key": "incoming%2Fsample+file.txt"}}}`

## 6. Command
```bash
python lambda_function.py
```

## 7. Expected Output
```text
=== LOCAL TEST DRIVER: S3 EVENT TRIGGER ===
[INFO] S3 Trigger function invoked with 1 record(s).
[LOG] S3 Event: ObjectCreated:Put | Bucket: s3://my-learning-s3-bucket-unique-12345 | Key: 'incoming/sample file.txt' | Size: 215 bytes

Handler Response:
{
  "statusCode": 200,
  "headers": {
    "Content-Type": "application/json"
  },
  "body": "{\"status\": \"success\", \"processed_records_count\": 1, \"records\": [{\"event_name\": \"ObjectCreated:Put\", \"event_time\": \"2026-08-25T12:00:00.000Z\", \"aws_region\": \"us-east-1\", \"bucket_name\": \"my-learning-s3-bucket-unique-12345\", \"object_key\": \"incoming/sample file.txt\", \"object_size_bytes\": 215, \"e_tag\": \"d41d8cd98f00b204e9800998ecf8427e\"}]}"
}
```

## 8. Code
The operation is implemented in [`lambda_function.py`](./lambda_function.py).

## 9. Code Breakdown
- **Line 11–35**: Iterates over `event['Records']` extracting bucket name and key metadata.
- **Line 26**: Uses `urllib.parse.unquote_plus(raw_key)` to convert URL-encoded spaces (`+`) and special characters back into valid object key strings.

## 10. Parameter Breakdown
- `Records` *(list)*: Array of S3 event notification record maps.
- `eventName` *(string)*: Trigger type (`ObjectCreated:Put`, `ObjectCreated:Post`, `ObjectRemoved:Delete`).

## 11. AWS CLI Equivalent
```bash
# Add Lambda trigger permission to S3 bucket via CLI:
aws lambda add-permission --function-name S3TriggerFunction --statement-id s3invoke --action lambda:InvokeFunction --principal s3.amazonaws.com --source-arn arn:aws:s3:::my-learning-s3-bucket-unique-12345
```

## 12. AWS Console Verification
1. Open [AWS S3 Console](https://s3.console.aws.amazon.com/s3/).
2. Select your bucket -> Open **Properties** tab -> Scroll to **Event notifications** -> Configure event targeting your Lambda function.

## 13. Common Errors
- `KeyError`: Failing to URL-decode key strings, causing downstream `NoSuchKey` errors when calling Boto3 `get_object()`.

## 14. Troubleshooting
- Ensure resource-based policy (`lambda:InvokeFunction`) allows `s3.amazonaws.com` as principal to trigger the Lambda function.

## 15. Security Notes
- Restrict `source-arn` in Lambda resource policies to prevent other AWS accounts from triggering your function.

## 16. Cleanup
Delete S3 Event notification configuration in S3 console.

## 17. Related Operations
- Previous: [Basic Operations Overview](../../basic_operations/README.md)
- Next: [07. S3 File Processing](../07_s3_file_processing/README.md)
