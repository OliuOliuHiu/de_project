CREATE SCHEMA IF NOT EXISTS sales;

-- Tạo bảng trong schema sales
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