# 11. S3 Object Access Control List (ACL)

## 1. Definition
An Access Control List (ACL) is a legacy resource-based access policy mechanism in Amazon S3 that defines which AWS accounts or predefined groups are granted read or write permissions to buckets and individual objects.

## 2. Why Is It Used?
Historically, ACLs were used to grant public read access to specific assets (e.g. `public-read`) or cross-account access. In modern cloud architecture, AWS recommends disabling ACLs entirely.

## 3. AWS Concept
- `get_object_acl()`: Reads current grants and owner information for an object.
- `put_object_acl()`: Applies a canned ACL (e.g. `private`, `bucket-owner-full-control`).
- **S3 Object Ownership**: Modern S3 buckets default to **Bucket Owner Enforced**, which disables ACLs completely and forces access control through IAM policies.

## 4. Prerequisites
- S3 object exists in target bucket.
- IAM permissions: `s3:GetObjectAcl`, `s3:PutObjectAcl`.

## 5. Input
- **Bucket Name**: `my-learning-s3-bucket-unique-12345`
- **Object Key**: `sample.txt`
- **Canned ACL**: `private`

## 6. Command
```bash
python object_acl.py --bucket my-learning-s3-bucket-unique-12345 --key sample.txt --acl private
```

## 7. Expected Output
```text
[INFO] Reading ACL for s3://my-learning-s3-bucket-unique-12345/sample.txt...
[SUCCESS] Object Owner: dev-user (ID: 1234567890abcdef...)
[SUCCESS] Found 1 Grant(s):
  - Grantee Type: CanonicalUser | Permission: FULL_CONTROL | ID: 1234567890abcdef...

[INFO] Setting canned ACL 'private' on s3://my-learning-s3-bucket-unique-12345/sample.txt...
[SUCCESS] Object ACL updated to 'private' successfully!
```
*(Note: If ACLs are disabled on your bucket, the script prints an informational message regarding `AccessControlListNotSupported`.)*

## 8. Code
The operation is implemented in [`object_acl.py`](./object_acl.py).

## 9. Code Breakdown
- **Line 26**: Invokes `get_object_acl(Bucket=..., Key=...)`.
- **Line 60–64**: Invokes `put_object_acl(Bucket=..., Key=..., ACL='private')`.
- **Line 66–69**: Handles `AccessControlListNotSupported` gracefully.

## 10. Parameter Breakdown
- `ACL` *(string)*: Canned ACL identifier (`private`, `public-read`, `bucket-owner-full-control`).

## 11. AWS CLI Equivalent
```bash
# Get ACL:
aws s3api get-object-acl --bucket my-learning-s3-bucket-unique-12345 --key sample.txt

# Put Canned ACL:
aws s3api put-object-acl --bucket my-learning-s3-bucket-unique-12345 --key sample.txt --acl private
```

## 12. AWS Console Verification
1. Open [AWS S3 Console](https://s3.console.aws.amazon.com/s3/).
2. Select your object `sample.txt` and click **Permissions** tab.
3. Inspect Access Control List settings.

## 13. Common Errors
- `AccessControlListNotSupported`: ACLs are disabled on the target bucket (Bucket Owner Enforced).
- `AccessDenied`: Lacking `s3:PutObjectAcl` IAM permission.

## 14. Troubleshooting
- If your application requires setting object ACLs, change the bucket's Object Ownership setting to "Bucket owner preferred" or "Object writer" in the S3 console.

## 15. Security Notes
- **AWS Best Practice**: Disable ACLs on all production S3 buckets. Rely exclusively on IAM policies and S3 Bucket Policies for security controls.

## 16. Cleanup
No special cleanup required.

## 17. Related Operations
- Previous: [10. Object Metadata](../10_object_metadata/README.md)
- Next: [12. Presigned URL](../12_presigned_url/README.md)
