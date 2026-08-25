"""
Repository Integrity, Link Validator, Syntax & Security Audit Tool

Automated test suite to verify:
1. Python AST syntax across all .py files in repository.
2. Structural completeness (every operation has .py and README.md).
3. Markdown relative link integrity (verifies target path existence for all .md files).
4. Security check for hardcoded secrets or machine-specific absolute paths (C:\\Users, /home/).
"""

import ast
import re
import sys
import os
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent

S3_OPERATIONS = [
    ("aws-s3/basic_operations/01_create_bucket", "create_bucket.py"),
    ("aws-s3/basic_operations/02_upload_file", "upload_file.py"),
    ("aws-s3/basic_operations/03_list_buckets_and_objects", "list_buckets_and_objects.py"),
    ("aws-s3/basic_operations/04_download_file", "download_file.py"),
    ("aws-s3/basic_operations/05_delete_file", "delete_file.py"),
    ("aws-s3/basic_operations/06_delete_bucket", "delete_bucket.py"),
    ("aws-s3/intermediate_operations/07_copy_object", "copy_object.py"),
    ("aws-s3/intermediate_operations/08_move_object", "move_object.py"),
    ("aws-s3/intermediate_operations/09_create_folder", "create_folder.py"),
    ("aws-s3/intermediate_operations/10_object_metadata", "object_metadata.py"),
    ("aws-s3/intermediate_operations/11_object_acl", "object_acl.py"),
    ("aws-s3/intermediate_operations/12_presigned_url", "presigned_url.py"),
    ("aws-s3/intermediate_operations/13_bucket_versioning", "bucket_versioning.py"),
    ("aws-s3/intermediate_operations/14_bucket_encryption", "bucket_encryption.py"),
    ("aws-s3/advanced_operations/15_multipart_upload", "multipart_upload.py"),
    ("aws-s3/advanced_operations/16_pagination", "pagination.py"),
    ("aws-s3/advanced_operations/17_s3_select", "s3_select.py"),
    ("aws-s3/advanced_operations/18_lifecycle_configuration", "lifecycle_configuration.py"),
    ("aws-s3/advanced_operations/19_bucket_policy", "bucket_policy.py"),
]

LAMBDA_OPERATIONS = [
    ("aws-lambda/basic_operations/01_hello_world", "lambda_function.py"),
    ("aws-lambda/basic_operations/02_lambda_event", "lambda_function.py"),
    ("aws-lambda/basic_operations/03_lambda_context", "lambda_function.py"),
    ("aws-lambda/basic_operations/04_environment_variables", "lambda_function.py"),
    ("aws-lambda/basic_operations/05_error_handling", "lambda_function.py"),
    ("aws-lambda/s3_integration/06_s3_trigger", "lambda_function.py"),
    ("aws-lambda/s3_integration/07_s3_file_processing", "lambda_function.py"),
    ("aws-lambda/s3_integration/08_s3_event_processing", "lambda_function.py"),
    ("aws-lambda/advanced_operations/09_lambda_layers", "lambda_function.py"),
    ("aws-lambda/advanced_operations/10_lambda_permissions", "lambda_function.py"),
    ("aws-lambda/advanced_operations/11_lambda_logging", "lambda_function.py"),
    ("aws-lambda/advanced_operations/12_lambda_deployment", "deploy_script.py"),
]


def test_python_syntax():
    """Compiles all Python files into AST to ensure 0 syntax errors."""
    print("[TEST 1/4] Checking Python AST Syntax across repository...")
    py_files = list(REPO_ROOT.glob("**/*.py"))
    failed = []

    for py_file in py_files:
        if ".venv" in py_file.parts or "venv" in py_file.parts:
            continue
        try:
            with open(py_file, "r", encoding="utf-8") as f:
                ast.parse(f.read(), filename=str(py_file))
        except SyntaxError as e:
            print(f"  [FAIL] Syntax Error in '{py_file.relative_to(REPO_ROOT)}': {e}")
            failed.append(py_file)

    if not failed:
        print(f"  [PASS] All {len(py_files)} Python files parsed cleanly.")
    return len(failed) == 0


def test_directory_structure():
    """Verifies all 31 operations contain both script file and README.md."""
    print("\n[TEST 2/4] Verifying Operation Directories and Required Files...")
    all_ops = S3_OPERATIONS + LAMBDA_OPERATIONS
    missing = []

    for rel_dir, script_name in all_ops:
        op_dir = REPO_ROOT / rel_dir
        script_file = op_dir / script_name
        readme_file = op_dir / "README.md"

        if not op_dir.exists():
            print(f"  [MISSING DIR] {rel_dir}")
            missing.append(rel_dir)
            continue

        if not script_file.exists():
            print(f"  [MISSING SCRIPT] {rel_dir}/{script_name}")
            missing.append(f"{rel_dir}/{script_name}")

        if not readme_file.exists():
            print(f"  [MISSING README] {rel_dir}/README.md")
            missing.append(f"{rel_dir}/README.md")

    if not missing:
        print(f"  [PASS] All {len(all_ops)} operation folders contain script and README.md.")
    return len(missing) == 0


def test_markdown_links():
    """Parses relative markdown links in all .md files and checks target file existence."""
    print("\n[TEST 3/4] Validating Markdown Relative Links...")
    md_files = list(REPO_ROOT.glob("**/*.md"))
    link_pattern = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")
    broken_links = []

    for md_file in md_files:
        if ".venv" in md_file.parts or "venv" in md_file.parts:
            continue
        with open(md_file, "r", encoding="utf-8") as f:
            content = f.read()

        matches = link_pattern.findall(content)
        for text, link in matches:
            # Skip external web URLs, mailto links, or pure anchor targets (#heading)
            if link.startswith(("http://", "https://", "mailto:", "#")):
                continue

            # Strip anchor tags inside relative links (e.g. ./README.md#section)
            clean_link = link.split("#")[0]
            if not clean_link:
                continue

            target_path = (md_file.parent / clean_link).resolve()
            if not target_path.exists():
                print(f"  [BROKEN LINK] In '{md_file.relative_to(REPO_ROOT)}': [{text}]({link}) -> Target '{clean_link}' not found!")
                broken_links.append((md_file, link))

    if not broken_links:
        print(f"  [PASS] All relative Markdown links verified successfully across {len(md_files)} documentation files.")
    return len(broken_links) == 0


def test_security_and_portability():
    """Scans repository files for hardcoded AWS keys or absolute machine paths."""
    print("\n[TEST 4/4] Security & Portability Audit (Scanning for secrets / hardcoded user paths)...")
    forbidden_patterns = [
        (re.compile(r"AKIA[0-9A-Z]{16}"), "AWS Access Key ID"),
        (re.compile(r"C:\\Users\\[a-zA-Z0-9_\-\.]+"), "Windows absolute user path"),
        (re.compile(r"/home/[a-zA-Z0-9_\-\.]+"), "Linux absolute home path"),
        (re.compile(r"/Users/[a-zA-Z0-9_\-\.]+"), "macOS absolute user path")
    ]

    violations = []
    text_files = list(REPO_ROOT.glob("**/*.py")) + list(REPO_ROOT.glob("**/*.md"))

    for filepath in text_files:
        if ".venv" in filepath.parts or "venv" in filepath.parts or filepath.name == "validate_repo.py" or filepath.name == "implementation_plan.md":
            continue

        with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
            lines = f.readlines()

        for line_num, line in enumerate(lines, 1):
            for pattern, desc in forbidden_patterns:
                if pattern.search(line):
                    print(f"  [SECURITY RISK] {desc} found in '{filepath.relative_to(REPO_ROOT)}' at line {line_num}")
                    violations.append((filepath, line_num, desc))

    if not violations:
        print("  [PASS] Zero hardcoded secrets or non-portable absolute user paths detected.")
    return len(violations) == 0


if __name__ == "__main__":
    print("==========================================================")
    print("   AWS OPERATIONS REPOSITORY AUTOMATED INTEGRITY AUDITOR   ")
    print("==========================================================\n")

    t1 = test_python_syntax()
    t2 = test_directory_structure()
    t3 = test_markdown_links()
    t4 = test_security_and_portability()

    print("\n----------------------------------------------------------")
    if t1 and t2 and t3 and t4:
        print(" [SUCCESS] REPOSITORY AUDIT PASSED 100%! ALL CHECKS CLEAN.")
        print("----------------------------------------------------------")
        sys.exit(0)
    else:
        print(" [FAILURE] REPOSITORY AUDIT DETECTED ISSUES. SEE LOG ABOVE.")
        print("----------------------------------------------------------")
        sys.exit(1)
