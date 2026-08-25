# 07. Copy Object in S3

## 1. Definition
Copying an object performs a server-side duplication of S3 data from a source bucket/key to a destination bucket/key inside AWS network boundaries.

## 2. Why Is It Used?
Server-side object copying enables efficient data replication across environments (dev -> prod), renaming keys, creating backups, or shifting data across regions without incurring local internet egress bandwidth overhead.

## 3. AWS Concept
- `copy_object()`: Directly triggers AWS S3 server-side copy.
- **No Local Egress**: Data is transferred entirely within AWS network infrastructure without landing on the client host machine.

## 4. Prerequisites
- Source object exists in source S3 bucket.
- IAM permissions: `s3:GetObject` on source bucket, `s3:PutObject` on destination bucket.

## 5. Input
- **Source Bucket**: `my-learning-s3-bucket-unique-12345`
- **Source Key**: `sample.txt`
- **Destination Bucket**: `my-learning-s3-bucket-unique-12345`
- **Destination Key**: `copies/sample_copy.txt`

## 6. Command
```bash
python copy_object.py --src-bucket my-learning-s3-bucket-unique-12345 --src-key sample.txt --dest-bucket my-learning-s3-bucket-unique-12345 --dest-key copies/sample_copy.txt
```

## 7. Expected Output
```text
[INFO] Copying s3://my-learning-s3-bucket-unique-12345/sample.txt -> s3://my-learning-s3-bucket-unique-12345/copies/sample_copy.txt...
[SUCCESS] Object copied successfully!
         Source:      s3://my-learning-s3-bucket-unique-12345/sample.txt
         Destination: s3://my-learning-s3-bucket-unique-12345/copies/sample_copy.txt
         ETag:        "d41d8cd98f00b204e9800998ecf8427e"
```

## 8. Code
The operation is implemented in [`copy_object.py`](./copy_object.py).

## 9. Code Breakdown
- **Line 26**: Constructs `CopySource = {'Bucket': src_bucket, 'Key': src_key}` dictionary required by Boto3 API.
- **Line 30–34**: Calls `s3_client.copy_object(CopySource=..., Bucket=..., Key=...)`.

## 10. Parameter Breakdown
- `CopySource` *(dict)*: Dictionary identifying source bucket, key, and optional version ID.
- `Bucket` *(string)*: Destination S3 bucket name.
- `Key` *(string)*: Destination object key.

## 11. AWS CLI Equivalent
```bash
aws s3 cp s3://my-learning-s3-bucket-unique-12345/sample.txt s3://my-learning-s3-bucket-unique-12345/copies/sample_copy.txt
```

## 12. AWS Console Verification
1. Open [AWS S3 Console](https://s3.console.aws.amazon.com/s3/).
2. Navigate to bucket `my-learning-s3-bucket-unique-12345`.
3. Open `copies/` folder prefix and verify `sample_copy.txt` exists.

## 13. Common Errors
- `NoSuchKey`: Source object key does not exist.
- `AccessDenied`: Missing read permissions on source or write permissions on destination.

## 14. Troubleshooting
- Ensure `CopySource` format exact key matches source object name.

## 15. Security Notes
- Object metadata and tags are copied by default unless overridden using `MetadataDirective='REPLACE'`.

## 16. Cleanup
To delete copied object:
```bash
python ../../basic_operations/05_delete_file/delete_file.py --bucket my-learning-s3-bucket-unique-12345 --key copies/sample_copy.txt --force
```

## 17. Related Operations
- Previous: [Basic Operations Overview](../../basic_operations/README.md)
- Next: [08. Move Object](../08_move_object/README.md)
