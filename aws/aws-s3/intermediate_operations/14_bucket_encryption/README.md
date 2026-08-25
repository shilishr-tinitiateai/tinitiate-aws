# 14. S3 Default Bucket Encryption

## 1. Definition
Default Bucket Encryption ensures that all objects uploaded to an S3 bucket are automatically encrypted at rest on AWS disk infrastructure before writing.

## 2. Why Is It Used?
Encrypting data at rest is a mandatory security compliance requirement across corporate enterprises, protecting raw physical storage media against unauthorized access and satisfying SOC2, HIPAA, and PCI-DSS compliance frameworks.

## 3. AWS Concept
- **SSE-S3 (`AES256`)**: Server-Side Encryption managed by Amazon S3 using 256-bit Advanced Encryption Standard keys.
- **SSE-KMS (`aws:kms`)**: Server-Side Encryption utilizing AWS Key Management Service (KMS) keys, providing granular key access policies and CloudWatch audit trails.
- **Default Behavior**: Effective January 2023, AWS S3 automatically encrypts all new buckets and object uploads with SSE-S3 by default.

## 4. Prerequisites
- Target S3 bucket exists.
- IAM permissions: `s3:GetEncryptionConfiguration`, `s3:PutEncryptionConfiguration`.

## 5. Input
- **Bucket Name**: `my-learning-s3-bucket-unique-12345`
- **Algorithm**: `AES256` (or `aws:kms`)

## 6. Command
```bash
python bucket_encryption.py --bucket my-learning-s3-bucket-unique-12345 --algo AES256
```

## 7. Expected Output
```text
[INFO] Fetching default encryption settings for s3://my-learning-s3-bucket-unique-12345...
[SUCCESS] Found 1 Encryption Rule(s):
  - SSE Algorithm: AES256     | KMS Key ID: N/A (Managed S3 Key)

[INFO] Setting default encryption on s3://my-learning-s3-bucket-unique-12345 -> SSE Algorithm: 'AES256'...
[SUCCESS] Default encryption applied successfully!
```

## 8. Code
The operation is implemented in [`bucket_encryption.py`](./bucket_encryption.py).

## 9. Code Breakdown
- **Line 26**: Queries current encryption settings via `get_bucket_encryption(Bucket=...)`.
- **Line 66–70**: Configures default bucket encryption using `put_bucket_encryption(Bucket=..., ServerSideEncryptionConfiguration={'Rules': [...]})`.

## 10. Parameter Breakdown
- `SSEAlgorithm` *(string)*: `'AES256'` or `'aws:kms'`.
- `KMSMasterKeyID` *(string, optional)*: Key ARN or Alias if using SSE-KMS.

## 11. AWS CLI Equivalent
```bash
# Get encryption configuration:
aws s3api get-bucket-encryption --bucket my-learning-s3-bucket-unique-12345

# Apply SSE-S3 AES256 default encryption:
aws s3api put-bucket-encryption --bucket my-learning-s3-bucket-unique-12345 --server-side-encryption-configuration '{"Rules":[{"ApplyServerSideEncryptionByDefault":{"SSEAlgorithm":"AES256"}}]}'
```

## 12. AWS Console Verification
1. Open [AWS S3 Console](https://s3.console.aws.amazon.com/s3/).
2. Select your bucket and open the **Properties** tab.
3. Scroll down to **Default encryption** section and confirm **Encryption type** displays **SSE-S3** or **SSE-KMS**.

## 13. Common Errors
- `AccessDenied`: Lacking `s3:PutEncryptionConfiguration` IAM permission.
- `KmsAccessDenied`: IAM role lacks permission to invoke `kms:GenerateDataKey` or `kms:Decrypt`.

## 14. Troubleshooting
- When using `aws:kms`, ensure the IAM principal uploading objects has `kms:Decrypt` and `kms:GenerateDataKey` permissions on the KMS Key policy.

## 15. Security Notes
- SSE-S3 incurs no extra KMS API charge, making it ideal for standard workloads. SSE-KMS provides enhanced auditability in CloudTrail.

## 16. Cleanup
Default encryption settings can be updated or removed via `delete_bucket_encryption`.

## 17. Related Operations
- Previous: [13. Bucket Versioning](../13_bucket_versioning/README.md)
- Next: [Advanced Operations Overview](../../advanced_operations/README.md)
