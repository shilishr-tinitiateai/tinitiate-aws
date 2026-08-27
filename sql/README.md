# Synthetic Data Generation Suite for Retail & Healthcare Domains

High-performance, portable synthetic data generator suite providing production-ready ANSI SQL DDL schemas, Python generator scripts, single-file SQLite databases (`retail.db`, `healthcare.db`), formatted **CSV exports**, and **JSON file exports**.

---

## 📋 Project Summary

| Domain | Total Entities | Target Scale | Formats Generated |
| :--- | :--- | :--- | :--- |
| **Retail Enterprise** | 8 Tables (Master, Fact, Dim) | **1,000,000** Sales Transactions, **100,000** Customers, **10,000** Products, **1,300** Stores | SQLite DB, CSV Files, JSON Files, SQL DDL |
| **Healthcare Provider** | 10 Tables (5 Dim + 5 Fact/Master) | **100,000** Patients, **100,000** Encounters, Claims, Prescriptions, Labs & Procedures | SQLite DB, CSV Files, JSON Files, SQL DDL |

---

## 📁 Repository Structure

```
.
├── retail_schema.sql           # DDL schema definition for Retail domain
├── healthcare_schema.sql       # DDL schema definition for Healthcare domain
├── generate_retail_data.py     # Fast generator script for Retail dataset
├── generate_healthcare_data.py # Fast generator script for Healthcare dataset
├── build_all_data.py           # Master pipeline script to build all DBs, CSVs & JSONs
├── verify_data.py              # Verification audit script checking row counts & metrics
├── retail.db                   # SQLite database for Retail domain
├── healthcare.db               # SQLite database for Healthcare domain
└── data/
    ├── csv/
    │   ├── retail/             # CSV exports for Retail (8 tables)
    │   └── healthcare/         # CSV exports for Healthcare (10 tables)
    └── json/
        ├── retail/             # JSON exports for Retail (8 tables)
        │   ├── time_dimension.json
        │   ├── customers.json
        │   ├── customer_addresses.json
        │   ├── locations.json
        │   ├── products.json
        │   ├── sales_transactions.json
        │   ├── store_inventory.json
        │   └── warehouse_inventory.json
        └── healthcare/         # JSON exports for Healthcare (10 tables)
            ├── dim_patients.json
            ├── dim_providers.json
            ├── dim_facilities.json
            ├── dim_diagnoses.json
            ├── dim_medications.json
            ├── fact_encounters.json
            ├── fact_prescriptions.json
            ├── fact_lab_results.json
            ├── fact_billing_claims.json
            └── fact_medical_procedures.json
```

---

## 🚀 Quick Start & Execution

The scripts use **portable script-relative paths**, so you can download or place this repository in any folder on Windows, macOS, or Linux without editing any file paths.

### 1. Prerequisites
- **Python 3.8+** (Uses standard Python standard library: `sqlite3`, `json`, `csv`, `random`, `datetime`, `os`, `time`). No external `pip` dependencies required!

### 2. Generate All Formats (DB, CSV, JSON)
Run the master orchestrator script:

```bash
python build_all_data.py
```

### 3. Verify Datasets
Run the audit script to check row counts and validation metrics:

```bash
python verify_data.py
```

---

## 🛍️ 1. Retail Domain Schema & Specs

### Date Range
3 Years: **2023-08-27 to 2026-08-27** (1,097 days).

### Tables & Record Specifications

1. **`time_dimension`** (1,097 rows) -> `time_dimension.json` & `.csv`
2. **`customers`** (100,000 rows) -> `customers.json` & `.csv`
3. **`customer_addresses`** (100,000 rows) -> `customer_addresses.json` & `.csv`
4. **`locations`** (1,300 rows) -> `locations.json` & `.csv`
5. **`products`** (10,000 rows) -> `products.json` & `.csv`
6. **`sales_transactions`** (1,000,000 rows) -> `sales_transactions.json` & `.csv`
7. **`store_inventory`** (100,000 rows) -> `store_inventory.json` & `.csv`
8. **`warehouse_inventory`** (100,000 rows) -> `warehouse_inventory.json` & `.csv`

---

## 🏥 2. Healthcare Domain Schema & Specs

### Dimension Tables (JSON & CSV)
1. **`dim_patients`** (100,000 rows) -> `dim_patients.json` & `.csv`
2. **`dim_providers`** (5,000 rows) -> `dim_providers.json` & `.csv`
3. **`dim_facilities`** (500 rows) -> `dim_facilities.json` & `.csv`
4. **`dim_diagnoses`** (2,000 rows) -> `dim_diagnoses.json` & `.csv`
5. **`dim_medications`** (3,000 rows) -> `dim_medications.json` & `.csv`

### Master / Fact Tables (JSON & CSV)
6. **`fact_encounters`** (100,000 rows) -> `fact_encounters.json` & `.csv`
7. **`fact_prescriptions`** (100,000 rows) -> `fact_prescriptions.json` & `.csv`
8. **`fact_lab_results`** (100,000 rows) -> `fact_lab_results.json` & `.csv`
9. **`fact_billing_claims`** (100,000 rows) -> `fact_billing_claims.json` & `.csv`
10. **`fact_medical_procedures`** (100,000 rows) -> `fact_medical_procedures.json` & `.csv`
