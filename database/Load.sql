USE ShoppingDB;

-- Insert test data into Users table
INSERT INTO Users (username, name, email, password, city, state, account_type)
VALUES
('user1', 'John Doe', 'johndoe@example.com', 'hashed_password', 'Nashville', 'TN', 'user'),
('business1', 'Tech Store', 'techstore@example.com', 'hashed_password', 'Nashville', 'TN', 'business'),
('user2', 'Jane Smith', 'janesmith@example.com', 'hashed_password', 'Memphis', 'TN', 'user'),
('business2', 'Clothing Co', 'clothingco@example.com', 'hashed_password', 'Chattanooga', 'TN', 'business');

-- Insert test data into Stores table
INSERT INTO Stores (store_name, location, city, contact_info, store_type, created_by_user)
VALUES
('Best Electronics', '123 Tech Lane, Nashville, TN', 'Nashville', '123-456-7890', 'Electronics', 2),
('Fashion Hub', '456 Style St, Chattanooga, TN', 'Chattanooga', '987-654-3210', 'Clothing', 4),
('Grocery Outlet', '789 Fresh Ave, Memphis, TN', 'Memphis', '555-555-5555', 'Grocery', 2);

-- Insert test data into Products table
INSERT INTO Products (product_name, category, price)
VALUES
('Laptop', 'Electronics', 799.99),
('Jeans', 'Clothing', 49.99),
('Organic Apples', 'Food', 3.99),
('Desk Chair', 'Furniture', 129.99),
('Soccer Ball', 'Sports Equipment', 19.99);

-- Insert test data into Promotions table
INSERT INTO Promotions (store_id, product_id, discount, description, start_date, end_date)
VALUES
(1, 1, 10.00, '10% off on all laptops', '2024-12-01', '2024-12-15'),
(2, 2, 20.00, '20% off on jeans', '2024-12-05', '2024-12-25'),
(3, 3, 5.00, 'Discount on organic apples', '2024-12-01', '2024-12-31');



--
-- load.sql: Database Data Loading Script for ShoppingDB
--
-- This script is one of two ways to populate the ShoppingDB database with test data:
-- 1. Use load.sql: Manually insert predefined test data for Users, Stores, Products, and Promotions 
--    directly into the database. 


-- 2. **Run mockDataGen.py**: Alternatively, execute the Python script to dynamically generate large 
--    volumes of randomized test data. This is useful for stress testing and load simulations.