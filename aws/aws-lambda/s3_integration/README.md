# AWS Lambda S3 Integration Operations

This module covers serverless event-driven processing patterns connecting Amazon S3 with AWS Lambda.

---

## Operations Map

| # | Operation | Script | Documentation | Description |
|---|---|---|---|---|
| 06 | **S3 Event Trigger** | [`lambda_function.py`](./06_s3_trigger/lambda_function.py) | [README](./06_s3_trigger/README.md) | Parse S3 Event Notification records (`ObjectCreated:Put`) and decode keys. |
| 07 | **S3 File Processing** | [`lambda_function.py`](./07_s3_file_processing/lambda_function.py) | [README](./07_s3_file_processing/README.md) | Download triggered S3 files to `/tmp` storage, process contents, and clean up. |
| 08 | **S3 Event Processing (ETL)** | [`lambda_function.py`](./08_s3_event_processing/lambda_function.py) | [README](./08_s3_event_processing/README.md) | Complete serverless pipeline: Source S3 upload -> Lambda transform -> Destination S3 write. |

---

## Suggested Progression
Execute operations sequentially from `06_s3_trigger` to `08_s3_event_processing` to master serverless S3 event workflows.
