CREATE SCHEMA IF NOT EXISTS sales;
CREATE SCHEMA IF NOT EXISTS staging;

CREATE TABLE sales.sales_data (
    order_id INT PRIMARY KEY,
    user_id VARCHAR(20),
    customer_name VARCHAR(255),
    city VARCHAR(255),
    product VARCHAR(255),
    quantity INT,
    total_amount NUMERIC(10,2),
    order_month VARCHAR(7)
);

CREATE TABLE staging.sales_data (
    order_id INT,
    user_id VARCHAR(20),
    customer_name VARCHAR(255),
    city VARCHAR(255),
    product VARCHAR(255),
    quantity INT,
    total_amount NUMERIC(10,2),
    order_month VARCHAR(7)
);

CREATE TABLE staging.pipeline_metadata (

    batch_id TEXT,

    load_time TIMESTAMP,

    row_count INT,

    status TEXT
);

CREATE TABLE sales.watermark_table (
    id int PRIMARY KEY,

    table_name TEXT,

    last_updated_at TIMESTAMP
);