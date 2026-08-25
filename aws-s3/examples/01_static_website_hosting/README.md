# 🌐 Example 1: Hosting a Static Website on AWS S3

Welcome to **Example 1**! This beginner-friendly guide demonstrates how to host a static website (HTML, CSS, JavaScript) directly on an **Amazon S3 Bucket**.

---

## 🎯 What Does This Example Do?

1. Creates an S3 bucket named `my-static-website-example-2026`.
2. Configures the S3 bucket's **Website Hosting Configuration** pointing to `index.html` (Index Document) and `error.html` (Error 404 Document).
3. Uploads HTML files with the correct MIME Header (`Content-Type: text/html`) so browsers render the page instead of downloading it.
4. Outputs the public HTTP Web URL.

---

## 📁 File Structure

* [`index.html`](file:///c:/code/aws-s3-and-lmbda-operations/aws-s3/examples/01_static_website_hosting/index.html): Main website landing page HTML.
* [`error.html`](file:///c:/code/aws-s3-and-lmbda-operations/aws-s3/examples/01_static_website_hosting/error.html): Custom 404 error page.
* [`run_example.py`](file:///c:/code/aws-s3-and-lmbda-operations/aws-s3/examples/01_static_website_hosting/run_example.py): Python Boto3 script that automates bucket creation, website configuration, and uploading.

---

## 💻 How to Run on ANY Computer (Windows, macOS, Linux)

### Option A: Run via Python Runner Script (Recommended)
```bash
python run_example.py
```

---

### Option B: Run via AWS CLI (Step-by-Step)

#### Step 1: Create the S3 Bucket
```bash
aws s3 mb s3://my-static-website-example-2026 --endpoint-url http://localhost:4566
```

#### Step 2: Configure Bucket Website Hosting
```bash
aws s3 website s3://my-static-website-example-2026/ \
  --index-document index.html \
  --error-document error.html \
  --endpoint-url http://localhost:4566
```

#### Step 3: Upload Website Files with Content-Type Header
```bash
aws s3 cp index.html s3://my-static-website-example-2026/index.html \
  --content-type "text/html" \
  --endpoint-url http://localhost:4566

aws s3 cp error.html s3://my-static-website-example-2026/error.html \
  --content-type "text/html" \
  --endpoint-url http://localhost:4566
```

---

## ✏️ Changes You Should Make for Real AWS Cloud

1. **Bucket Name Uniqueness**: Bucket names must be globally unique across all AWS accounts worldwide. Change `my-static-website-example-2026` to `my-company-website-unique-1234`.
2. **Remove Local Endpoint**: Omit `--endpoint-url http://localhost:4566` from CLI commands.
3. **Disable Block Public Access**: In real AWS Console/CLI, disable S3 "Block Public Access" settings and apply a Public Read Bucket Policy:
   ```json
   {
     "Version": "2012-10-17",
     "Statement": [
       {
         "Sid": "PublicReadGetObject",
         "Effect": "Allow",
         "Principal": "*",
         "Action": "s3:GetObject",
         "Resource": "arn:aws:s3:::my-static-website-example-2026/*"
       }
     ]
   }
   ```

---

## 📤 Output Details
* **Real AWS Cloud URL**: `http://my-static-website-example-2026.s3-website-us-east-1.amazonaws.com`
* **Local Emulator URL**: `http://localhost:4566/my-static-website-example-2026/index.html`
