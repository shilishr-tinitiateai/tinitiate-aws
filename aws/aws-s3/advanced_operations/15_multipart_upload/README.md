# 15. Low-Level S3 Multipart Upload

## 1. Definition
Multipart Upload breaks large binary files into smaller chunked parts, uploads parts independently in parallel, and reassembles them server-side into a single destination S3 object.

## 2. Why Is It Used?
Multipart upload is mandatory for objects exceeding 5 GB and strongly recommended for files larger than 100 MB. It improves network throughput via parallel part streaming and enables quick resume if a single part fails without restarting the entire transfer.

## 3. AWS Concept
- `create_multipart_upload()`: Initiates transfer and returns an `UploadId`.
- `upload_part()`: Uploads an individual part (minimum 5 MB per part except the final part) and returns an `ETag`.
- `complete_multipart_upload()`: Assembles parts in sequential `PartNumber` order.
- `abort_multipart_upload()`: Cleans up incomplete part data stored in S3 to prevent background storage billing.

## 4. Prerequisites
- Target S3 bucket exists.
- IAM permissions: `s3:PutObject`, `s3:AbortMultipartUpload`.

## 5. Input
- **Bucket Name**: `my-learning-s3-bucket-unique-12345`
- **Local File**: `examples/sample.txt`
- **Object Key**: `multipart/sample_large.txt`
- **Chunk Size**: `5 MB`

## 6. Command
```bash
python multipart_upload.py --bucket my-learning-s3-bucket-unique-12345 --file ../../../examples/sample.txt --key multipart/sample_large.txt
```

## 7. Expected Output
```text
[INFO] Starting Low-Level Multipart Upload for 'sample.txt' (215 bytes)...
       Destination: s3://my-learning-s3-bucket-unique-12345/multipart/sample_large.txt
       Chunk Size:  5.0 MB
       [Step 1/3] Initiated Multipart Upload. UploadId: 2v1A8z...
       [Step 2/3] Uploading Part 1 (215 bytes)...
       [Step 2/3] Part 1 uploaded. ETag: "d41d8cd98f00b204e9800998ecf8427e"
       [Step 3/3] Completing Multipart Upload with 1 part(s)...
[SUCCESS] Low-level Multipart Upload completed successfully!
         Location: https://my-learning-s3-bucket-unique-12345.s3.us-east-1.amazonaws.com/multipart/sample_large.txt
         ETag:     "d41d8cd98f00b204e9800998ecf8427e-1"
```

## 8. Code
The operation is implemented in [`multipart_upload.py`](./multipart_upload.py).

## 9. Code Breakdown
- **Line 41**: Calls `s3_client.create_multipart_upload` to retrieve `UploadId`.
- **Line 47–61**: Streams chunks from local disk file and uploads parts with incrementing `PartNumber`.
- **Line 65–70**: Assembles parts array into `complete_multipart_upload`.
- **Line 78–82**: Intercepts errors and invokes `abort_multipart_upload` to prevent orphaned part storage charges.

## 10. Parameter Breakdown
- `UploadId` *(string)*: Unique identifier returned during initiation.
- `PartNumber` *(int)*: 1-indexed part sequence number (1 to 10,000).
- `MultipartUpload` *(dict)*: Array containing `PartNumber` and `ETag` for every uploaded part.

## 11. AWS CLI Equivalent
```bash
# High-level CLI automatically uses multipart upload for large files:
aws s3 cp large_file.bin s3://my-learning-s3-bucket-unique-12345/multipart/large_file.bin
```

## 12. AWS Console Verification
1. Open [AWS S3 Console](https://s3.console.aws.amazon.com/s3/).
2. Navigate to bucket `my-learning-s3-bucket-unique-12345`.
3. Open `multipart/` folder and verify `sample_large.txt` exists.

## 13. Common Errors
- `EntityTooSmall`: Part size is less than 5 MB (except the last part).
- `InvalidPart`: ETag or PartNumber array mismatch during completion.

## 14. Troubleshooting
- Configure S3 Lifecycle rules (`AbortIncompleteMultipartUpload`) to automatically clear failed multipart uploads older than 7 days.

## 15. Security Notes
- Secure uploaded parts using server-side encryption parameters in `create_multipart_upload`.

## 16. Cleanup
To delete uploaded file:
```bash
python ../../basic_operations/05_delete_file/delete_file.py --bucket my-learning-s3-bucket-unique-12345 --key multipart/sample_large.txt --force
```

## 17. Related Operations
- Previous: [Intermediate Operations Overview](../../intermediate_operations/README.md)
- Next: [16. Pagination](../16_pagination/README.md)
