# 08. S3 Event Processing End-to-End Pipeline

## 1. Definition
An end-to-end serverless ETL pipeline triggers a Lambda function upon object creation in a source S3 bucket, executes data transformation logic in memory, and writes the processed output artifact to a destination S3 bucket.

## 2. Why Is It Used?
This pattern underpins serverless data engineering architecture (e.g. converting uploaded CSV logs to parquet format, generating JSON metadata reports, anonymizing sensitive PII columns) without running persistent servers.

## 3. AWS Concept
- **Decoupled Architecture**: Source Bucket (Ingestion) -> Event Trigger -> Lambda (Transform) -> Destination Bucket (Delivery).
- **IAM Principle of Least Privilege**: The Lambda execution role requires `s3:GetObject` on the source bucket and `s3:PutObject` on the destination bucket.

## 4. Prerequisites
- Source S3 bucket and Destination S3 bucket created.
- IAM execution role configured with read/write access.

## 5. Input
- **Source Bucket**: `source-bucket-12345`
- **Source Key**: `sample.txt`
- **Destination Bucket**: `dest-bucket-12345`

## 6. Command
```bash
python lambda_function.py
```

## 7. Expected Output
```text
=== LOCAL TEST DRIVER: S3 PIPELINE ===
[ETL STEP 1/3] Reading s3://source-bucket-12345/sample.txt...
[ETL STEP 2/3] Transforming payload content...
[ETL STEP 3/3] Uploading transformed result -> s3://dest-bucket-12345/processed/processed_sample.json...

[MOCK S3 WRITE SUCCESS]
Bucket: dest-bucket-12345
Key:    processed/processed_sample.json
Body Content:
{
  "pipeline_status": "SUCCESS",
  "source": {
    "bucket": "source-bucket-12345",
    "key": "sample.txt",
    "size_bytes": 215
  },
  "transformation_summary": {
    "total_non_empty_lines": 4,
    "word_count": 28,
    "uppercase_sample": [
      "HELLO FROM AWS S3 & AWS LAMBDA OPERATIONS REPOSITORY!",
      "THIS IS A SAMPLE TEXT FILE USED TO DEMONSTRATE FILE UPLOAD, DOWNLOAD, COPY, METADATA, PRESIGNED URLS, AND LAMBDA PROCESSING."
    ]
  },
  "processed_timestamp_utc": "2026-08-25T12:00:00Z"
}
```

## 8. Code
The operation is implemented in [`lambda_function.py`](./lambda_function.py).

## 9. Code Breakdown
- **Line 33**: Step 1 reads source object payload (`s3_client.get_object`).
- **Line 39–53**: Step 2 transforms string lines into structured JSON summary format.
- **Line 57–62**: Step 3 writes transformed result to destination bucket under `processed/` prefix via `s3_client.put_object`.

## 10. Parameter Breakdown
- `DEST_BUCKET_NAME` *(env var)*: Destination bucket name identifier.

## 11. AWS CLI Equivalent
```bash
# Monitor end-to-end pipeline executions via CloudWatch CLI:
aws logs tail /aws/lambda/S3EventPipelineFunction --follow
```

## 12. AWS Console Verification
1. Upload file to Source Bucket in [AWS S3 Console](https://s3.console.aws.amazon.com/s3/).
2. Open Destination Bucket -> Navigate to `processed/` folder prefix -> Verify `processed_<filename>.json` artifact created.

## 13. Common Errors
- `AccessDenied`: Occurs if Lambda execution role lacks `s3:PutObject` on destination bucket or `s3:GetObject` on source bucket.
- **Recursive Invocation Loop**: Triggering Lambda on a bucket and writing output back to the *same* bucket under the *same* prefix creates an infinite execution billing loop!

## 14. Troubleshooting
- To prevent infinite invocation loops, ensure output files are written to a different bucket OR filtered out using distinct S3 event prefix rules (e.g. trigger only on `raw/` and write to `processed/`).

## 15. Security Notes
- Enforce strict IAM policies restricting Lambda to specific source and destination ARNs.

## 16. Cleanup
Delete source and output destination test files.

## 17. Related Operations
- Previous: [07. S3 File Processing](../07_s3_file_processing/README.md)
- Next: [Advanced Operations Overview](../../advanced_operations/README.md)
