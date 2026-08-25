# 13. S3 Bucket Versioning

## 1. Definition
Bucket Versioning keeps multiple historical revisions of an object stored in the same S3 bucket, protecting against accidental deletions or overwrites.

## 2. Why Is It Used?
Versioning is essential for backup recovery, disaster prevention, compliance archiving, and audit logging. Once enabled, overwriting an object creates a new version rather than replacing existing data.

## 3. AWS Concept
- `get_bucket_versioning()`: Checks whether versioning state is `Enabled`, `Suspended`, or `Unconfigured`.
- `put_bucket_versioning()`: Configures versioning state. Once enabled, versioning can be `Suspended` but never completely reset to `Unconfigured`.
- `list_object_versions()`: Lists all historical revisions and Delete Markers in a bucket.

## 4. Prerequisites
- Target S3 bucket exists.
- IAM permissions: `s3:GetBucketVersioning`, `s3:PutBucketVersioning`, `s3:ListBucketVersions`.

## 5. Input
- **Bucket Name**: `my-learning-s3-bucket-unique-12345`
- **Versioning Configuration**: `{"Status": "Enabled"}`

## 6. Command
```bash
python bucket_versioning.py --bucket my-learning-s3-bucket-unique-12345
```

## 7. Expected Output
```text
[INFO] Checking versioning status for s3://my-learning-s3-bucket-unique-12345...
[SUCCESS] Bucket Versioning Status: 'Disabled (Never Enabled)'

[INFO] Updating versioning status on s3://my-learning-s3-bucket-unique-12345 -> 'Enabled'...
[SUCCESS] Bucket Versioning configured to 'Enabled' successfully!

[INFO] Checking versioning status for s3://my-learning-s3-bucket-unique-12345...
[SUCCESS] Bucket Versioning Status: 'Enabled'

[INFO] Listing object versions in s3://my-learning-s3-bucket-unique-12345...
[SUCCESS] Found 1 object version(s):
  [LATEST] Key: sample.txt                     | VersionId: a1b2c3d4e5f6... | Size: 215 bytes
```

## 8. Code
The operation is implemented in [`bucket_versioning.py`](./bucket_versioning.py).

## 9. Code Breakdown
- **Line 26**: Queries `s3_client.get_bucket_versioning(Bucket=...)`.
- **Line 50–53**: Updates state using `s3_client.put_bucket_versioning(Bucket=..., VersioningConfiguration={'Status': 'Enabled'})`.
- **Line 81**: Enumerates versions via `s3_client.list_object_versions(Bucket=...)`.

## 10. Parameter Breakdown
- `VersioningConfiguration` *(dict)*: Container specifying `Status` (`'Enabled'` or `'Suspended'`).

## 11. AWS CLI Equivalent
```bash
# Check versioning status:
aws s3api get-bucket-versioning --bucket my-learning-s3-bucket-unique-12345

# Enable versioning:
aws s3api put-bucket-versioning --bucket my-learning-s3-bucket-unique-12345 --versioning-configuration Status=Enabled

# List object versions:
aws s3api list-object-versions --bucket my-learning-s3-bucket-unique-12345
```

## 12. AWS Console Verification
1. Open [AWS S3 Console](https://s3.console.aws.amazon.com/s3/).
2. Select your bucket and click the **Properties** tab.
3. Scroll down to **Bucket Versioning** section and confirm status is **Enabled**.

## 13. Common Errors
- `AccessDenied`: Lacking `s3:PutBucketVersioning` IAM permission.

## 14. Troubleshooting
- Remember that enabling versioning increases storage costs if multiple old object revisions accumulate. Configure S3 Lifecycle rules to expire old noncurrent versions.

## 15. Security Notes
- Combine versioning with **MFA Delete** for critical production buckets to prevent rogue API deletion of historical versions.

## 16. Cleanup
To suspend versioning:
```bash
python bucket_versioning.py --bucket my-learning-s3-bucket-unique-12345 --suspend
```

## 17. Related Operations
- Previous: [12. Presigned URL](../12_presigned_url/README.md)
- Next: [14. Bucket Encryption](../14_bucket_encryption/README.md)
