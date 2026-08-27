import sys
import os
import time
from generate_retail_data import generate_retail_dataset
from generate_healthcare_data import generate_healthcare_dataset

def main():
    print("==================================================")
    print("     SYNTHETIC DATASET GENERATION PIPELINE        ")
    print("==================================================")
    
    total_start = time.time()
    
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    
    # 1. Retail
    retail_db = os.path.join(BASE_DIR, "retail.db")
    retail_csv_dir = os.path.join(BASE_DIR, "data", "csv", "retail")
    retail_json_dir = os.path.join(BASE_DIR, "data", "json", "retail")
    generate_retail_dataset(retail_db, retail_csv_dir, retail_json_dir)
    
    print()
    
    # 2. Healthcare
    healthcare_db = os.path.join(BASE_DIR, "healthcare.db")
    healthcare_csv_dir = os.path.join(BASE_DIR, "data", "csv", "healthcare")
    healthcare_json_dir = os.path.join(BASE_DIR, "data", "json", "healthcare")
    generate_healthcare_dataset(healthcare_db, healthcare_csv_dir, healthcare_json_dir)
    
    total_elapsed = round(time.time() - total_start, 2)
    print()
    print("==================================================")
    print(f" ALL DATASETS GENERATED SUCCESSFULLY IN {total_elapsed}s ")
    print("==================================================")

if __name__ == "__main__":
    main()
