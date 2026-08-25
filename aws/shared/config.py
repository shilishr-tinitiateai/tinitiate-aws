"""
Shared Configuration Helper for AWS Operations Repository.

Provides unified configuration loading from environment variables and .env files
with safe fallback defaults and cross-platform path resolution using pathlib.
"""

import os
from pathlib import Path

# Attempt to load .env file if python-dotenv is installed
try:
    from dotenv import load_dotenv
    # Resolve repository root path
    REPO_ROOT = Path(__file__).resolve().parent.parent
    env_path = REPO_ROOT / ".env"
    if env_path.exists():
        load_dotenv(dotenv_path=env_path)
except ImportError:
    pass

# Base Directory Resolution
REPO_ROOT = Path(__file__).resolve().parent.parent
EXAMPLES_DIR = REPO_ROOT / "examples"
DOWNLOADS_DIR = REPO_ROOT / "downloads"

# AWS Configuration Defaults
AWS_REGION = os.getenv("AWS_REGION", "us-east-1")
S3_BUCKET_NAME = os.getenv("S3_BUCKET_NAME", "my-learning-s3-bucket-unique-12345")
S3_OBJECT_KEY = os.getenv("S3_OBJECT_KEY", "sample.txt")
LOCAL_SAMPLE_FILE = EXAMPLES_DIR / "sample.txt"
LOCAL_SAMPLE_JSON = EXAMPLES_DIR / "sample.json"

LAMBDA_FUNCTION_NAME = os.getenv("LAMBDA_FUNCTION_NAME", "MySampleLambdaFunction")
LAMBDA_ROLE_ARN = os.getenv("LAMBDA_ROLE_ARN", "")

def get_downloads_dir() -> Path:
    """Ensure downloads directory exists and return its Path object."""
    DOWNLOADS_DIR.mkdir(parents=True, exist_ok=True)
    return DOWNLOADS_DIR
