# 05. Delete File from S3

## 1. Definition
Deleting a file permanently removes an object key (or writes a delete marker in versioned buckets) from an Amazon S3 bucket.

## 2. Why Is It Used?
Applications delete files to clean up temporary upload artifacts, purge expired data, enforce compliance storage retention schedules, or remove user-deleted files.

## 3. AWS Concept
- `delete_object()`: S3 API call that removes the specified object version or key.
- **Versioning Behavior**: If versioning is enabled, calling `delete_object` without specifying a `VersionId` creates a 0-byte **Delete Marker** rather than permanently purging underlying object data.

## 4. Prerequisites
- S3 object must exist in bucket.
- IAM permission: `s3:DeleteObject`.

## 5. Input
- **Bucket Name**: `my-learning-s3-bucket-unique-12345`
- **Object Key**: `sample.txt`
- **Force Flag**: `--force` (skips interactive confirmation prompt)

## 6. Command
```bash
python delete_file.py --bucket my-learning-s3-bucket-unique-12345 --key sample.txt --force
```

## 7. Expected Output
```text
[INFO] Deleting 's3://my-learning-s3-bucket-unique-12345/sample.txt'...
[SUCCESS] Object deleted successfully!
         Bucket: my-learning-s3-bucket-unique-12345
         Key:    sample.txt
```

## 8. Code
The operation is implemented in [`delete_file.py`](./delete_file.py).

## 9. Code Breakdown
- **Line 26–36**: Invokes `head_object` first to confirm object existence prior to deletion.
- **Line 38–43**: Prompts user for interactive `'YES'` confirmation unless `--force` is set.
- **Line 47–53**: Calls `s3_client.delete_object(Bucket, Key)` and checks response metadata.

## 10. Parameter Breakdown
- `Bucket` *(string)*: Target S3 bucket.
- `Key` *(string)*: Object key identifier to delete.
- `VersionId` *(string, optional)*: Specific version identifier to purge in versioned buckets.

## 11. AWS CLI Equivalent
```bash
aws s3 rm s3://my-learning-s3-bucket-unique-12345/sample.txt
```

## 12. AWS Console Verification
1. Open the [AWS S3 Console](https://s3.console.aws.amazon.com/s3/).
2. Click your bucket `my-learning-s3-bucket-unique-12345`.
3. Confirm `sample.txt` is no longer present in the object listing.

## 13. Common Errors
- `AccessDenied`: Lacking `s3:DeleteObject` IAM permission.
- `NoSuchBucket`: Target bucket name invalid.

## 14. Troubleshooting
- If deleted objects remain visible in versioned buckets, enable "Show versions" in the S3 console to inspect Delete Markers.

## 15. Security Notes
- Deletion is irreversible unless Bucket Versioning or Multi-Factor Authentication (MFA) Delete is enabled.
- Always implement confirmation checks in automated administrative scripts.

## 16. Cleanup
This operation cleans up the object itself.

## 17. Related Operations
- Previous: [04. Download File](../04_download_file/README.md)
- Next: [06. Delete Bucket](../06_delete_bucket/README.md)
