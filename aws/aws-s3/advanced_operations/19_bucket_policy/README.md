# 19. S3 Bucket Policy

## 1. Definition
An S3 Bucket Policy is a JSON resource-based access policy attached directly to an S3 bucket to grant or restrict fine-grained permissions for IAM principals, anonymous web requests, or cross-account access.

## 2. Why Is It Used?
Bucket Policies enforce security governance rules across entire storage containers—such as enforcing HTTPS/TLS-only transport (`aws:SecureTransport`), blocking unencrypted uploads, restricting access to specific VPC Endpoints, or granting read access to AWS Lambda functions.

## 3. AWS Concept
- `get_bucket_policy()`: Retrieves active JSON policy string.
- `put_bucket_policy()`: Replaces bucket policy with new JSON string.
- `delete_bucket_policy()`: Clears active policy.
- **Resource ARNs**: Identifies the bucket container (`arn:aws:s3:::bucket-name`) and objects inside (`arn:aws:s3:::bucket-name/*`).

## 4. Prerequisites
- Target S3 bucket exists.
- IAM permissions: `s3:GetBucketPolicy`, `s3:PutBucketPolicy`, `s3:DeleteBucketPolicy`.

## 5. Input
- **Bucket Name**: `my-learning-s3-bucket-unique-12345`
- **Policy Standard**: Deny unencrypted HTTP access (`aws:SecureTransport: false`).

## 6. Command
```bash
python bucket_policy.py --bucket my-learning-s3-bucket-unique-12345
```

## 7. Expected Output
```text
[INFO] Reading Bucket Policy for s3://my-learning-s3-bucket-unique-12345...
[INFO] No custom Bucket Policy currently applied to this bucket.

[INFO] Applying Enforce-HTTPS Bucket Policy to s3://my-learning-s3-bucket-unique-12345...
[SUCCESS] Bucket Policy applied successfully!

[INFO] Reading Bucket Policy for s3://my-learning-s3-bucket-unique-12345...
[SUCCESS] Active Bucket Policy:
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "EnforceHTTPSTransportOnly",
      "Effect": "Deny",
      "Principal": "*",
      "Action": "s3:*",
      "Resource": [
        "arn:aws:s3:::my-learning-s3-bucket-unique-12345",
        "arn:aws:s3:::my-learning-s3-bucket-unique-12345/*"
      ],
      "Condition": {
        "Bool": {
          "aws:SecureTransport": "false"
        }
      }
    }
  ]
}
```

## 8. Code
The operation is implemented in [`bucket_policy.py`](./bucket_policy.py).

## 9. Code Breakdown
- **Line 26**: Queries `get_bucket_policy(Bucket=...)`.
- **Line 50–77**: Constructs JSON policy dictionary enforcing TLS transport and calls `put_bucket_policy(Bucket=..., Policy=json_str)`.

## 10. Parameter Breakdown
- `Bucket` *(string)*: Target S3 bucket.
- `Policy` *(string)*: Valid JSON IAM Policy document string.

## 11. AWS CLI Equivalent
```bash
# Get policy:
aws s3api get-bucket-policy --bucket my-learning-s3-bucket-unique-12345

# Apply policy:
aws s3api put-bucket-policy --bucket my-learning-s3-bucket-unique-12345 --policy file://policy.json
```

## 12. AWS Console Verification
1. Open [AWS S3 Console](https://s3.console.aws.amazon.com/s3/).
2. Select your bucket and click the **Permissions** tab.
3. Scroll down to **Bucket policy** and review JSON content.

## 13. Common Errors
- `MalformedPolicy`: JSON syntax invalid or non-existent ARN referenced in Principal/Resource.
- `AccessDenied`: Lacking `s3:PutBucketPolicy` IAM permission or self-lockout error.

## 14. Troubleshooting
- **WARNING**: Avoid applying explicit `"Effect": "Deny"` policies without proper condition keys, which can cause administrative lockout from the bucket.

## 15. Security Notes
- Enforcing `aws:SecureTransport: false` -> `Deny` is an AWS Security Hub top-recommendation best practice.

## 16. Cleanup
To remove applied policy:
```bash
python bucket_policy.py --bucket my-learning-s3-bucket-unique-12345 --delete
```

## 17. Related Operations
- Previous: [18. Lifecycle Configuration](../18_lifecycle_configuration/README.md)
- Next: [AWS Lambda Operations Overview](../../../aws-lambda/README.md)
