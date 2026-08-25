# 🔒 Example 2: Secure Encrypted Private Database Backup

Welcome to **Example 2**! This beginner-friendly guide demonstrates how to upload database dumps and log files to a **Private S3 Bucket** enforcing **AES256 Server-Side Encryption (SSE-S3)** and compliance metadata tags.

---

## 🎯 What Does This Example Do?

1. Creates a private S3 bucket named `my-company-private-backups-2026`.
2. Uploads a database dump (`sample_database_backup.sql`) to `database_backups/2026/backup_prod_db.sql`.
3. Automatically encrypts the object at rest using **AES-256 Server-Side Encryption**.
4. Attaches compliance resource tags (`Environment=Production`, `Retention=30Days`) and custom metadata (`backup_type=full_database_dump`).
5. Verifies encryption status using `head_object`.

---

## 📁 File Structure

* [`sample_database_backup.sql`](file:///c:/code/aws-s3-and-lmbda-operations/aws-s3/examples/02_secure_private_backup/sample_database_backup.sql): Sample database SQL dump file.
* [`run_example.py`](file:///c:/code/aws-s3-and-lmbda-operations/aws-s3/examples/02_secure_private_backup/run_example.py): Python Boto3 script enforcing encryption and metadata tags.

---

## 💻 How to Run on ANY Computer (Windows, macOS, Linux)

### Option A: Run via Python Runner Script (Recommended)
```bash
python run_example.py
```

---

### Option B: Run via AWS CLI (Step-by-Step)

#### Step 1: Create Private Bucket
```bash
aws s3 mb s3://my-company-private-backups-2026 --endpoint-url http://localhost:4566
```

#### Step 2: Upload File with AES256 Encryption & Metadata Tags
```bash
aws s3 cp sample_database_backup.sql s3://my-company-private-backups-2026/database_backups/2026/backup_prod_db.sql \
  --sse AES256 \
  --metadata "backup_type=full_database_dump,database_engine=PostgreSQL" \
  --endpoint-url http://localhost:4566
```

#### Step 3: Verify Encryption Metadata
```bash
aws s3api head-object \
  --bucket my-company-private-backups-2026 \
  --key database_backups/2026/backup_prod_db.sql \
  --endpoint-url http://localhost:4566
```

---

## ✏️ Changes You Should Make for Real AWS Cloud

1. **Bucket Name**: Change `my-company-private-backups-2026` to your unique private bucket name.
2. **KMS Key Encryption (Optional)**: For enterprise KMS encryption, replace `--sse AES256` with `--sse aws:kms --sse-kms-key-id arn:aws:kms:us-east-1:123456789012:key/your-key-uuid`.
3. **Remove Local Endpoint**: Omit `--endpoint-url http://localhost:4566` from CLI commands.

---

## 📤 Verified Output Summary
* **Server-Side Encryption**: `AES256`
* **Custom Metadata**: `{ "backup_type": "full_database_dump", "database_engine": "PostgreSQL" }`
* **Object Access**: Private (Restricted to authenticated IAM users).
