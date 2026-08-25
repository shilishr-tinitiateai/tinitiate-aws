# 03. List Buckets and Objects

## 1. Definition
Listing operations enumerate AWS account-owned S3 buckets and discover objects stored within a target bucket, providing metadata such as key names, byte sizes, and modification timestamps.

## 2. Why Is It Used?
Applications list buckets and objects to discover available datasets, inspect directory prefixes, run audit pipelines, or power file explorer user interfaces.

## 3. AWS Concept
- `list_buckets()`: Account-level global metadata operation returning all buckets owned by the IAM caller.
- `list_objects_v2()`: Modern, paginated API to query contents of a specific bucket. Replaces legacy `list_objects`.
- **Prefix**: Acts as a virtual folder filter matching object keys starting with the specified string.

## 4. Prerequisites
- Configured AWS credentials.
- IAM permissions: `s3:ListAllMyBuckets` and `s3:ListBucket`.

## 5. Input
- **Bucket Name**: `my-learning-s3-bucket-unique-12345`
- **Prefix Filter** *(optional)*: `""` (empty string lists all keys)

## 6. Command
```bash
python list_buckets_and_objects.py --bucket my-learning-s3-bucket-unique-12345
```

## 7. Expected Output
```text
[INFO] Fetching account S3 buckets...
[SUCCESS] Found 1 bucket(s):
  - my-learning-s3-bucket-unique-12345 (Created: 2026-08-25 15:00:00 UTC)

[INFO] Listing objects in s3://my-learning-s3-bucket-unique-12345 (Prefix: '')...
[SUCCESS] Found 1 object(s):
  - sample.txt                          | Size:      215 bytes | Modified: 2026-08-25 15:05:00 UTC
Total objects size: 215 bytes
```

## 8. Code
The operation is implemented in [`list_buckets_and_objects.py`](./list_buckets_and_objects.py).

## 9. Code Breakdown
- **Line 21–25**: Invokes `s3_client.list_buckets()` to retrieve account-wide bucket listings.
- **Line 45–50**: Builds dynamic keyword parameters for `list_objects_v2(Bucket=..., Prefix=...)`.
- **Line 55–60**: Iterates over returned `Contents` dict array extracting `Key`, `Size`, and `LastModified`.

## 10. Parameter Breakdown
- `Bucket` *(string)*: Name of bucket to list.
- `Prefix` *(string)*: Limits response to keys that begin with the specified prefix.
- `MaxKeys` *(int)*: Sets maximum keys per response (default 1000).

## 11. AWS CLI Equivalent
```bash
# List all account buckets:
aws s3 ls

# List objects inside a specific bucket:
aws s3 ls s3://my-learning-s3-bucket-unique-12345/
```

## 12. AWS Console Verification
1. Open the [AWS S3 Console](https://s3.console.aws.amazon.com/s3/).
2. Verify account buckets listed on the root landing page.
3. Click your bucket to inspect object items.

## 13. Common Errors
- `AccessDenied`: Missing `s3:ListBucket` or `s3:ListAllMyBuckets` IAM permissions.
- `NoSuchBucket`: Target bucket name invalid or non-existent.

## 14. Troubleshooting
- If `list_objects_v2` returns empty contents, verify exact prefix case-sensitivity.

## 15. Security Notes
- `s3:ListBucket` permission allows viewing metadata (key names, sizes) but not reading object payload contents (`s3:GetObject`).

## 16. Cleanup
Listing operations are read-only and require no cleanup.

## 17. Related Operations
- Previous: [02. Upload File](../02_upload_file/README.md)
- Next: [04. Download File](../04_download_file/README.md)
