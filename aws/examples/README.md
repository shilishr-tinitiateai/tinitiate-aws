# Examples Directory Overview

The `examples/` directory contains sample source assets used by operations throughout the repository for testing file uploads, S3 Select queries, presigned URL downloads, and Lambda payload event triggers.

---

## Files Included

1. **`sample.txt`**: Standard plain text asset used for:
   - S3 Upload (`aws-s3/basic_operations/02_upload_file`)
   - S3 Object Copy & Move operations
   - S3 Presigned URL GET / PUT testing

2. **`sample.json`**: Structured JSON data file used for:
   - S3 Select queries (`aws-s3/advanced_operations/17_s3_select`)
   - Lambda event parsing & file processing (`aws-lambda/s3_integration/07_s3_file_processing`)

---

## Portability Notice

All Python scripts access these files using relative paths resolved dynamically via `shared.config.LOCAL_SAMPLE_FILE` or Python's `pathlib.Path`, ensuring seamless compatibility across Windows, Linux, and macOS.
