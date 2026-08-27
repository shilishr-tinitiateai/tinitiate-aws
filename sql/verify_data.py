import sqlite3
import os

def verify_retail(db_path):
    print("--------------------------------------------------")
    print(" VERIFYING RETAIL DATABASE: retail.db ")
    print("--------------------------------------------------")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    tables = [
        "time_dimension", "customers", "customer_addresses", "locations",
        "products", "sales_transactions", "store_inventory", "warehouse_inventory"
    ]
    
    for tbl in tables:
        cursor.execute(f"SELECT COUNT(*) FROM {tbl}")
        count = cursor.fetchone()[0]
        print(f"  Table '{tbl:22s}': {count:>10,} rows")
        
    cursor.execute("SELECT MIN(full_date), MAX(full_date) FROM time_dimension")
    min_d, max_d = cursor.fetchone()
    print(f"\n  Retail Time Range: {min_d} to {max_d}")
    
    cursor.execute("SELECT SUM(total_amount), AVG(total_amount) FROM sales_transactions")
    total_rev, avg_order = cursor.fetchone()
    print(f"  Total Revenue: ${total_rev:,.2f}")
    print(f"  Average Order Total: ${avg_order:.2f}")
    
    conn.close()

def verify_healthcare(db_path):
    print("\n--------------------------------------------------")
    print(" VERIFYING HEALTHCARE DATABASE: healthcare.db ")
    print("--------------------------------------------------")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    tables = [
        "dim_patients", "dim_providers", "dim_facilities", "dim_diagnoses", "dim_medications",
        "fact_encounters", "fact_prescriptions", "fact_lab_results", "fact_billing_claims", "fact_medical_procedures"
    ]
    
    for tbl in tables:
        cursor.execute(f"SELECT COUNT(*) FROM {tbl}")
        count = cursor.fetchone()[0]
        print(f"  Table '{tbl:22s}': {count:>10,} rows")
        
    cursor.execute("SELECT SUM(total_charged_amount), SUM(insurance_covered_amount) FROM fact_billing_claims")
    total_charged, total_covered = cursor.fetchone()
    print(f"\n  Total Charges: ${total_charged:,.2f}")
    print(f"  Total Covered: ${total_covered:,.2f}")
    
    conn.close()

def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    retail_db = os.path.join(base_dir, "retail.db")
    healthcare_db = os.path.join(base_dir, "healthcare.db")
    
    if os.path.exists(retail_db):
        verify_retail(retail_db)
    else:
        print(f"Error: {retail_db} does not exist.")
        
    if os.path.exists(healthcare_db):
        verify_healthcare(healthcare_db)
    else:
        print(f"Error: {healthcare_db} does not exist.")

if __name__ == "__main__":
    main()
