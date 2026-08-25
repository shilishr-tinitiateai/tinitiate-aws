# 17. S3 Select Query

## 1. Definition
S3 Select filters binary and structured object contents (CSV, JSON, GZIP, Parquet) directly at the S3 storage layer using standard ANSI SQL queries, returning only requested data fields.

## 2. Why Is It Used?
Instead of pulling multi-gigabyte log or data files over the network to application servers for local filtering, S3 Select performs server-side data projection, reducing network egress bandwidth by up to 95% and boosting query speeds.

## 3. AWS Concept
- `select_object_content()`: Event-streamed API executing SQL expressions on structured S3 object keys.
- **Payload Event Stream**: The response streams back payload events (`Records`, `Stats`, `Progress`, `End`).

## 4. Prerequisites
- Structured JSON or CSV object stored in target S3 bucket (e.g. `examples/sample.json`).
- IAM permission: `s3:GetObject`.

## 5. Input
- **Bucket Name**: `my-learning-s3-bucket-unique-12345`
- **Object Key**: `sample.json`
- **SQL Query**: `SELECT s.name, s.amount FROM S3Object[*].records[*] s WHERE s.amount > 100.0`

## 6. Command
```bash
python s3_select.py --bucket my-learning-s3-bucket-unique-12345 --key sample.json
```

## 7. Expected Output
```text
[INFO] Executing S3 Select query on s3://my-learning-s3-bucket-unique-12345/sample.json...
       SQL Expression: "SELECT s.name, s.amount FROM S3Object[*].records[*] s WHERE s.amount > 100.0"
[INFO] Query Stats - Bytes Scanned: 368, Processed: 368
[SUCCESS] S3 Select Query Result:
----------------------------------------
{"name":"Invoice Alpha","amount":250.5}
{"name":"Report Beta","amount":120.0}
----------------------------------------
```

## 8. Code
The operation is implemented in [`s3_select.py`](./s3_select.py).

## 9. Code Breakdown
- **Line 33–40**: Invokes `select_object_content(Bucket=..., Key=..., Expression=..., InputSerialization=..., OutputSerialization=...)`.
- **Line 42–49**: Loops through payload event stream decoding binary chunk events into text strings.

## 10. Parameter Breakdown
- `ExpressionType` *(string)*: Must be `'SQL'`.
- `InputSerialization` *(dict)*: Defines format (`JSON`, `CSV`, or `Parquet`).
- `OutputSerialization` *(dict)*: Format returned to client (`JSON` or `CSV`).

## 11. AWS CLI Equivalent
```bash
aws s3api select-object-content --bucket my-learning-s3-bucket-unique-12345 --key sample.json --expression "SELECT s.name, s.amount FROM S3Object[*].records[*] s WHERE s.amount > 100.0" --expression-type SQL --input-serialization '{"JSON": {"Type": "DOCUMENT"}}' --output-serialization '{"JSON": {"RecordDelimiter": "\n"}}' output.json
```

## 12. AWS Console Verification
1. Open [AWS S3 Console](https://s3.console.aws.amazon.com/s3/).
2. Select `sample.json` and click **Actions** -> **Query with S3 Select**.
3. Choose input format (JSON) and execute SQL preview.

## 13. Common Errors
- `InvalidTextEncoding`: JSON or CSV formatting invalid.
- `SqlParseException`: Syntax error in SQL query string.

## 14. Troubleshooting
- Verify JSON document structure (single JSON object vs. line-delimited JSON records).

## 15. Security Notes
- S3 Select respects object-level encryption (SSE-S3, SSE-KMS) automatically.

## 16. Cleanup
Delete sample JSON file if no longer required:
```bash
python ../../basic_operations/05_delete_file/delete_file.py --bucket my-learning-s3-bucket-unique-12345 --key sample.json --force
```

## 17. Related Operations
- Previous: [16. Pagination](../16_pagination/README.md)
- Next: [18. Lifecycle Configuration](../18_lifecycle_configuration/README.md)
