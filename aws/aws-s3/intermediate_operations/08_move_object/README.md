# 08. Move Object in S3

## 1. Definition
Moving an S3 object relocates data from an existing object key to a new object key (or destination bucket) and removes the original source key.

## 2. Why Is It Used?
Moving objects is used to rename object keys, transition processed data files from an `incoming/` prefix to a `processed/` or `archived/` prefix, or restructure bucket storage organization.

## 3. AWS Concept
- **No Native Rename API**: AWS S3 object keys are immutable. Moving an object is implemented via an atomic 2-step process: `copy_object()` followed by `delete_object()`.

## 4. Prerequisites
- Source object exists in source S3 bucket.
- IAM permissions: `s3:GetObject` and `s3:DeleteObject` on source bucket, `s3:PutObject` on destination bucket.

## 5. Input
- **Source Bucket**: `my-learning-s3-bucket-unique-12345`
- **Source Key**: `copies/sample_copy.txt`
- **Destination Bucket**: `my-learning-s3-bucket-unique-12345`
- **Destination Key**: `archived/sample_moved.txt`

## 6. Command
```bash
python move_object.py --src-bucket my-learning-s3-bucket-unique-12345 --src-key copies/sample_copy.txt --dest-bucket my-learning-s3-bucket-unique-12345 --dest-key archived/sample_moved.txt
```

## 7. Expected Output
```text
[INFO] Initiating Move: s3://my-learning-s3-bucket-unique-12345/copies/sample_copy.txt -> s3://my-learning-s3-bucket-unique-12345/archived/sample_moved.txt
       [Step 1/2] Copying server-side...
       [Step 1/2] Copy complete.
       [Step 2/2] Deleting source object...
       [Step 2/2] Source deleted.
[SUCCESS] Object move completed successfully!
         Old Location: s3://my-learning-s3-bucket-unique-12345/copies/sample_copy.txt
         New Location: s3://my-learning-s3-bucket-unique-12345/archived/sample_moved.txt
```

## 8. Code
The operation is implemented in [`move_object.py`](./move_object.py).

## 9. Code Breakdown
- **Line 35–40**: Step 1 executes server-side copy (`s3_client.copy_object`).
- **Line 44–47**: Step 2 deletes original key (`s3_client.delete_object`) only after Step 1 succeeds.

## 10. Parameter Breakdown
- `CopySource` *(dict)*: Identifies source bucket and key.
- `Bucket` & `Key`: Specifies destination bucket and key.

## 11. AWS CLI Equivalent
```bash
aws s3 mv s3://my-learning-s3-bucket-unique-12345/copies/sample_copy.txt s3://my-learning-s3-bucket-unique-12345/archived/sample_moved.txt
```

## 12. AWS Console Verification
1. Open [AWS S3 Console](https://s3.console.aws.amazon.com/s3/).
2. Verify `copies/sample_copy.txt` no longer exists.
3. Open `archived/` prefix and confirm `sample_moved.txt` is present.

## 13. Common Errors
- `NoSuchKey`: Source object missing.
- `AccessDenied`: Missing `s3:DeleteObject` permission on source.

## 14. Troubleshooting
- If copy succeeds but delete fails, check source bucket `s3:DeleteObject` IAM policy restrictions.

## 15. Security Notes
- Validate copy completion status prior to executing source key deletion.

## 16. Cleanup
To delete relocated object:
```bash
python ../../basic_operations/05_delete_file/delete_file.py --bucket my-learning-s3-bucket-unique-12345 --key archived/sample_moved.txt --force
```

## 17. Related Operations
- Previous: [07. Copy Object](../07_copy_object/README.md)
- Next: [09. Create Folder](../09_create_folder/README.md)
