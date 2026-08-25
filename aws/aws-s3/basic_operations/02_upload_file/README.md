# 02. Upload File to S3

## 1. Definition
Uploading a file transfers a local filesystem file to an Amazon S3 bucket, storing it as an S3 Object referenced by an Object Key.

## 2. Why Is It Used?
Applications upload files to S3 for persistent cloud storage, serving static website assets, archiving logs, or feeding downstream automated processing pipelines (e.g. triggering AWS Lambda functions).

## 3. AWS Concept
- **Object Key**: The unique name (path identifier) that assigns an identity to an object within a bucket (e.g. `documents/invoices/sample.txt`).
- **Managed Upload**: Boto3's `upload_file()` method automatically handles single-part uploads for small files and multi-part parallel uploads for large files thresholding at 8 MB.

## 4. Prerequisites
- Target S3 bucket created (e.g. via `01_create_bucket`).
- Local sample file present (e.g. `examples/sample.txt`).
- IAM permission: `s3:PutObject`.

## 5. Input
- **Bucket**: `my-learning-s3-bucket-unique-12345`
- **Local File Path**: `examples/sample.txt`
- **Object Key**: `sample.txt`

## 6. Command
```bash
python upload_file.py --bucket my-learning-s3-bucket-unique-12345 --file ../../../examples/sample.txt --key sample.txt
```

## 7. Expected Output
```text
[INFO] Uploading 'c:\code\aws\examples\sample.txt' -> s3://my-learning-s3-bucket-unique-12345/sample.txt...
[SUCCESS] File uploaded successfully!
         Bucket: my-learning-s3-bucket-unique-12345
         Key:    sample.txt
         Size:   215 bytes
```

## 8. Code
The operation is implemented in [`upload_file.py`](./upload_file.py).

## 9. Code Breakdown
- **Line 21–24**: Checks if local file exists via `pathlib.Path.exists()`.
- **Line 33–37**: Calls `s3_client.upload_file(Filename, Bucket, Key)`, abstracting chunk management.
- **Line 41–50**: Catches `ClientError` for `NoSuchBucket` and `AccessDenied`.

## 10. Parameter Breakdown
- `Filename` *(string)*: Absolute or relative local path to the file.
- `Bucket` *(string)*: S3 target bucket name.
- `Key` *(string)*: Destination object key in S3.

## 11. AWS CLI Equivalent
```bash
aws s3 cp examples/sample.txt s3://my-learning-s3-bucket-unique-12345/sample.txt
```

## 12. AWS Console Verification
1. Navigate to the [AWS S3 Console](https://s3.console.aws.amazon.com/s3/).
2. Select bucket `my-learning-s3-bucket-unique-12345`.
3. Verify that `sample.txt` appears in the object list with matching size.

## 13. Common Errors
- `NoSuchBucket`: Destination bucket does not exist.
- `AccessDenied`: IAM permissions missing for `s3:PutObject`.
- `FileNotFoundError`: Local source path invalid or file deleted.

## 14. Troubleshooting
- Verify target bucket name spelling.
- Ensure local relative paths resolve correctly regardless of active working directory.

## 15. Security Notes
- Avoid storing sensitive plain-text API credentials or private keys in uploaded files.
- Enable S3 Default Encryption (SSE-S3) on target buckets.

## 16. Cleanup
To delete uploaded file:
```bash
python ../05_delete_file/delete_file.py --bucket my-learning-s3-bucket-unique-12345 --key sample.txt
```

## 17. Related Operations
- Previous: [01. Create Bucket](../01_create_bucket/README.md)
- Next: [03. List Buckets and Objects](../03_list_buckets_and_objects/README.md)
