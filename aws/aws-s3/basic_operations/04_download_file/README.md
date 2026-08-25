# 04. Download File from S3

## 1. Definition
Downloading a file transfers an object stored in Amazon S3 to the local host filesystem.

## 2. Why Is It Used?
Applications download objects from S3 to retrieve data for local processing, analysis, reporting, or local caching.

## 3. AWS Concept
- `download_file()`: Boto3 high-level managed API that streams object content directly to disk without loading entire large payloads into Python memory buffers.
- **Path Resolution**: `pathlib.Path` ensures target parent folders exist across Windows, Linux, and macOS.

## 4. Prerequisites
- Target object must exist in S3 (e.g. uploaded via `02_upload_file`).
- IAM permission: `s3:GetObject`.

## 5. Input
- **Bucket Name**: `my-learning-s3-bucket-unique-12345`
- **Object Key**: `sample.txt`
- **Destination Path**: `downloads/downloaded_sample.txt`

## 6. Command
```bash
python download_file.py --bucket my-learning-s3-bucket-unique-12345 --key sample.txt
```

## 7. Expected Output
```text
[INFO] Downloading s3://my-learning-s3-bucket-unique-12345/sample.txt -> 'c:\code\aws\downloads\downloaded_sample.txt'...
[SUCCESS] Download completed successfully!
         Local File: c:\code\aws\downloads\downloaded_sample.txt
         Size:       215 bytes
```

## 8. Code
The operation is implemented in [`download_file.py`](./download_file.py).

## 9. Code Breakdown
- **Line 26**: Ensures local parent directories are created before streaming down file data (`dest_path.parent.mkdir(...)`).
- **Line 31–35**: Calls `s3_client.download_file(Bucket, Key, Filename)`.
- **Line 41–48**: Handles specific errors like `NoSuchKey` (HTTP 404) or `AccessDenied` (HTTP 403).

## 10. Parameter Breakdown
- `Bucket` *(string)*: Source S3 bucket.
- `Key` *(string)*: Target S3 object key.
- `Filename` *(string)*: Local path destination.

## 11. AWS CLI Equivalent
```bash
aws s3 cp s3://my-learning-s3-bucket-unique-12345/sample.txt downloads/downloaded_sample.txt
```

## 12. AWS Console Verification
1. Open the [AWS S3 Console](https://s3.console.aws.amazon.com/s3/).
2. Click your bucket and select the object `sample.txt`.
3. Click the **Download** button to manually download and compare file hashes.

## 13. Common Errors
- `NoSuchKey`: The requested object key does not exist.
- `NoSuchBucket`: The bucket does not exist.
- `AccessDenied`: IAM user/role lacks `s3:GetObject` permission.

## 14. Troubleshooting
- Verify object key spelling including case-sensitivity and prefixes.

## 15. Security Notes
- Ensure downloaded file permissions locally restrict unauthorized host user access.

## 16. Cleanup
To remove local download file:
Delete `downloads/downloaded_sample.txt` locally.

## 17. Related Operations
- Previous: [03. List Buckets and Objects](../03_list_buckets_and_objects/README.md)
- Next: [05. Delete File](../05_delete_file/README.md)
