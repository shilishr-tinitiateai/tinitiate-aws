# 🧩 Example 4: Fault-Tolerant Multipart Large File Uploader

Welcome to **Example 4**! This beginner-friendly guide demonstrates how to upload large files (> 100MB up to 5TB) using the AWS S3 **Multipart Upload API**.

---

## 🎯 What Does This Example Do?

1. **Initiate**: Calls `create_multipart_upload` to obtain a unique `UploadId` session token.
2. **Chunking & Upload**: Splits the large file into 5MB chunks and uploads each part independently via `upload_part`.
3. **Assemble & Complete**: Collects the ETags of all uploaded parts and calls `complete_multipart_upload` to instruct S3 to stitch the chunks back into a single object.
4. **Fault Tolerance**: If one part fails due to network glitch, only that single 5MB part needs to be re-sent, rather than restarting the entire multi-gigabyte upload from 0%.

---

## 📁 File Structure

* [`generate_sample_data.py`](file:///c:/code/aws-s3-and-lmbda-operations/aws-s3/examples/04_multipart_large_file_uploader/generate_sample_data.py): Generator creating a 6MB dummy binary dataset file (`large_dataset.bin`).
* [`run_example.py`](file:///c:/code/aws-s3-and-lmbda-operations/aws-s3/examples/04_multipart_large_file_uploader/run_example.py): Python Boto3 script executing the 3-step Multipart Upload sequence.

---

## 💻 How to Run on ANY Computer (Windows, macOS, Linux)

### Option A: Run via Python Runner Script (Recommended)
```bash
python run_example.py
```

---

### Option B: Run via AWS CLI (Step-by-Step)

#### Step 1: Generate Sample File & Create Bucket
```bash
python generate_sample_data.py
aws s3 mb s3://my-large-data-lake-2026 --endpoint-url http://localhost:4566
```

#### Step 2: Initiate Multipart Upload Session
```bash
aws s3api create-multipart-upload \
  --bucket my-large-data-lake-2026 \
  --key datasets/large_dataset.bin \
  --endpoint-url http://localhost:4566
```

#### Step 3: Upload Parts (5MB Chunks)
```bash
aws s3api upload-part \
  --bucket my-large-data-lake-2026 \
  --key datasets/large_dataset.bin \
  --part-number 1 \
  --upload-id <UPLOAD_ID_FROM_STEP_2> \
  --body large_dataset.bin \
  --endpoint-url http://localhost:4566
```

#### Step 4: Complete Multipart Upload
```bash
aws s3api complete-multipart-upload \
  --bucket my-large-data-lake-2026 \
  --key datasets/large_dataset.bin \
  --upload-id <UPLOAD_ID_FROM_STEP_2> \
  --multipart-upload '{"Parts": [{"ETag": "\"b10a8db164e0754105b7a99be72e3fe5\"", "PartNumber": 1}]}' \
  --endpoint-url http://localhost:4566
```

---

## ✏️ Changes You Should Make for Real AWS Cloud

1. **Bucket Name**: Replace `my-large-data-lake-2026` with your target bucket name.
2. **Chunk Size**: For multi-GB files, use 10MB to 100MB chunk sizes. S3 allows up to 10,000 parts per object.
3. **Remove Local Endpoint**: Omit `--endpoint-url http://localhost:4566` from CLI commands.

---

## 📤 Verified Output Details
```text
🚀 Initializing AWS S3 Client...
🪣 Creating Bucket 'my-large-data-lake-2026'...
🧩 Initiating Multipart Upload...
✅ Upload ID: MzQ1Njc4OTAxMjM0NTY3ODkwMT...
📤 Uploading Part 1 (5242880 bytes)... ETag: "a1b2c3d4..."
📤 Uploading Part 2 (1048576 bytes)... ETag: "e5f6g7h8..."
🏁 Completing Multipart Upload (2 parts total)...
🎉 Multipart Upload Completed Successfully!
```
