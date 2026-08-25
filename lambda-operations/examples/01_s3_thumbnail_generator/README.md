# 🖼️ Example 1: Automated S3 Image & File Thumbnail Processor

Welcome to **Example 1**! This beginner-friendly guide demonstrates how AWS Lambda automatically runs when files are uploaded to an **Amazon S3 Bucket**.

---

## 🎯 What Does This Example Do?

1. A user uploads an image (e.g. `avatars/user_profile_photo.jpg`) to an S3 bucket named `my-user-uploads-bucket`.
2. Amazon S3 automatically generates an **S3 Event Notification JSON payload** and triggers this Lambda function.
3. The Lambda function reads the file name, bucket name, and file size, logs the details, and returns a processed thumbnail key (`thumbnails/thumb_user_profile_photo.jpg`).

---

## 📁 File Structure

* [`lambda_function.py`](file:///c:/code/aws-s3-and-lmbda-operations/lambda-operations/examples/01_s3_thumbnail_generator/lambda_function.py): Python Lambda function handler.
* [`sample_s3_event.json`](file:///c:/code/aws-s3-and-lmbda-operations/lambda-operations/examples/01_s3_thumbnail_generator/sample_s3_event.json): Realistic mock S3 upload event payload.
* [`run_example.py`](file:///c:/code/aws-s3-and-lmbda-operations/lambda-operations/examples/01_s3_thumbnail_generator/run_example.py): Automated Boto3 runner that packages, deploys, invokes, and prints results.

---

## 💻 How to Run on ANY Computer (Windows, macOS, Linux)

### Option A: Run via Python Runner Script (Recommended)
From this directory, execute:

```bash
python run_example.py
```

---

### Option B: Run via AWS CLI (Step-by-Step)

#### Step 1: Zip the Lambda function
```bash
# Windows PowerShell
Compress-Archive -Path lambda_function.py -DestinationPath s3_func.zip -Force

# Linux / macOS Bash
zip s3_func.zip lambda_function.py
```

#### Step 2: Create the Lambda function
```bash
aws lambda create-function \
  --function-name s3-thumbnail-generator-example \
  --runtime python3.12 \
  --role arn:aws:iam::123456789012:role/lambda-role \
  --handler lambda_function.lambda_handler \
  --zip-file fileb://s3_func.zip \
  --endpoint-url http://localhost:4566
```

#### Step 3: Invoke the function with sample S3 event
```bash
# Windows PowerShell
aws lambda invoke `
  --function-name s3-thumbnail-generator-example `
  --payload file://sample_s3_event.json `
  --cli-binary-format raw-in-base64-out `
  output.json `
  --endpoint-url http://localhost:4566

# Linux / macOS Bash
aws lambda invoke \
  --function-name s3-thumbnail-generator-example \
  --payload file://sample_s3_event.json \
  --cli-binary-format raw-in-base64-out \
  output.json \
  --endpoint-url http://localhost:4566
```

---

## ✏️ Changes You Should Make for Real AWS Cloud

1. **Remove Local Endpoint**: Omit `--endpoint-url http://localhost:4566` from CLI commands.
2. **Update Role ARN**: Replace `arn:aws:iam::123456789012:role/lambda-role` with your actual IAM role ARN.
3. **Connect S3 Bucket Event**: In AWS Console / CLI, configure S3 Event Notification to trigger this Lambda function whenever `s3:ObjectCreated:*` occurs.

---

## 📥 Sample Input Event (`sample_s3_event.json`)
```json
{
  "Records": [
    {
      "eventSource": "aws:s3",
      "s3": {
        "bucket": { "name": "my-user-uploads-bucket" },
        "object": { "key": "avatars/user_profile_photo.jpg", "size": 1048576 }
      }
    }
  ]
}
```

---

## 📤 Sample Response Output (`output.json`)
```json
{
  "statusCode": 200,
  "headers": {
    "Content-Type": "application/json"
  },
  "body": {
    "message": "S3 File Event Processed Successfully!",
    "total_files_processed": 1,
    "files": [
      {
        "bucket": "my-user-uploads-bucket",
        "original_key": "avatars/user_profile_photo.jpg",
        "thumbnail_key": "thumbnails/thumb_user_profile_photo.jpg",
        "file_size_bytes": 1048576,
        "status": "THUMBNAIL_CREATED"
      }
    ]
  }
}
```
