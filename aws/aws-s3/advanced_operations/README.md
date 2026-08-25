# AWS S3 Advanced Operations

This module covers advanced Amazon S3 data operations, high-performance streaming, SQL querying, automated lifecycle retention, and bucket security policies.

---

## Operations Map

| # | Operation | Script | Documentation | Description |
|---|---|---|---|---|
| 15 | **Multipart Upload** | [`multipart_upload.py`](./15_multipart_upload/multipart_upload.py) | [README](./15_multipart_upload/README.md) | High-performance low-level chunked multipart upload with failure abort handling. |
| 16 | **Pagination** | [`pagination.py`](./16_pagination/pagination.py) | [README](./16_pagination/README.md) | Enumerate large datasets across multiple pages using Boto3 `Paginator`. |
| 17 | **S3 Select** | [`s3_select.py`](./17_s3_select/s3_select.py) | [README](./17_s3_select/README.md) | Query CSV/JSON object contents directly in S3 using server-side SQL expressions. |
| 18 | **Lifecycle Config** | [`lifecycle_configuration.py`](./18_lifecycle_configuration/lifecycle_configuration.py) | [README](./18_lifecycle_configuration/README.md) | Define automated object transitions to Glacier and expiration rules. |
| 19 | **Bucket Policy** | [`bucket_policy.py`](./19_bucket_policy/bucket_policy.py) | [README](./19_bucket_policy/README.md) | Apply and validate JSON IAM Bucket Access Policies (e.g. HTTPS enforcement). |

---

## Suggested Progression
Execute operations sequentially from `15_multipart_upload` to `19_bucket_policy` to master advanced S3 cloud operations.
