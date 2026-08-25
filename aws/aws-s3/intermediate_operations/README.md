# AWS S3 Intermediate Operations

This module covers intermediate management operations on Amazon S3, focusing on object manipulation, security, version control, metadata, and presigned authorization.

---

## Operations Map

| # | Operation | Script | Documentation | Description |
|---|---|---|---|---|
| 07 | **Copy Object** | [`copy_object.py`](./07_copy_object/copy_object.py) | [README](./07_copy_object/README.md) | Duplicate objects server-side across buckets or keys without local egress. |
| 08 | **Move Object** | [`move_object.py`](./08_move_object/move_object.py) | [README](./08_move_object/README.md) | Move/rename object keys via atomic copy-and-delete workflow. |
| 09 | **Create Folder** | [`create_folder.py`](./09_create_folder/create_folder.py) | [README](./09_create_folder/README.md) | Create logical directory prefixes using 0-byte trailing slash objects. |
| 10 | **Object Metadata** | [`object_metadata.py`](./10_object_metadata/object_metadata.py) | [README](./10_object_metadata/README.md) | Inspect system HTTP headers and update user-defined custom metadata (`x-amz-meta-*`). |
| 11 | **Object ACL** | [`object_acl.py`](./11_object_acl/object_acl.py) | [README](./11_object_acl/README.md) | Inspect and manage legacy Access Control Lists (ACLs) and Bucket Owner Enforcement. |
| 12 | **Presigned URL** | [`presigned_url.py`](./12_presigned_url/presigned_url.py) | [README](./12_presigned_url/README.md) | Generate temporary GET/PUT presigned URLs for client authorization. |
| 13 | **Bucket Versioning** | [`bucket_versioning.py`](./13_bucket_versioning/bucket_versioning.py) | [README](./13_bucket_versioning/README.md) | Enable and manage S3 Bucket Versioning and revision listings. |
| 14 | **Bucket Encryption** | [`bucket_encryption.py`](./14_bucket_encryption/bucket_encryption.py) | [README](./14_bucket_encryption/README.md) | Configure default server-side encryption (SSE-S3 AES256 / SSE-KMS). |

---

## Suggested Progression
Execute operations sequentially from `07_copy_object` to `14_bucket_encryption` to build proficiency in intermediate S3 cloud management.
