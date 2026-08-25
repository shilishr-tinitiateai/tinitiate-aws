# 16. S3 List Pagination

## 1. Definition
Pagination retrieves large datasets from AWS S3 API listing operations across multiple sequential response pages when total items exceed single-request API response limits.

## 2. Why Is It Used?
Amazon S3 caps single `list_objects_v2` requests to a maximum of 1,000 object keys. Pagination prevents API buffer overflow and memory strain when enumerating buckets containing tens of thousands or millions of files.

## 3. AWS Concept
- `get_paginator('list_objects_v2')`: High-level Boto3 paginator helper that automatically handles `NextContinuationToken` pass-through loop logic under the hood.
- `PaginationConfig`: Configuration container for parameters such as `PageSize` (items per API page) and `MaxItems` (overall total cap).

## 4. Prerequisites
- Target S3 bucket exists and contains objects.
- IAM permission: `s3:ListBucket`.

## 5. Input
- **Bucket Name**: `my-learning-s3-bucket-unique-12345`
- **Page Size**: `2` (artificially restricted to demonstrate multi-page looping)

## 6. Command
```bash
python pagination.py --bucket my-learning-s3-bucket-unique-12345 --page-size 2
```

## 7. Expected Output
```text
[INFO] Initializing Paginator for list_objects_v2 on s3://my-learning-s3-bucket-unique-12345...
       Page Size (MaxKeys): 2

[PAGE 1] Retrieved 2 object(s) in page:
  - Key: sample.txt                          | Size: 215 bytes
  - Key: copies/sample_copy.txt              | Size: 215 bytes

[PAGE 2] Retrieved 1 object(s) in page:
  - Key: multipart/sample_large.txt          | Size: 215 bytes

[SUCCESS] Pagination complete! Retrieved 3 total object(s) across 2 page(s).
```

## 8. Code
The operation is implemented in [`pagination.py`](./pagination.py).

## 9. Code Breakdown
- **Line 33**: Creates paginator instance via `s3_client.get_paginator("list_objects_v2")`.
- **Line 34–38**: Initializes `paginate(Bucket=..., PaginationConfig={'PageSize': page_size})`.
- **Line 40–46**: Iterates through returned pages seamlessly without manual token management.

## 10. Parameter Breakdown
- `PageSize` *(int)*: Limits number of items returned per individual HTTP page request.
- `StartingToken` *(string)*: Optional continuation token to resume pagination from a specific page.

## 11. AWS CLI Equivalent
```bash
# AWS CLI automatically handles pagination for listing commands:
aws s3api list-objects-v2 --bucket my-learning-s3-bucket-unique-12345 --max-items 100
```

## 12. AWS Console Verification
1. Open [AWS S3 Console](https://s3.console.aws.amazon.com/s3/).
2. Bucket object lists automatically paginate at 300 items per page in the Web Console UI.

## 13. Common Errors
- `AccessDenied`: Missing `s3:ListBucket` permission.

## 14. Troubleshooting
- Always use `Paginator` instead of manual `while response.get('IsTruncated')` loops to reduce boilerplate code and prevent infinite loops.

## 15. Security Notes
- Pagination operations are read-only metadata requests.

## 16. Cleanup
No resource cleanup required.

## 17. Related Operations
- Previous: [15. Multipart Upload](../15_multipart_upload/README.md)
- Next: [17. S3 Select](../17_s3_select/README.md)
