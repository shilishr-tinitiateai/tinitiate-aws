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
               "Matthew", "Betty", "Anthony", "Margaret", "Donald", "Sandra", "Mark", "Ashley",
               "Paul", "Kimberly", "Steven", "Emily", "Andrew", "Donna", "Kenneth", "Michelle",
               "Joshua", "Carol", "Kevin", "Amanda", "Brian", "Dorothy", "George", "Melissa"]

LAST_NAMES = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis",
              "Rodriguez", "Martinez", "Hernandez", "Lopez", "Gonzalez", "Wilson", "Anderson",
              "Thomas", "Taylor", "Moore", "Jackson", "Martin", "Lee", "Perez", "Thompson",
              "White", "Harris", "Sanchez", "Clark", "Ramirez", "Lewis", "Robinson", "Walker",
              "Young", "Allen", "King", "Wright", "Scott", "Torres", "Nguyen", "Hill", "Flores"]

STREET_NAMES = ["Main St", "Highland Ave", "Maple St", "Oak St", "Washington Ave", "Park Rd",
                "Cedar St", "Pine St", "Elm St", "Lakeview Dr", "Sunset Blvd", "Broadway",
                "Market St", "Chestnut St", "Walnut St", "Center St", "River Rd", "Lincoln Way"]

CITIES_STATES = [
    ("New York", "NY", "10001"), ("Los Angeles", "CA", "90001"), ("Chicago", "IL", "60601"),
    ("Houston", "TX", "77001"), ("Phoenix", "AZ", "85001"), ("Philadelphia", "PA", "19101"),
    ("San Antonio", "TX", "78201"), ("San Diego", "CA", "92101"), ("Dallas", "TX", "75201"),
    ("San Jose", "CA", "95101"), ("Austin", "TX", "78701"), ("Jacksonville", "FL", "32201"),
    ("Fort Worth", "TX", "76101"), ("Columbus", "OH", "43201"), ("Charlotte", "NC", "28201"),
    ("San Francisco", "CA", "94101"), ("Indianapolis", "IN", "46201"), ("Seattle", "WA", "98101"),
    ("Denver", "CO", "80201"), ("Washington", "DC", "20001"), ("Boston", "MA", "02101"),
    ("El Paso", "TX", "79901"), ("Nashville", "TN", "37201"), ("Detroit", "MI", "48201"),
    ("Oklahoma City", "OK", "73101"), ("Portland", "OR", "97201"), ("Las Vegas", "NV", "89101"),
    ("Memphis", "TN", "38101"), ("Louisville", "KY", "40201"), ("Baltimore", "MD", "21201"),
    ("Milwaukee", "WI", "53201"), ("Albuquerque", "NM", "87101"), ("Tucson", "AZ", "85701"),
    ("Fresno", "CA", "93701"), ("Sacramento", "CA", "95801"), ("Mesa", "AZ", "85201"),
    ("Kansas City", "MO", "64101"), ("Atlanta", "GA", "30301"), ("Omaha", "NE", "68101"),
    ("Colorado Springs", "CO", "80901"), ("Raleigh", "NC", "27601"), ("Miami", "FL", "33101")
]

CATEGORIES = {
    "Electronics": ["Smartphones", "Laptops", "Audio & Headphones", "Smart Home", "Accessories", "Wearables"],
    "Apparel": ["Men's Clothing", "Women's Clothing", "Footwear", "Outerwear", "Sportswear", "Accessories"],
    "Home & Kitchen": ["Cookware", "Small Appliances", "Bedding", "Furniture", "Decor", "Storage"],
    "Beauty & Care": ["Skincare", "Haircare", "Cosmetics", "Personal Care", "Fragrances"],
    "Sports & Outdoors": ["Fitness Gear", "Camping & Hiking", "Cycling", "Team Sports", "Water Sports"],
    "Grocery & Pantry": ["Beverages", "Snacks", "Canned Goods", "Breakfast", "Organic Foods", "Condiments"],
    "Toys & Games": ["Action Figures", "Board Games", "Puzzles", "Outdoor Toys", "Educational Toys"],
    "Automotive": ["Car Care", "Tools & Equipment", "Interior Accessories", "Oils & Fluids"]
}

BRANDS = ["Apex", "Aura", "Nova", "Zenith", "Vortex", "Pulse", "Summit", "Lumina", 
          "Titan", "Echo", "Prism", "Matrix", "Horizon", "Velocity", "Sol"];

PAYMENT_METHODS = ["Credit Card", "Debit Card", "Cash", "Apple Pay", "Gift Card"]
ORDER_CHANNELS = ["In-Store", "Online", "Mobile App"]
SEGMENTS = ["VIP", "Regular", "New", "Inactive"]

def generate_retail_dataset(db_path, csv_dir, json_dir=None):
    print(f"--- Generating Retail Dataset ---")
    start_time = time.time()
    
    os.makedirs(csv_dir, exist_ok=True)
    if json_dir is None:
        json_dir = os.path.join(os.path.dirname(csv_dir), "retail_json")
    os.makedirs(json_dir, exist_ok=True)
    
    if os.path.exists(db_path):
        os.remove(db_path)
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Load Schema
    base_dir = os.path.dirname(os.path.abspath(__file__))
    schema_path = os.path.join(base_dir, "retail_schema.sql")
    with open(schema_path, "r") as f:
        cursor.executescript(f.read())
        
    print("Schema created successfully.")

    # 1. Time Dimension (3 years: 2023-08-27 to 2026-08-27)
    print("Generating Time Dimension...")
    start_date = datetime.date(2023, 8, 27)
    end_date = datetime.date(2026, 8, 27)
    curr_date = start_date
    time_rows = []
    
    holidays = {
        (1, 1), (7, 4), (11, 25), (12, 25) # simplified holidays
    }
    
    while curr_date <= end_date:
        date_id = int(curr_date.strftime("%Y%m%d"))
        day_of_week = curr_date.weekday() + 1 # 1=Mon, 7=Sun
        day_name = curr_date.strftime("%A")
        day_of_month = curr_date.day
        month = curr_date.month
        month_name = curr_date.strftime("%B")
        quarter = (month - 1) // 3 + 1
        year = curr_date.year
        is_weekend = 1 if day_of_week in [6, 7] else 0
        is_holiday = 1 if (month, day_of_month) in holidays else 0
        
        time_rows.append((date_id, curr_date.isoformat(), day_of_week, day_name,
                          day_of_month, month, month_name, quarter, year, is_weekend, is_holiday))
        curr_date += datetime.timedelta(days=1)
        
    cursor.executemany("INSERT INTO time_dimension VALUES (?,?,?,?,?,?,?,?,?,?,?)", time_rows)
    conn.commit()
    print(f"Time Dimension inserted: {len(time_rows)} days.")

    # 2. Locations (1,300 locations: 1,250 stores + 50 warehouses)
    print("Generating 1,300 Locations...")
    loc_rows = []
    regions = ["North", "South", "East", "West", "Midwest"]
    
    for loc_id in range(1, 1301):
        city, state, zip_code = random.choice(CITIES_STATES)
        region = random.choice(regions)
        if loc_id <= 1250:
            loc_type = "Store"
            name = f"Store #{loc_id:04d} - {city}"
            sq_ft = random.randint(5000, 120000)
        else:
            loc_type = "Warehouse"
            name = f"DC/Warehouse #{loc_id - 1250:02d} - {city}"
            sq_ft = random.randint(150000, 500000)
            
        opened = start_date - datetime.timedelta(days=random.randint(100, 3650))
        loc_rows.append((loc_id, name, loc_type, region, city, state, zip_code, sq_ft, opened.isoformat()))
        
    cursor.executemany("INSERT INTO locations VALUES (?,?,?,?,?,?,?,?,?)", loc_rows)
    conn.commit()
    print("Locations inserted.")

    # 3. Products (10,000 products)
    print("Generating 10,000 Products...")
    prod_rows = []
    cat_keys = list(CATEGORIES.keys())
    
    for prod_id in range(1, 10001):
        cat = random.choice(cat_keys)
        subcat = random.choice(CATEGORIES[cat])
        brand = random.choice(BRANDS)
        sku = f"SKU-{cat[:3].upper()}-{prod_id:06d}"
        p_name = f"{brand} {subcat} Model-{prod_id % 1000 + 1:03d}"
        cost = round(random.uniform(5.0, 450.0), 2)
        margin = random.uniform(1.25, 2.5)
        price = round(cost * margin, 2)
        is_active = 1 if random.random() > 0.05 else 0
        
        prod_rows.append((prod_id, sku, p_name, cat, subcat, brand, cost, price, is_active))
        
    cursor.executemany("INSERT INTO products VALUES (?,?,?,?,?,?,?,?,?)", prod_rows)
    conn.commit()
    print("Products inserted.")

    # 4. Customers (100,000 customers) & Addresses
    print("Generating 100,000 Customers & Customer Addresses...")
    cust_rows = []
    addr_rows = []
    
    for cust_id in range(1, 100001):
        fname = random.choice(FIRST_NAMES)
        lname = random.choice(LAST_NAMES)
        email = f"{fname.lower()}.{lname.lower()}{cust_id}@example-domain.com"
        phone = f"{random.randint(200, 999)}-{random.randint(100, 999)}-{random.randint(1000, 9999)}"
        gender = random.choice(["Male", "Female", "Non-binary"])
        dob = start_date - datetime.timedelta(days=random.randint(6570, 25550)) # 18 to 70 yrs old
        signup = start_date - datetime.timedelta(days=random.randint(0, 1095))
        segment = random.choice(SEGMENTS)
        
        cust_rows.append((cust_id, fname, lname, email, phone, gender, dob.isoformat(), signup.isoformat(), segment))
        
        # Address
        city, state, zip_code = random.choice(CITIES_STATES)
        street = f"{random.randint(100, 9999)} {random.choice(STREET_NAMES)}"
        addr_rows.append((cust_id, cust_id, street, city, state, zip_code, "USA", 1))
        
    cursor.executemany("INSERT INTO customers VALUES (?,?,?,?,?,?,?,?,?)", cust_rows)
    cursor.executemany("INSERT INTO customer_addresses VALUES (?,?,?,?,?,?,?,?)", addr_rows)
    conn.commit()
    print("Customers & Addresses inserted.")

    # 5. Store Inventory (100,000 rows)
    print("Generating 100,000 Store Inventory records...")
    store_inv_rows = []
    for inv_id in range(1, 100001):
        loc_id = random.randint(1, 1250)
        prod_id = random.randint(1, 10000)
        qty = random.randint(5, 500)
        reorder = random.randint(10, 50)
        reorder_qty = reorder * random.randint(2, 5)
        restock = end_date - datetime.timedelta(days=random.randint(0, 60))
        store_inv_rows.append((inv_id, loc_id, prod_id, qty, reorder, reorder_qty, restock.isoformat()))
        
    cursor.executemany("INSERT INTO store_inventory VALUES (?,?,?,?,?,?,?)", store_inv_rows)
    conn.commit()
    print("Store Inventory inserted.")

    # 6. Warehouse Inventory (100,000 rows)
    print("Generating 100,000 Warehouse Inventory records...")
    wh_inv_rows = []
    for inv_id in range(1, 100001):
        loc_id = random.randint(1251, 1300)
        prod_id = random.randint(1, 10000)
        qty = random.randint(500, 20000)
        reserved = int(qty * random.uniform(0.05, 0.25))
        reorder = random.randint(500, 2000)
        received = end_date - datetime.timedelta(days=random.randint(0, 90))
        wh_inv_rows.append((inv_id, loc_id, prod_id, qty, reserved, reorder, received.isoformat()))
        
    cursor.executemany("INSERT INTO warehouse_inventory VALUES (?,?,?,?,?,?,?)", wh_inv_rows)
    conn.commit()
    print("Warehouse Inventory inserted.")

    # 7. Sales Transactions (1,000,000 transactions across 3 years)
    print("Generating 1,000,000 Sales Transactions in batches...")
    
    # Pre-cache product prices for speed
    prod_prices = {row[0]: row[7] for row in prod_rows}
    
    batch_size = 100000
    total_sales = 1000000
    
    for batch_start in range(1, total_sales + 1, batch_size):
        tx_rows = []
        batch_end = min(batch_start + batch_size - 1, total_sales)
        
        for tx_id in range(batch_start, batch_end + 1):
            random_days = random.randint(0, 1095)
            tx_date = start_date + datetime.timedelta(days=random_days)
            date_id = int(tx_date.strftime("%Y%m%d"))
            
            random_seconds = random.randint(28800, 75600) # 8am to 9pm
            tx_datetime = datetime.datetime.combine(tx_date, datetime.time()) + datetime.timedelta(seconds=random_seconds)
            
            cust_id = random.randint(1, 100001 - 1)
            loc_id = random.randint(1, 1250)
            prod_id = random.randint(1, 10000)
            
            unit_p = prod_prices[prod_id]
            qty = random.choices([1, 2, 3, 4, 5], weights=[60, 25, 10, 3, 2])[0]
            
            disc_rate = random.choice([0.0, 0.0, 0.0, 0.05, 0.10, 0.15, 0.20])
            discount = round(unit_p * qty * disc_rate, 2)
            subtotal = (unit_p * qty) - discount
            tax = round(subtotal * 0.07, 2)
            total = round(subtotal + tax, 2)
            
            pmt = random.choice(PAYMENT_METHODS)
            channel = random.choice(ORDER_CHANNELS)
            
            tx_rows.append((tx_id, tx_datetime.isoformat(), date_id, cust_id, loc_id, prod_id,
                            qty, unit_p, discount, tax, total, pmt, channel))
            
        cursor.executemany("INSERT INTO sales_transactions VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)", tx_rows)
        conn.commit()
        print(f"   Inserted batch {batch_start} to {batch_end} transactions...")

    tables = ["time_dimension", "customers", "customer_addresses", "locations", 
              "products", "sales_transactions", "store_inventory", "warehouse_inventory"]

    # Export to CSVs
    print("Exporting Retail tables to CSV files...")
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
    print("Exporting Retail tables to JSON files...")
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
    print(f"--- Retail Dataset Completed in {elapsed} seconds ---")

if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.abspath(__file__))
    db_file = os.path.join(base_dir, "retail.db")
    csv_folder = os.path.join(base_dir, "data", "retail_csv")
    json_folder = os.path.join(base_dir, "data", "retail_json")
    generate_retail_dataset(db_file, csv_folder, json_folder)

