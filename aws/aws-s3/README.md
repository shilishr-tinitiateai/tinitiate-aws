# AWS S3 Operations (Python Boto3 & AWS CLI)

Welcome to the **AWS S3 Operations** module. This section provides complete Python implementation scripts and thorough documentation for 19 AWS S3 operations, categorized into Basic, Intermediate, and Advanced learning tiers.

---

## Operations Index

### 1. Basic Operations (`basic_operations/`)
Fundamental CRUD lifecycle operations for S3 buckets and object keys:
- [01. Create Bucket](./basic_operations/01_create_bucket/README.md)
- [02. Upload File](./basic_operations/02_upload_file/README.md)
- [03. List Buckets and Objects](./basic_operations/03_list_buckets_and_objects/README.md)
- [04. Download File](./basic_operations/04_download_file/README.md)
- [05. Delete File](./basic_operations/05_delete_file/README.md)
- [06. Delete Bucket](./basic_operations/06_delete_bucket/README.md)

### 2. Intermediate Operations (`intermediate_operations/`)
Object manipulation, metadata, security ACLs, presigned access, versioning, and encryption:
- [07. Copy Object](./intermediate_operations/07_copy_object/README.md)
- [08. Move Object](./intermediate_operations/08_move_object/README.md)
- [09. Create Logical Folder](./intermediate_operations/09_create_folder/README.md)
- [10. S3 Object Metadata](./intermediate_operations/10_object_metadata/README.md)
- [11. Object Access Control List (ACL)](./intermediate_operations/11_object_acl/README.md)
- [12. S3 Presigned URL](./intermediate_operations/12_presigned_url/README.md)
- [13. S3 Bucket Versioning](./intermediate_operations/13_bucket_versioning/README.md)
- [14. Default Bucket Encryption](./intermediate_operations/14_bucket_encryption/README.md)

### 3. Advanced Operations (`advanced_operations/`)
Low-level chunking, pagination, S3 Select SQL queries, lifecycle rules, and JSON policies:
- [15. Low-Level Multipart Upload](./advanced_operations/15_multipart_upload/README.md)
- [16. S3 List Pagination](./advanced_operations/16_pagination/README.md)
- [17. S3 Select Query](./advanced_operations/17_s3_select/README.md)
- [18. S3 Lifecycle Configuration](./advanced_operations/18_lifecycle_configuration/README.md)
- [19. S3 Bucket Policy](./advanced_operations/19_bucket_policy/README.md)

---

## General S3 Concepts
- **Globally Unique Bucket Names**: S3 bucket names share a single global DNS namespace across all AWS accounts worldwide.
- **Flat Namespace**: S3 is an object key-value store. Subfolders are virtual abstractions delimited by slashes (`/`).
- **Managed Boto3 API**: Boto3 provides high-level client (`boto3.client('s3')`) and resource (`boto3.resource('s3')`) interfaces.
