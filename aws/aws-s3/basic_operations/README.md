# AWS S3 Basic Operations

This module covers the core, fundamental CRUD (Create, Read, Update, Delete) lifecycle operations on Amazon Simple Storage Service (S3) using Python `boto3` and the AWS CLI.

---

## Operations Map

| # | Operation | Script | Documentation | Description |
|---|---|---|---|---|
| 01 | **Create Bucket** | [`create_bucket.py`](./01_create_bucket/create_bucket.py) | [README](./01_create_bucket/README.md) | Create a globally unique S3 bucket with region location handling. |
| 02 | **Upload File** | [`upload_file.py`](./02_upload_file/upload_file.py) | [README](./02_upload_file/README.md) | Managed single/multipart file upload to S3. |
| 03 | **List Buckets & Objects** | [`list_buckets_and_objects.py`](./03_list_buckets_and_objects/list_buckets_and_objects.py) | [README](./03_list_buckets_and_objects/README.md) | Enumerate account buckets and list object keys using `list_objects_v2`. |
| 04 | **Download File** | [`download_file.py`](./04_download_file/download_file.py) | [README](./04_download_file/README.md) | Stream S3 object contents to host local filesystem. |
| 05 | **Delete File** | [`delete_file.py`](./05_delete_file/delete_file.py) | [README](./05_delete_file/README.md) | Delete single object key from an S3 bucket with safety checks. |
| 06 | **Delete Bucket** | [`delete_bucket.py`](./06_delete_bucket/delete_bucket.py) | [README](./06_delete_bucket/README.md) | Empty all object keys and version markers, then delete bucket container. |

---

## Suggested Progression
We recommend executing these operations sequentially from `01_create_bucket` to `06_delete_bucket` to experience the complete lifecycle of S3 bucket objects.
