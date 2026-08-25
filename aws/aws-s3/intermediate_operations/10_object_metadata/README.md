# 10. S3 Object Metadata

## 1. Definition
Object metadata consists of key-value pairs stored alongside an S3 object, divided into System Metadata (e.g. `Content-Type`, `Content-Length`) and User-Defined Custom Metadata (`x-amz-meta-*`).

## 2. Why Is It Used?
Metadata categorizes stored assets, controls browser rendering behavior (`Content-Type: application/pdf`, `Content-Disposition`), records file authorship, and attaches tracking tags for downstream indexing workflows.

## 3. AWS Concept
- `head_object()`: Fast HTTP HEAD call returning object metadata without transferring binary file payloads.
- **In-Place Metadata Update**: Because object keys are immutable, updating metadata on an existing key requires calling `copy_object()` targeting the same key with `MetadataDirective='REPLACE'`.

## 4. Prerequisites
- Target object exists in S3 (e.g. `sample.txt`).
- IAM permissions: `s3:GetObject` / `s3:PutObject`.

## 5. Input
- **Bucket Name**: `my-learning-s3-bucket-unique-12345`
- **Object Key**: `sample.txt`
- **Custom Metadata**: `{"author": "dev-team", "environment": "learning"}`

## 6. Command
```bash
python object_metadata.py --bucket my-learning-s3-bucket-unique-12345 --key sample.txt
```

## 7. Expected Output
```text
[INFO] Fetching metadata for s3://my-learning-s3-bucket-unique-12345/sample.txt...
[SUCCESS] System Metadata:
  - ContentType           : text/plain
  - ContentLength         : 215
  - ETag                  : "d41d8cd98f00b204e9800998ecf8427e"
  - LastModified          : 2026-08-25 15:05:00+00:00

[INFO] Updating metadata on s3://my-learning-s3-bucket-unique-12345/sample.txt...
       New Custom Metadata: {'author': 'dev-team', 'environment': 'learning', 'project': 'aws-operations'}
[SUCCESS] Metadata updated successfully!

[SUCCESS] Custom User Metadata (x-amz-meta-*):
  - x-amz-meta-author         : dev-team
  - x-amz-meta-environment    : learning
  - x-amz-meta-project        : aws-operations
```

## 8. Code
The operation is implemented in [`object_metadata.py`](./object_metadata.py).

## 9. Code Breakdown
- **Line 26**: Uses `head_object(Bucket=..., Key=...)` to retrieve headers.
- **Line 65–71**: Updates metadata using `copy_object` targeting the same key with `MetadataDirective='REPLACE'`.

## 10. Parameter Breakdown
- `Metadata` *(dict)*: Dictionary of custom key-value pairs (S3 automatically prefixes keys with `x-amz-meta-`).
- `MetadataDirective` *(string)*: Must be `'REPLACE'` to overwrite existing metadata, or `'COPY'` to inherit original metadata.

## 11. AWS CLI Equivalent
```bash
# View metadata:
aws s3api head-object --bucket my-learning-s3-bucket-unique-12345 --key sample.txt

# Update metadata in-place:
aws s3api copy-object --bucket my-learning-s3-bucket-unique-12345 --key sample.txt --copy-source my-learning-s3-bucket-unique-12345/sample.txt --metadata author=dev-team,environment=learning --metadata-directive REPLACE
```

## 12. AWS Console Verification
1. Open [AWS S3 Console](https://s3.console.aws.amazon.com/s3/).
2. Click your object `sample.txt`.
3. Scroll down to **System Properties** and **User Metadata** sections.

## 13. Common Errors
- `NoSuchKey`: Key not found.
- `AccessDenied`: Lacking `s3:GetObject` or `s3:PutObject` IAM permissions.

## 14. Troubleshooting
- Remember that user-defined metadata keys are automatically converted to lowercase by AWS S3.

## 15. Security Notes
- Custom metadata values are exposed in unencrypted HTTP response headers; do not store passwords or secret keys in custom metadata.

## 16. Cleanup
Metadata cleanup can be performed by replacing metadata with an empty dict.

## 17. Related Operations
- Previous: [09. Create Folder](../09_create_folder/README.md)
- Next: [11. Object ACL](../11_object_acl/README.md)
