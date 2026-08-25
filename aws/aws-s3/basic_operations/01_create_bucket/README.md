# 01. Create S3 Bucket

## 1. Definition
Creating an S3 bucket provisions a globally unique object storage container within a designated AWS Region to store unstructured data files (objects).

## 2. Why Is It Used?
Bucket creation is the initial prerequisite step in AWS cloud storage architecture. Applications create buckets to segregate environments (e.g., development, staging, production) or organize separate business datasets (e.g., logs, user uploads, backups).

## 3. AWS Concept
- **Bucket**: A top-level container for S3 objects. Bucket names reside in a single global DNS namespace across all AWS accounts globally.
- **Region**: The geographic location where AWS stores the bucket metadata and object data.
- **LocationConstraint**: A parameter required by the S3 API for all regions except `us-east-1`.

## 4. Prerequisites
- Configured AWS credentials (`aws configure` or environment variables).
- IAM permission: `s3:CreateBucket`.

## 5. Input
- **Bucket Name**: `my-learning-s3-bucket-unique-12345` (must be globally unique, 3–63 chars, lowercase, no underscores).
- **Region**: `us-east-1` (or your preferred region, e.g. `ap-south-1`).

## 6. Command
```bash
python create_bucket.py --bucket my-learning-s3-bucket-unique-12345 --region us-east-1
```

## 7. Expected Output
```text
[INFO] Attempting to create S3 bucket 'my-learning-s3-bucket-unique-12345' in region 'us-east-1'...
[SUCCESS] Bucket created successfully!
         Bucket Name: my-learning-s3-bucket-unique-12345
         Location:    /my-learning-s3-bucket-unique-12345
```

## 8. Code
The operation is implemented in [`create_bucket.py`](./create_bucket.py).

## 9. Code Breakdown
- **Line 18–19**: Imports shared Boto3 client initialization (`get_s3_client`) and configuration helpers (`AWS_REGION`, `S3_BUCKET_NAME`).
- **Line 33–34**: Initializes the Boto3 S3 client using standard credentials.
- **Line 37–43**: Handles the AWS region quirk: `us-east-1` omits `CreateBucketConfiguration`, while all other regions pass `LocationConstraint`.
- **Line 47–67**: Catches `ClientError` exceptions specifically targeting `BucketAlreadyOwnedByYou` and `BucketAlreadyExists`.

## 10. Parameter Breakdown
- `Bucket` *(string)*: Name of the bucket to create.
- `CreateBucketConfiguration` *(dict)*: Container for `LocationConstraint`.
- `LocationConstraint` *(string)*: The AWS region identifier (e.g. `ap-south-1`).

## 11. AWS CLI Equivalent
```bash
# For us-east-1:
aws s3 mb s3://my-learning-s3-bucket-unique-12345 --region us-east-1

# For other regions (e.g., ap-south-1):
aws s3api create-bucket --bucket my-learning-s3-bucket-unique-12345 --region ap-south-1 --create-bucket-configuration LocationConstraint=ap-south-1
```

## 12. AWS Console Verification
1. Open the [AWS S3 Console](https://s3.console.aws.amazon.com/s3/).
2. Look for `my-learning-s3-bucket-unique-12345` in the bucket list.
3. Confirm that the **AWS Region** matches your targeted region.

## 13. Common Errors
- `BucketAlreadyExists`: The requested bucket name is taken by another AWS account globally.
- `BucketAlreadyOwnedByYou`: The bucket already exists under your account.
- `InvalidBucketName`: Bucket name contains uppercase letters, underscores, or invalid length.
- `AccessDenied`: Lacking `s3:CreateBucket` IAM permission.

## 14. Troubleshooting
- If you get `BucketAlreadyExists`, add a random suffix or timestamp to your bucket name.
- If you get `IllegalLocationConstraintException`, check that your region string matches standard AWS region codes.

## 15. Security Notes
- Never create public buckets by default.
- Follow least privilege: grant `s3:CreateBucket` only to administrative deployment roles.

## 16. Cleanup
To delete the created bucket, run:
```bash
python ../06_delete_bucket/delete_bucket.py --bucket my-learning-s3-bucket-unique-12345
```

## 17. Related Operations
- Next: [02. Upload File](../02_upload_file/README.md)
- Root S3 Operations: [AWS S3 Overview](../../README.md)
