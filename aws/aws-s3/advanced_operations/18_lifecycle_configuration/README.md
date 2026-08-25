# 18. S3 Lifecycle Configuration

## 1. Definition
S3 Lifecycle rules define automated storage management policies that transition objects to cost-effective storage classes (e.g. Standard-IA, Glacier) or permanently expire/delete objects after a specified number of days.

## 2. Why Is It Used?
Automated lifecycle rules optimize cloud storage expenditure by automatically migrating stale data to archival tier classes (Glacier Flexible Retrieval / Deep Archive) and purging unneeded logs or incomplete multipart upload artifacts without human manual intervention.

## 3. AWS Concept
- `put_bucket_lifecycle_configuration()`: Applies a JSON array of lifecycle rule definitions.
- **Transitions**: Specifies when objects migrate to alternative storage classes (e.g. `STANDARD_IA`, `GLACIER`, `DEEP_ARCHIVE`).
- **Expiration**: Specifies when AWS S3 permanently deletes matching objects or noncurrent versions.
- **AbortIncompleteMultipartUpload**: Cleans up failed upload parts left behind by network drops.

## 4. Prerequisites
- Target S3 bucket exists.
- IAM permissions: `s3:GetLifecycleConfiguration`, `s3:PutLifecycleConfiguration`.

## 5. Input
- **Bucket Name**: `my-learning-s3-bucket-unique-12345`
- **Rule 1**: Transition `logs/` to `GLACIER` at 30 days, expire at 365 days.
- **Rule 2**: Abort incomplete multipart uploads after 7 days.

## 6. Command
```bash
python lifecycle_configuration.py --bucket my-learning-s3-bucket-unique-12345
```

## 7. Expected Output
```text
[INFO] Fetching Lifecycle configuration for s3://my-learning-s3-bucket-unique-12345...
[INFO] No lifecycle configuration currently exists for this bucket.

[INFO] Applying Lifecycle configuration to s3://my-learning-s3-bucket-unique-12345...
[SUCCESS] Lifecycle rules applied successfully!

[INFO] Fetching Lifecycle configuration for s3://my-learning-s3-bucket-unique-12345...
[SUCCESS] Found 2 Lifecycle Rule(s):
  - Rule ID: LogArchivalAndExpirationPolicy | Status: Enabled  | Filter Prefix: 'logs/'
  - Rule ID: AbortIncompleteMultipartUploadsPolicy | Status: Enabled  | Filter Prefix: ''
```

## 8. Code
The operation is implemented in [`lifecycle_configuration.py`](./lifecycle_configuration.py).

## 9. Code Breakdown
- **Line 26**: Queries `get_bucket_lifecycle_configuration(Bucket=...)`.
- **Line 50–77**: Constructs rule JSON dictionary and calls `put_bucket_lifecycle_configuration`.

## 10. Parameter Breakdown
- `Filter` *(dict)*: Limits rule applicability to specific key prefixes or object tags.
- `Transitions` *(list)*: Specifies `Days` elapsed and target `StorageClass`.
- `Expiration` *(dict)*: Specifies `Days` until deletion.

## 11. AWS CLI Equivalent
```bash
# Get lifecycle configuration:
aws s3api get-bucket-lifecycle-configuration --bucket my-learning-s3-bucket-unique-12345

# Apply lifecycle configuration:
aws s3api put-bucket-lifecycle-configuration --bucket my-learning-s3-bucket-unique-12345 --lifecycle-configuration file://lifecycle.json
```

## 12. AWS Console Verification
1. Open [AWS S3 Console](https://s3.console.aws.amazon.com/s3/).
2. Select your bucket and click the **Management** tab.
3. Inspect rules listed under **Lifecycle rules**.

## 13. Common Errors
- `InvalidRequest`: Days must be positive integers, or transition sequence invalid (e.g. Glacier transition before Standard-IA).

## 14. Troubleshooting
- Transition to Glacier requires objects to be stored in Standard storage for a minimum of 30 days before migrating.

## 15. Security Notes
- Verify that expiration rules do not conflict with compliance legal hold requirements.

## 16. Cleanup
Delete lifecycle configuration:
```bash
aws s3api delete-bucket-lifecycle --bucket my-learning-s3-bucket-unique-12345
```

## 17. Related Operations
- Previous: [17. S3 Select](../17_s3_select/README.md)
- Next: [19. Bucket Policy](../19_bucket_policy/README.md)
