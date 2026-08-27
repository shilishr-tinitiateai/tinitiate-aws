-- Healthcare Database Schema DDL
-- Compatible with SQLite, PostgreSQL, MySQL, DuckDB, Snowflake, BigQuery

-- ==========================================
-- DIMENSION TABLES (5 Tables)
-- ==========================================

CREATE TABLE IF NOT EXISTS dim_patients (
    patient_id INTEGER PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    dob DATE NOT NULL,
    gender VARCHAR(10) NOT NULL,
    blood_type VARCHAR(5) NOT NULL,
    ssn_masked VARCHAR(11) NOT NULL,
    phone VARCHAR(20),
    email VARCHAR(100),
    address VARCHAR(150),
    city VARCHAR(50),
    state VARCHAR(50),
    zip_code VARCHAR(20),
    insurance_provider VARCHAR(50) NOT NULL,
    insurance_policy_num VARCHAR(30) NOT NULL
);

CREATE TABLE IF NOT EXISTS dim_providers (
    provider_id INTEGER PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    npi_number VARCHAR(10) UNIQUE NOT NULL,
    specialty VARCHAR(50) NOT NULL,
    license_state VARCHAR(2) NOT NULL,
    phone VARCHAR(20)
);

CREATE TABLE IF NOT EXISTS dim_facilities (
    facility_id INTEGER PRIMARY KEY,
    facility_name VARCHAR(100) NOT NULL,
    facility_type VARCHAR(30) NOT NULL, -- Hospital, Clinic, Urgent Care, Diagnostic Center
    address VARCHAR(150) NOT NULL,
    city VARCHAR(50) NOT NULL,
    state VARCHAR(50) NOT NULL,
    zip_code VARCHAR(20) NOT NULL,
    bed_capacity INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS dim_diagnoses (
    diagnosis_id INTEGER PRIMARY KEY,
    icd10_code VARCHAR(10) UNIQUE NOT NULL,
    icd10_description VARCHAR(200) NOT NULL,
    category VARCHAR(50) NOT NULL,
    severity_level VARCHAR(20) NOT NULL -- Mild, Moderate, Severe, Critical
);

CREATE TABLE IF NOT EXISTS dim_medications (
    medication_id INTEGER PRIMARY KEY,
    ndc_code VARCHAR(12) UNIQUE NOT NULL,
    drug_name VARCHAR(100) NOT NULL,
    generic_name VARCHAR(100) NOT NULL,
    dosage_form VARCHAR(30) NOT NULL,   -- Tablet, Capsule, Injection, Liquid
    strength VARCHAR(20) NOT NULL,
    manufacturer VARCHAR(50) NOT NULL
);

-- ==========================================
-- MASTER / FACT TABLES (5 Tables)
-- ==========================================

CREATE TABLE IF NOT EXISTS fact_encounters (
    encounter_id INTEGER PRIMARY KEY,
    patient_id INTEGER NOT NULL,
    provider_id INTEGER NOT NULL,
    facility_id INTEGER NOT NULL,
    primary_diagnosis_id INTEGER NOT NULL,
    encounter_type VARCHAR(20) NOT NULL, -- Inpatient, Outpatient, Emergency, Telehealth
    admission_date TIMESTAMP NOT NULL,
    discharge_date TIMESTAMP,
    encounter_status VARCHAR(20) NOT NULL, -- Completed, Cancelled, In-Progress
    FOREIGN KEY (patient_id) REFERENCES dim_patients(patient_id),
    FOREIGN KEY (provider_id) REFERENCES dim_providers(provider_id),
    FOREIGN KEY (facility_id) REFERENCES dim_facilities(facility_id),
    FOREIGN KEY (primary_diagnosis_id) REFERENCES dim_diagnoses(diagnosis_id)
);

CREATE TABLE IF NOT EXISTS fact_prescriptions (
    prescription_id INTEGER PRIMARY KEY,
    encounter_id INTEGER NOT NULL,
    patient_id INTEGER NOT NULL,
    provider_id INTEGER NOT NULL,
    medication_id INTEGER NOT NULL,
    prescribed_date DATE NOT NULL,
    dosage_instructions VARCHAR(150) NOT NULL,
    refills_allowed INTEGER NOT NULL DEFAULT 0,
    quantity_dispensed INTEGER NOT NULL,
    FOREIGN KEY (encounter_id) REFERENCES fact_encounters(encounter_id),
    FOREIGN KEY (patient_id) REFERENCES dim_patients(patient_id),
    FOREIGN KEY (provider_id) REFERENCES dim_providers(provider_id),
    FOREIGN KEY (medication_id) REFERENCES dim_medications(medication_id)
);

CREATE TABLE IF NOT EXISTS fact_lab_results (
    lab_result_id INTEGER PRIMARY KEY,
    encounter_id INTEGER NOT NULL,
    patient_id INTEGER NOT NULL,
    test_name VARCHAR(100) NOT NULL,
    test_date TIMESTAMP NOT NULL,
    result_value VARCHAR(50) NOT NULL,
    unit_of_measure VARCHAR(20),
    reference_range VARCHAR(30),
    abnormal_flag VARCHAR(10) NOT NULL, -- Normal, High, Low, Critical
    FOREIGN KEY (encounter_id) REFERENCES fact_encounters(encounter_id),
    FOREIGN KEY (patient_id) REFERENCES dim_patients(patient_id)
);

CREATE TABLE IF NOT EXISTS fact_billing_claims (
    claim_id INTEGER PRIMARY KEY,
    encounter_id INTEGER NOT NULL,
    patient_id INTEGER NOT NULL,
    claim_date DATE NOT NULL,
    total_charged_amount DECIMAL(10, 2) NOT NULL,
    insurance_covered_amount DECIMAL(10, 2) NOT NULL,
    patient_copay_amount DECIMAL(10, 2) NOT NULL,
    claim_status VARCHAR(20) NOT NULL, -- Submitted, Approved, Pending, Denied, Paid
    FOREIGN KEY (encounter_id) REFERENCES fact_encounters(encounter_id),
    FOREIGN KEY (patient_id) REFERENCES dim_patients(patient_id)
);

CREATE TABLE IF NOT EXISTS fact_medical_procedures (
    procedure_id INTEGER PRIMARY KEY,
    encounter_id INTEGER NOT NULL,
    patient_id INTEGER NOT NULL,
    cpt_code VARCHAR(10) NOT NULL,
    procedure_description VARCHAR(200) NOT NULL,
    procedure_date DATE NOT NULL,
    procedure_cost DECIMAL(10, 2) NOT NULL,
    FOREIGN KEY (encounter_id) REFERENCES fact_encounters(encounter_id),
    FOREIGN KEY (patient_id) REFERENCES dim_patients(patient_id)
);

-- Indexes for analytical performance
CREATE INDEX IF NOT EXISTS idx_enc_patient ON fact_encounters(patient_id);
CREATE INDEX IF NOT EXISTS idx_enc_provider ON fact_encounters(provider_id);
CREATE INDEX IF NOT EXISTS idx_rx_patient ON fact_prescriptions(patient_id);
CREATE INDEX IF NOT EXISTS idx_lab_patient ON fact_lab_results(patient_id);
CREATE INDEX IF NOT EXISTS idx_claim_patient ON fact_billing_claims(patient_id);
CREATE INDEX IF NOT EXISTS idx_proc_patient ON fact_medical_procedures(patient_id);
