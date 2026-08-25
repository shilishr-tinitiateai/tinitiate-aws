# Shared Module Overview

The `shared/` directory contains centralized Python helper utilities designed to promote DRY (Don't Repeat Yourself) architecture across all AWS S3 and Lambda operations.

---

## 1. Modules Included

### `config.py`
- Handles environment variable resolution.
- Resolves cross-platform absolute and relative filesystem paths using Python's `pathlib.Path`.
- Provides fallback defaults for bucket names, region codes, and sample file locations.
- Safe integration with `python-dotenv` if a `.env` file is present.

### `aws_client.py`
- Centralized Boto3 client/resource creation for `s3` and `lambda`.
- Enforces AWS Credential Provider Chain resolution (`aws configure`, IAM roles, environment variables).
- Intercepts missing/partial credential errors (`NoCredentialsError`, `PartialCredentialsError`) with actionable developer feedback.

---

## 2. Standard Usage in Operations

Operations throughout the repository import these helpers as follows:

```python
from shared.aws_client import get_s3_client
from shared.config import AWS_REGION, S3_BUCKET_NAME

# Initialize AWS client securely
s3_client = get_s3_client(region_name=AWS_REGION)
```
