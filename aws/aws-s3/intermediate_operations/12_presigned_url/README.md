# 12. S3 Presigned URL

## 1. Definition
A Presigned URL embeds temporary AWS IAM authorization credentials directly into an HTTP query string, allowing unauthenticated clients to read (GET) or upload (PUT) a specific S3 object for a limited timeframe.

## 2. Why Is It Used?
Presigned URLs allow secure client-side browser file uploads and downloads directly to/from Amazon S3 without routing heavy binary traffic through backend application servers or exposing long-lived IAM keys.

## 3. AWS Concept
- `generate_presigned_url()`: Cryptographically signs an S3 API endpoint URL using the active AWS identity's secret key.
- **Expiration**: Range from 1 second to 604,800 seconds (7 days).
- **Security Scope**: The Presigned URL possesses exactly the same permissions as the IAM user or role that generated it at the time of access.

## 4. Prerequisites
- Target object uploaded in S3.
- IAM permissions: `s3:GetObject` (for GET URLs) or `s3:PutObject` (for PUT URLs).

## 5. Input
- **Bucket Name**: `my-learning-s3-bucket-unique-12345`
- **Object Key**: `sample.txt`
- **Expiration**: `3600` seconds (1 hour)

## 6. Command
```bash
python presigned_url.py --bucket my-learning-s3-bucket-unique-12345 --key sample.txt --expires 3600
```

## 7. Expected Output
```text
[INFO] Generating presigned URL for method 'get_object' on s3://my-learning-s3-bucket-unique-12345/sample.txt...
       Expiration: 3600 seconds (60 minutes)
[SUCCESS] Presigned URL generated successfully!
         URL: https://my-learning-s3-bucket-unique-12345.s3.us-east-1.amazonaws.com/sample.txt?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=...

[INFO] Testing HTTP GET download using presigned URL...
[SUCCESS] HTTP GET Status Code: 200
         Downloaded Content Snippet (215 bytes):
         'Hello from AWS S3 & AWS Lambda Operations Repository!...'
```

## 8. Code
The operation is implemented in [`presigned_url.py`](./presigned_url.py).

## 9. Code Breakdown
- **Line 26–31**: Invokes `s3_client.generate_presigned_url(ClientMethod='get_object', Params={'Bucket': ..., 'Key': ...}, ExpiresIn=3600)`.
- **Line 46–55**: Performs a native HTTP GET using Python's `urllib.request` to prove valid unauthenticated URL access.

## 10. Parameter Breakdown
- `ClientMethod` *(string)*: Boto3 client method to presign (`get_object`, `put_object`).
- `Params` *(dict)*: Dictionary containing `Bucket` and `Key`.
- `ExpiresIn` *(int)*: Time to live in seconds.

## 11. AWS CLI Equivalent
```bash
# Generate GET presigned URL for 1 hour:
aws s3 presign s3://my-learning-s3-bucket-unique-12345/sample.txt --expires-in 3600
```

## 12. AWS Console Verification
1. Open [AWS S3 Console](https://s3.console.aws.amazon.com/s3/).
2. Select `sample.txt`.
3. Click **Actions** -> **Open** (which internally generates a 5-minute GET presigned URL).

## 13. Common Errors
- `AccessDenied` (HTTP 403 on URL access): Occurs if the IAM identity that generated the presigned URL loses permissions, or if credentials expire (e.g. temporary STS credentials).
- `RequestExpired`: The timeframe specified in `ExpiresIn` has passed.

## 14. Troubleshooting
- If using temporary STS credentials (e.g., AWS SSO or Lambda execution role), the URL expiration cannot exceed the lifetime of the STS session.

## 15. Security Notes
- Treat presigned URLs like temporary access tokens. Do not log full presigned URLs in public logging aggregators.

## 16. Cleanup
Presigned URLs expire automatically once `ExpiresIn` seconds elapse.

## 17. Related Operations
- Previous: [11. Object ACL](../11_object_acl/README.md)
- Next: [13. Bucket Versioning](../13_bucket_versioning/README.md)
