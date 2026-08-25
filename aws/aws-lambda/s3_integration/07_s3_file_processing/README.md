# 07. Lambda S3 File Processing

## 1. Definition
S3 File Processing downloads triggered objects from an S3 bucket into Lambda's ephemeral container filesystem (`/tmp`), inspects/parses file content, and extracts analytical data metrics.

## 2. Why Is It Used?
Applications use Lambda file processing to compute text statistics, convert image formats, parse uploaded CSV/JSON logs, or extract PDF metadata automatically whenever users upload files to S3 buckets.

## 3. AWS Concept
- **Ephemeral `/tmp` Storage**: Every AWS Lambda instance provides between 512 MB and 10,240 MB of temporary disk space at `/tmp` for temporary file operations during invocation lifetime.
- **Container Reuse**: Files created in `/tmp` persist across warm container invocations. Developers must explicitly delete temporary files to avoid filling up disk allocation.

## 4. Prerequisites
- Target S3 bucket containing sample file (`sample.txt`).
- IAM execution role permission: `s3:GetObject`.

## 5. Input
- **S3 Event Record**: `{"s3": {"bucket": {"name": "my-learning-s3-bucket-unique-12345"}, "object": {"key": "sample.txt"}}}`

## 6. Command
```bash
python lambda_function.py
```

## 7. Expected Output
```text
=== LOCAL TEST DRIVER: S3 FILE PROCESSING ===
[INFO] Downloading s3://my-learning-s3-bucket-unique-12345/sample.txt -> 'scratch\sample.txt'...
[SUCCESS] Processed S3 File Metrics: Lines: 4 | Words: 28 | Size: 215 bytes
[INFO] Cleaned up ephemeral file 'scratch\sample.txt'.

Processed Summary:
{
  "bucket": "my-learning-s3-bucket-unique-12345",
  "key": "sample.txt",
  "local_tmp_path": "scratch\\sample.txt",
  "file_size_bytes": 215,
  "line_count": 4,
  "word_count": 28,
  "character_count": 215,
  "content_preview": "Hello from AWS S3 & AWS Lambda Operations Repository!..."
}
```

## 8. Code
The operation is implemented in [`lambda_function.py`](./lambda_function.py).

## 9. Code Breakdown
- **Line 26**: Resolves temporary local path under `/tmp/filename`.
- **Line 31**: Downloads object payload via `s3_client.download_file()`.
- **Line 51–53**: Deletes temporary file (`tmp_download_path.unlink()`) to ensure `/tmp` disk storage hygiene.

## 10. Parameter Breakdown
- `Bucket` *(string)*: Source S3 bucket name.
- `Key` *(string)*: Object key identifier.
- `Filename` *(string)*: Local path destination inside `/tmp`.

## 11. AWS CLI Equivalent
```bash
# Verify Lambda logs for file processing execution:
aws logs tail /aws/lambda/S3FileProcessingFunction --follow
```

## 12. AWS Console Verification
1. Open [AWS Lambda Console](https://console.aws.amazon.com/lambda/).
2. Upload `sample.txt` to S3 bucket.
3. Open CloudWatch Logs to view computed line/word count output metrics.

## 13. Common Errors
- `[Errno 28] No space left on device`: Occurs if `/tmp` storage fills up from uncleaned temporary files across warm Lambda invocations.

## 14. Troubleshooting
- Always wrap file processing logic in `try ... finally` or execute explicit `os.unlink(tmp_path)` cleanup blocks.

## 15. Security Notes
- Treat input files from untrusted uploads as unsafe. Validate file headers before parsing.

## 16. Cleanup
Ephemeral `/tmp` directory files are deleted automatically when function container terminates.

## 17. Related Operations
- Previous: [06. S3 Event Trigger Notification](../06_s3_trigger/README.md)
- Next: [08. S3 Event Processing End-to-End](../08_s3_event_processing/README.md)
