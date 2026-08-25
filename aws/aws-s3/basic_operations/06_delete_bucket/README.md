# 06. Delete S3 Bucket

## 1. Definition
Deleting an S3 bucket permanently removes the top-level S3 bucket container and frees its globally unique name.

## 2. Why Is It Used?
Bucket deletion is used during tear-down phases of ephemeral deployment stacks, automated testing cleanups, or decommissioned project environments to eliminate unnecessary cloud resource billing.

## 3. AWS Concept
- **Bucket Non-Empty Constraint**: AWS S3 API strictly rejects `delete_bucket()` calls on non-empty buckets. All objects, prefixes, version markers, and incomplete multipart uploads must be purged first.
- `delete_bucket()`: Permanently removes the empty bucket container.

## 4. Prerequisites
- Target S3 bucket exists.
- IAM permissions: `s3:DeleteBucket`, `s3:DeleteObject`, `s3:DeleteObjectVersion`, `s3:ListBucketVersions`.

## 5. Input
- **Bucket Name**: `my-learning-s3-bucket-unique-12345`
- **Force Flag**: `--force` (bypasses interactive text confirmation)

## 6. Command
```bash
python delete_bucket.py --bucket my-learning-s3-bucket-unique-12345 --force
```

## 7. Expected Output
```text
[INFO] Emptying all objects and versions from s3://my-learning-s3-bucket-unique-12345...
[SUCCESS] All objects and version markers removed from 'my-learning-s3-bucket-unique-12345'.
[INFO] Deleting empty bucket container 'my-learning-s3-bucket-unique-12345'...
[SUCCESS] Bucket 'my-learning-s3-bucket-unique-12345' has been deleted successfully!
```

## 8. Code
The operation is implemented in [`delete_bucket.py`](./delete_bucket.py).

## 9. Code Breakdown
- **Line 26–36**: Uses `boto3.resource("s3").Bucket(bucket_name).object_versions.delete()` to purge all objects and delete markers in one high-level call.
- **Line 47–51**: Prompts developer to type `'DELETE-BUCKET'` interactively when `--force` is omitted.
- **Line 58–60**: Calls `s3_client.delete_bucket(Bucket=bucket_name)` after confirming the bucket is empty.

## 10. Parameter Breakdown
- `Bucket` *(string)*: Globally unique bucket name to remove.

## 11. AWS CLI Equivalent
```bash
# Force delete all objects and bucket container:
aws s3 rb s3://my-learning-s3-bucket-unique-12345 --force
```

## 12. AWS Console Verification
1. Open the [AWS S3 Console](https://s3.console.aws.amazon.com/s3/).
2. Verify `my-learning-s3-bucket-unique-12345` is no longer in your account bucket listing.

## 13. Common Errors
- `BucketNotEmpty`: Attempted `delete_bucket()` while objects or hidden version markers still remain inside the bucket.
- `AccessDenied`: Missing IAM delete permissions.
- `NoSuchBucket`: Bucket already deleted.

## 14. Troubleshooting
- If `BucketNotEmpty` persists, ensure incomplete multipart uploads are aborted and version markers are purged.

## 15. Security Notes
- **DESTRUCTIVE ACTION**: Deleting a bucket permanently destroys all contained data.
- Restrict `s3:DeleteBucket` permissions strictly to security admin execution roles.

## 16. Cleanup
This operation completes the full lifecycle cleanup of the bucket resource.

## 17. Related Operations
- Previous: [05. Delete File](../05_delete_file/README.md)
- Next: [Intermediate Operations Overview](../../intermediate_operations/README.md)
