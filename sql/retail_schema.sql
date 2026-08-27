-- Retail Database Schema DDL
-- Compatible with SQLite, PostgreSQL, MySQL, DuckDB, Snowflake, BigQuery

CREATE TABLE IF NOT EXISTS time_dimension (
    date_id INTEGER PRIMARY KEY,        -- YYYYMMDD
    full_date DATE UNIQUE NOT NULL,
    day_of_week INTEGER NOT NULL,
    day_name VARCHAR(10) NOT NULL,
    day_of_month INTEGER NOT NULL,
    month INTEGER NOT NULL,
    month_name VARCHAR(10) NOT NULL,
    quarter INTEGER NOT NULL,
    year INTEGER NOT NULL,
    is_weekend INTEGER NOT NULL,        -- 0 or 1
    is_holiday INTEGER NOT NULL         -- 0 or 1
);

CREATE TABLE IF NOT EXISTS customers (
    customer_id INTEGER PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    phone_number VARCHAR(20),
    gender VARCHAR(10),
    birth_date DATE,
    signup_date DATE NOT NULL,
    customer_segment VARCHAR(20) NOT NULL -- VIP, Regular, New, Inactive
);

CREATE TABLE IF NOT EXISTS customer_addresses (
    address_id INTEGER PRIMARY KEY,
    customer_id INTEGER NOT NULL,
    street_address VARCHAR(150) NOT NULL,
    city VARCHAR(50) NOT NULL,
    state VARCHAR(50) NOT NULL,
    postal_code VARCHAR(20) NOT NULL,
    country VARCHAR(50) NOT NULL DEFAULT 'USA',
    is_primary INTEGER NOT NULL DEFAULT 1,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);

CREATE TABLE IF NOT EXISTS locations (
    location_id INTEGER PRIMARY KEY,
    location_name VARCHAR(100) NOT NULL,
    location_type VARCHAR(20) NOT NULL,  -- Store, Warehouse, Distribution Center
    region VARCHAR(30) NOT NULL,        -- North, South, East, West, Midwest
    city VARCHAR(50) NOT NULL,
    state VARCHAR(50) NOT NULL,
    postal_code VARCHAR(20) NOT NULL,
    square_feet INTEGER,
    opened_date DATE NOT NULL
);

CREATE TABLE IF NOT EXISTS products (
    product_id INTEGER PRIMARY KEY,
    sku VARCHAR(30) UNIQUE NOT NULL,
    product_name VARCHAR(150) NOT NULL,
    category VARCHAR(50) NOT NULL,
    subcategory VARCHAR(50) NOT NULL,
    brand VARCHAR(50) NOT NULL,
    unit_cost DECIMAL(10, 2) NOT NULL,
    unit_price DECIMAL(10, 2) NOT NULL,
    is_active INTEGER NOT NULL DEFAULT 1
);

CREATE TABLE IF NOT EXISTS sales_transactions (
    transaction_id BIGINT PRIMARY KEY,
    transaction_timestamp TIMESTAMP NOT NULL,
    date_id INTEGER NOT NULL,
    customer_id INTEGER NOT NULL,
    location_id INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL,
    unit_price DECIMAL(10, 2) NOT NULL,
    discount_amount DECIMAL(10, 2) NOT NULL DEFAULT 0.00,
    tax_amount DECIMAL(10, 2) NOT NULL DEFAULT 0.00,
    total_amount DECIMAL(10, 2) NOT NULL,
    payment_method VARCHAR(20) NOT NULL, -- Credit Card, Debit Card, Cash, Apple Pay, Gift Card
    order_channel VARCHAR(20) NOT NULL,  -- In-Store, Online, Mobile App
    FOREIGN KEY (date_id) REFERENCES time_dimension(date_id),
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
    FOREIGN KEY (location_id) REFERENCES locations(location_id),
    FOREIGN KEY (product_id) REFERENCES products(product_id)
);

CREATE TABLE IF NOT EXISTS store_inventory (
    inventory_id INTEGER PRIMARY KEY,
    location_id INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    quantity_on_hand INTEGER NOT NULL,
    reorder_point INTEGER NOT NULL,
    reorder_quantity INTEGER NOT NULL,
    last_restock_date DATE NOT NULL,
    FOREIGN KEY (location_id) REFERENCES locations(location_id),
    FOREIGN KEY (product_id) REFERENCES products(product_id)
);

CREATE TABLE IF NOT EXISTS warehouse_inventory (
    warehouse_inventory_id INTEGER PRIMARY KEY,
    location_id INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    quantity_on_hand INTEGER NOT NULL,
    quantity_reserved INTEGER NOT NULL,
    reorder_point INTEGER NOT NULL,
    last_received_date DATE NOT NULL,
    FOREIGN KEY (location_id) REFERENCES locations(location_id),
    FOREIGN KEY (product_id) REFERENCES products(product_id)
);

-- Indexes for optimal querying
CREATE INDEX IF NOT EXISTS idx_sales_date ON sales_transactions(date_id);
CREATE INDEX IF NOT EXISTS idx_sales_cust ON sales_transactions(customer_id);
CREATE INDEX IF NOT EXISTS idx_sales_prod ON sales_transactions(product_id);
CREATE INDEX IF NOT EXISTS idx_sales_loc ON sales_transactions(location_id);
CREATE INDEX IF NOT EXISTS idx_cust_addr ON customer_addresses(customer_id);
CREATE INDEX IF NOT EXISTS idx_store_inv ON store_inventory(location_id, product_id);
CREATE INDEX IF NOT EXISTS idx_wh_inv ON warehouse_inventory(location_id, product_id);
