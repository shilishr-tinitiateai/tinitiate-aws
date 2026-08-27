import sqlite3
import random
import datetime
import csv
import json
import os
import time

FIRST_NAMES = ["James", "Mary", "John", "Patricia", "Robert", "Jennifer", "Michael", "Linda", 
               "William", "Elizabeth", "David", "Barbara", "Richard", "Susan", "Joseph", "Jessica",
               "Thomas", "Sarah", "Charles", "Karen", "Christopher", "Nancy", "Daniel", "Lisa",
               "Matthew", "Betty", "Anthony", "Margaret", "Donald", "Sandra", "Mark", "Ashley"]

LAST_NAMES = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis",
              "Rodriguez", "Martinez", "Hernandez", "Lopez", "Gonzalez", "Wilson", "Anderson",
              "Thomas", "Taylor", "Moore", "Jackson", "Martin", "Lee", "Perez", "Thompson"]

CITIES_STATES = [
    ("New York", "NY", "10001"), ("Los Angeles", "CA", "90001"), ("Chicago", "IL", "60601"),
    ("Houston", "TX", "77001"), ("Phoenix", "AZ", "85001"), ("Philadelphia", "PA", "19101"),
    ("San Antonio", "TX", "78201"), ("San Diego", "CA", "92101"), ("Dallas", "TX", "75201"),
    ("San Jose", "CA", "95101"), ("Austin", "TX", "78701"), ("Jacksonville", "FL", "32201"),
    ("Seattle", "WA", "98101"), ("Denver", "CO", "80201"), ("Boston", "MA", "02101")
]

SPECIALTIES = [
    "Cardiology", "Pediatrics", "Oncology", "Neurology", "Orthopedics",
    "General Practice", "Internal Medicine", "Dermatology", "Gastroenterology",
    "Psychiatry", "Pulmonology", "Endocrinology", "Emergency Medicine", "Urology"
]

INSURANCE_PROVIDERS = [
    "Blue Cross Blue Shield", "UnitedHealth Group", "Aetna", "Cigna", 
    "Humana", "Kaiser Permanente", "Molina Healthcare", "Medicare", "Medicaid"
]

BLOOD_TYPES = ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"]

DIAGNOSIS_DATA = [
    ("I10", "Essential (primary) hypertension", "Cardiovascular", "Mild"),
    ("E11.9", "Type 2 diabetes mellitus without complications", "Endocrine", "Moderate"),
    ("J45.909", "Unspecified asthma, uncomplicated", "Respiratory", "Moderate"),
    ("M54.5", "Low back pain, unspecified", "Musculoskeletal", "Mild"),
    ("J06.9", "Acute upper respiratory infection, unspecified", "Respiratory", "Mild"),
    ("F41.1", "Generalized anxiety disorder", "Mental Health", "Moderate"),
    ("E78.5", "Hyperlipidemia, unspecified", "Endocrine", "Mild"),
    ("K21.9", "Gastro-esophageal reflux disease without esophagitis", "Gastrointestinal", "Mild"),
    ("N39.0", "Urinary tract infection, site not specified", "Urological", "Moderate"),
    ("I25.10", "Atherosclerotic heart disease of native coronary artery", "Cardiovascular", "Severe"),
    ("C34.90", "Malignant neoplasm of unspecified part of bronchus or lung", "Oncology", "Critical"),
    ("G40.909", "Epilepsy, unspecified, not intractable", "Neurology", "Severe"),
    ("M17.11", "Unspecified primary osteoarthritis, right knee", "Musculoskeletal", "Moderate"),
    ("R07.9", "Chest pain, unspecified", "Cardiovascular", "Severe"),
    ("J18.9", "Pneumonia, unspecified organism", "Respiratory", "Severe")
]

DRUG_DATA = [
    ("Amoxicillin", "Amoxicillin", "Capsule", "500mg", "Teva"),
    ("Lysinopril", "Lisinopril", "Tablet", "10mg", "Sandoz"),
    ("Metformin", "Metformin HCl", "Tablet", "850mg", "Mylan"),
    ("Atorvastatin", "Atorvastatin Calcium", "Tablet", "20mg", "Pfizer"),
    ("Albuterol", "Albuterol Sulfate", "Inhaler", "90mcg", "GSK"),
    ("Omeprazole", "Omeprazole", "Capsule", "20mg", "AstraZeneca"),
    ("Levothyroxine", "Levothyroxine Sodium", "Tablet", "50mcg", "AbbVie"),
    ("Gabapentin", "Gabapentin", "Capsule", "300mg", "Sun Pharma"),
    ("Amlodipine", "Amlodipine Besylate", "Tablet", "5mg", "Novartis"),
    ("Metoprolol", "Metoprolol Succinate", "Tablet", "50mg", "AstraZeneca"),
    ("Losartan", "Losartan Potassium", "Tablet", "50mg", "Merck"),
    ("Sertraline", "Sertraline HCl", "Tablet", "50mg", "Pfizer"),
    ("Hydrochlorothiazide", "Hydrochlorothiazide", "Tablet", "25mg", "Lupin"),
    ("Ibuprofen", "Ibuprofen", "Tablet", "800mg", "McNeil"),
    ("Azithromycin", "Azithromycin", "Tablet", "250mg", "Pfizer")
]

LAB_TESTS = [
    ("Complete Blood Count (CBC)", "White Blood Cells", "4.5-11.0", "10^3/uL"),
    ("Comprehensive Metabolic Panel", "Glucose", "70-99", "mg/dL"),
    ("Lipid Panel", "Total Cholesterol", "<200", "mg/dL"),
    ("HbA1c", "Hemoglobin A1c", "<5.7", "%"),
    ("Thyroid Panel", "TSH", "0.4-4.0", "mIU/L"),
    ("Urinalysis", "Protein", "Negative", "mg/dL"),
    ("Serum Creatinine", "Creatinine", "0.7-1.3", "mg/dL"),
    ("Liver Function Test", "ALT", "7-56", "U/L")
]

PROCEDURES = [
    ("99213", "Office or other outpatient visit, 15-29 minutes", 125.00),
    ("99214", "Office or other outpatient visit, 30-39 minutes", 185.00),
    ("99284", "Emergency department visit, high severity", 750.00),
    ("93000", "Electrocardiogram (EKG), routine with interpretation", 150.00),
    ("71045", "Chest X-ray, single view", 220.00),
    ("36415", "Routine venipuncture (blood draw)", 35.00),
    ("99232", "Subsequent hospital care, 25 minutes", 210.00),
    ("70450", "CT scan head/brain without contrast", 1200.00)
]

def generate_healthcare_dataset(db_path, csv_dir, json_dir=None):
    print("--- Generating Healthcare Dataset ---")
    start_time = time.time()
    
    os.makedirs(csv_dir, exist_ok=True)
    if json_dir is None:
        json_dir = os.path.join(os.path.dirname(csv_dir), "healthcare_json")
    os.makedirs(json_dir, exist_ok=True)

    if os.path.exists(db_path):
        os.remove(db_path)

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Load Schema
    base_dir = os.path.dirname(os.path.abspath(__file__))
    schema_path = os.path.join(base_dir, "healthcare_schema.sql")
    with open(schema_path, "r") as f:
        cursor.executescript(f.read())
        
    print("Healthcare Schema created successfully.")

    # 1. dim_patients (100,000 Patients)
    print("Generating 100,000 Patients (dim_patients)...")
    patient_rows = []
    start_date = datetime.date(2023, 8, 27)
    
    for pat_id in range(1, 100001):
        fname = random.choice(FIRST_NAMES)
        lname = random.choice(LAST_NAMES)
        dob = start_date - datetime.timedelta(days=random.randint(365, 29200)) # 1 to 80 yrs
        gender = random.choice(["Male", "Female"])
        btype = random.choice(BLOOD_TYPES)
        ssn = f"XXX-XX-{random.randint(1000, 9999)}"
        phone = f"{random.randint(200, 999)}-{random.randint(100, 999)}-{random.randint(1000, 9999)}"
        email = f"{fname.lower()}.{lname.lower()}{pat_id}@health-mail.org"
        city, state, zip_code = random.choice(CITIES_STATES)
        addr = f"{random.randint(100, 9999)} Medical Center Dr"
        ins_prov = random.choice(INSURANCE_PROVIDERS)
        ins_pol = f"POL-{random.randint(10000000, 99999999)}"
        
        patient_rows.append((pat_id, fname, lname, dob.isoformat(), gender, btype, ssn,
                             phone, email, addr, city, state, zip_code, ins_prov, ins_pol))
                             
    cursor.executemany("INSERT INTO dim_patients VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", patient_rows)
    conn.commit()
    print("Patients inserted.")

    # 2. dim_providers (5,000 Doctors / Providers)
    print("Generating 5,000 Healthcare Providers (dim_providers)...")
    provider_rows = []
    for prov_id in range(1, 5001):
        fname = random.choice(FIRST_NAMES)
        lname = random.choice(LAST_NAMES)
        npi = f"1{prov_id:09d}"
        spec = random.choice(SPECIALTIES)
        lic_state = random.choice(CITIES_STATES)[1]
        phone = f"{random.randint(200, 999)}-555-{random.randint(1000, 9999)}"
        provider_rows.append((prov_id, fname, lname, npi, spec, lic_state, phone))
        
    cursor.executemany("INSERT INTO dim_providers VALUES (?,?,?,?,?,?,?)", provider_rows)
    conn.commit()
    print("Providers inserted.")

    # 3. dim_facilities (500 Hospitals / Clinics)
    print("Generating 500 Facilities (dim_facilities)...")
    facility_rows = []
    types = ["General Hospital", "Urgent Care", "Specialty Clinic", "Diagnostic Center"]
    for fac_id in range(1, 501):
        city, state, zip_code = random.choice(CITIES_STATES)
        ftype = random.choice(types)
        name = f"{city} {ftype} #{fac_id}"
        addr = f"{random.randint(100, 9999)} Health Parkway"
        beds = random.randint(10, 800)
        facility_rows.append((fac_id, name, ftype, addr, city, state, zip_code, beds))
        
    cursor.executemany("INSERT INTO dim_facilities VALUES (?,?,?,?,?,?,?,?)", facility_rows)
    conn.commit()
    print("Facilities inserted.")

    # 4. dim_diagnoses (2,000 ICD-10 codes)
    print("Generating 2,000 Diagnoses (dim_diagnoses)...")
    diag_rows = []
    for diag_id in range(1, 2001):
        if diag_id <= len(DIAGNOSIS_DATA):
            code, desc, cat, sev = DIAGNOSIS_DATA[diag_id - 1]
        else:
            base_code, base_desc, cat, sev = random.choice(DIAGNOSIS_DATA)
            code = f"{base_code}.{diag_id}"
            desc = f"{base_desc} (Variant #{diag_id})"
            
        diag_rows.append((diag_id, code, desc, cat, sev))
        
    cursor.executemany("INSERT INTO dim_diagnoses VALUES (?,?,?,?,?)", diag_rows)
    conn.commit()
    print("Diagnoses inserted.")

    # 5. dim_medications (3,000 Drug NDC records)
    print("Generating 3,000 Medications (dim_medications)...")
    med_rows = []
    for med_id in range(1, 3001):
        ndc = f"{random.randint(10000, 99999):05d}-{random.randint(100, 999):03d}-{med_id % 100:02d}"
        if med_id <= len(DRUG_DATA):
            dname, gname, form, strg, mfr = DRUG_DATA[med_id - 1]
        else:
            dname, gname, form, strg, mfr = random.choice(DRUG_DATA)
            dname = f"{dname} Plus"
            
        med_rows.append((med_id, ndc, dname, gname, form, strg, mfr))
        
    cursor.executemany("INSERT INTO dim_medications VALUES (?,?,?,?,?,?,?)", med_rows)
    conn.commit()
    print("Medications inserted.")

    # 6. fact_encounters (100,000 Encounters)
    print("Generating 100,000 Patient Encounters (fact_encounters)...")
    enc_rows = []
    enc_types = ["Inpatient", "Outpatient", "Emergency", "Telehealth"]
    statuses = ["Completed", "Completed", "Completed", "In-Progress", "Cancelled"]
    
    for enc_id in range(1, 100001):
        pat_id = random.randint(1, 100000)
        prov_id = random.randint(1, 5000)
        fac_id = random.randint(1, 500)
        diag_id = random.randint(1, 2000)
        etype = random.choice(enc_types)
        
        days_ago = random.randint(0, 1095)
        adm_dt = start_date - datetime.timedelta(days=days_ago, hours=random.randint(0, 23))
        
        if etype == "Inpatient":
            dis_dt = adm_dt + datetime.timedelta(days=random.randint(1, 14))
        else:
            dis_dt = adm_dt + datetime.timedelta(hours=random.randint(1, 4))
            
        status = random.choice(statuses)
        dis_str = dis_dt.isoformat() if status == "Completed" else None
        
        enc_rows.append((enc_id, pat_id, prov_id, fac_id, diag_id, etype, adm_dt.isoformat(), dis_str, status))
        
    cursor.executemany("INSERT INTO fact_encounters VALUES (?,?,?,?,?,?,?,?,?)", enc_rows)
    conn.commit()
    print("Encounters inserted.")

    # 7. fact_prescriptions (100,000 Prescriptions)
    print("Generating 100,000 Prescriptions (fact_prescriptions)...")
    rx_rows = []
    instructions = ["1 tablet daily with food", "2 capsules twice daily", "1 spray as needed", "1 tablet every 12 hours"]
    
    for rx_id in range(1, 100001):
        enc_id = random.randint(1, 100000)
        pat_id = random.randint(1, 100000)
        prov_id = random.randint(1, 5000)
        med_id = random.randint(1, 3000)
        
        rx_date = start_date - datetime.timedelta(days=random.randint(0, 1095))
        inst = random.choice(instructions)
        refills = random.choice([0, 1, 2, 3, 5, 11])
        qty = random.choice([30, 60, 90, 100])
        
        rx_rows.append((rx_id, enc_id, pat_id, prov_id, med_id, rx_date.isoformat(), inst, refills, qty))
        
    cursor.executemany("INSERT INTO fact_prescriptions VALUES (?,?,?,?,?,?,?,?,?)", rx_rows)
    conn.commit()
    print("Prescriptions inserted.")

    # 8. fact_lab_results (100,000 Lab Results)
    print("Generating 100,000 Lab Results (fact_lab_results)...")
    lab_rows = []
    flags = ["Normal", "Normal", "Normal", "High", "Low", "Critical"]
    
    for lab_id in range(1, 100001):
        enc_id = random.randint(1, 100000)
        pat_id = random.randint(1, 100000)
        
        tname, field, ref, unit = random.choice(LAB_TESTS)
        val = str(round(random.uniform(3.0, 140.0), 1))
        flag = random.choice(flags)
        
        test_dt = start_date - datetime.timedelta(days=random.randint(0, 1095), hours=random.randint(0, 23))
        lab_rows.append((lab_id, enc_id, pat_id, tname, test_dt.isoformat(), val, unit, ref, flag))
        
    cursor.executemany("INSERT INTO fact_lab_results VALUES (?,?,?,?,?,?,?,?,?)", lab_rows)
    conn.commit()
    print("Lab Results inserted.")

    # 9. fact_billing_claims (100,000 Claims)
    print("Generating 100,000 Billing Claims (fact_billing_claims)...")
    claim_rows = []
    statuses = ["Paid", "Paid", "Approved", "Submitted", "Denied"]
    
    for claim_id in range(1, 100001):
        enc_id = random.randint(1, 100000)
        pat_id = random.randint(1, 100000)
        cdate = start_date - datetime.timedelta(days=random.randint(0, 1095))
        
        charged = round(random.uniform(150.0, 15000.0), 2)
        copay = round(random.uniform(15.0, 250.0), 2)
        covered = round(charged - copay, 2)
        cstatus = random.choice(statuses)
        
        claim_rows.append((claim_id, enc_id, pat_id, cdate.isoformat(), charged, covered, copay, cstatus))
        
    cursor.executemany("INSERT INTO fact_billing_claims VALUES (?,?,?,?,?,?,?,?)", claim_rows)
    conn.commit()
    print("Billing Claims inserted.")

    # 10. fact_medical_procedures (100,000 Procedures)
    print("Generating 100,000 Medical Procedures (fact_medical_procedures)...")
    proc_rows = []
    
    for proc_id in range(1, 100001):
        enc_id = random.randint(1, 100000)
        pat_id = random.randint(1, 100000)
        cpt, desc, cost = random.choice(PROCEDURES)
        cost_adj = round(cost * random.uniform(0.9, 1.25), 2)
        pdate = start_date - datetime.timedelta(days=random.randint(0, 1095))
        
        proc_rows.append((proc_id, enc_id, pat_id, cpt, desc, pdate.isoformat(), cost_adj))
        
    cursor.executemany("INSERT INTO fact_medical_procedures VALUES (?,?,?,?,?,?,?)", proc_rows)
    conn.commit()
    print("Procedures inserted.")

    tables = [
        "dim_patients", "dim_providers", "dim_facilities", "dim_diagnoses", "dim_medications",
        "fact_encounters", "fact_prescriptions", "fact_lab_results", "fact_billing_claims", "fact_medical_procedures"
    ]

    # Export to CSVs
    print("Exporting Healthcare tables to CSV files...")
    for tbl in tables:
        csv_file = os.path.join(csv_dir, f"{tbl}.csv")
        cursor.execute(f"SELECT * FROM {tbl}")
        col_names = [desc[0] for desc in cursor.description]
        
        with open(csv_file, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(col_names)
            while True:
                rows = cursor.fetchmany(50000)
                if not rows:
                    break
                writer.writerows(rows)
        print(f"   Exported {tbl}.csv")

    # Export to JSONs
    print("Exporting Healthcare tables to JSON files...")
    for tbl in tables:
        json_file = os.path.join(json_dir, f"{tbl}.json")
        cursor.execute(f"SELECT * FROM {tbl}")
        col_names = [desc[0] for desc in cursor.description]
        
        with open(json_file, "w", encoding="utf-8") as f:
            f.write("[\n")
            first = True
            while True:
                rows = cursor.fetchmany(10000)
                if not rows:
                    break
                for row in rows:
                    if not first:
                        f.write(",\n")
                    row_dict = dict(zip(col_names, row))
                    f.write("  " + json.dumps(row_dict))
                    first = False
            f.write("\n]")
        print(f"   Exported {tbl}.json")

    conn.close()
    elapsed = round(time.time() - start_time, 2)
    print(f"--- Healthcare Dataset Completed in {elapsed} seconds ---")

if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.abspath(__file__))
    db_file = os.path.join(base_dir, "healthcare.db")
    csv_folder = os.path.join(base_dir, "data", "healthcare_csv")
    json_folder = os.path.join(base_dir, "data", "healthcare_json")
    generate_healthcare_dataset(db_file, csv_folder, json_folder)

