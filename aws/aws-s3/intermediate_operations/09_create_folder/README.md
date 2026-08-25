# 09. Create Logical Folder (Prefix) in S3

## 1. Definition
Creating a logical folder in S3 writes a 0-byte placeholder object whose key ends with a trailing slash (`/`), causing tools and the AWS Console to render it as a directory.

## 2. Why Is It Used?
Logical folders structure flat object key spaces into clean directory hierarchies for human operators in the AWS Console (e.g. `raw_data/`, `processed/`, `reports/2026/`).

## 3. AWS Concept
- **Flat Namespace**: Amazon S3 is a flat key-value store. "Folders" are visual abstractions inferred by delimiting slashes (`/`) in object key strings.
- **Zero-Byte Object**: Creating an explicit folder uploads an empty payload object key named `path/to/folder/`.

## 4. Prerequisites
- Target S3 bucket exists.
- IAM permission: `s3:PutObject`.

## 5. Input
- **Bucket Name**: `my-learning-s3-bucket-unique-12345`
- **Folder Name**: `data/raw_files`

## 6. Command
```bash
python create_folder.py --bucket my-learning-s3-bucket-unique-12345 --folder data/raw_files
```

## 7. Expected Output
```text
[INFO] Creating logical folder 's3://my-learning-s3-bucket-unique-12345/data/raw_files/'...
[SUCCESS] Logical folder created successfully!
         Bucket:     my-learning-s3-bucket-unique-12345
         Folder Key: data/raw_files/
```

## 8. Code
The operation is implemented in [`create_folder.py`](./create_folder.py).

## 9. Code Breakdown
- **Line 26**: Normalizes path string ensuring a trailing `/`.
- **Line 30–34**: Calls `s3_client.put_object(Bucket=..., Key=folder_key, Body=b'')` with zero-byte binary content.

## 10. Parameter Breakdown
- `Key` *(string)*: Object key ending with `/` (e.g. `logs/app/`).
- `Body` *(bytes)*: Empty payload `b''`.

## 11. AWS CLI Equivalent
```bash
aws s3api put-object --bucket my-learning-s3-bucket-unique-12345 --key "data/raw_files/"
```

## 12. AWS Console Verification
1. Open [AWS S3 Console](https://s3.console.aws.amazon.com/s3/).
2. Select bucket `my-learning-s3-bucket-unique-12345`.
3. Confirm directory icon appears for `data/raw_files/`.

## 13. Common Errors
- `AccessDenied`: Missing `s3:PutObject` IAM permission.

## 14. Troubleshooting
- Explicit folder objects are optional in programmatic S3 workflows because uploading an object directly to `data/raw_files/sample.txt` automatically creates the prefix path.

## 15. Security Notes
- Logical folders inherit default bucket policies and encryption.

## 16. Cleanup
To delete logical folder placeholder:
```bash
python ../../basic_operations/05_delete_file/delete_file.py --bucket my-learning-s3-bucket-unique-12345 --key "data/raw_files/" --force
```

## 17. Related Operations
- Previous: [08. Move Object](../08_move_object/README.md)
- Next: [10. Object Metadata](../10_object_metadata/README.md)
