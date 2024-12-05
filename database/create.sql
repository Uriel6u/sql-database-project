

-- Create project database
CREATE DATABASE ShoppingDB;
USE ShoppingDB;
show tables;
-- users table
CREATE TABLE Users (
    user_ID INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(100) NOT NULL UNIQUE,
    name VARCHAR(100),
    email VARCHAR(255) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    city VARCHAR(100),
    state VARCHAR(100),
    account_type ENUM('user', 'business') NOT NULL
);


CREATE TABLE Stores (
    store_id INT PRIMARY KEY AUTO_INCREMENT,
    store_name VARCHAR(255) NOT NULL,
    location TEXT NOT NULL,
    city VARCHAR(100) NOT NULL,  -- New column for city-based searches
    contact_info VARCHAR(50),
    store_type ENUM(
        'Electronics', 
        'Clothing', 
        'Grocery', 
        'Furniture', 
        'Sports', 
        'Books', 
        'Personal Care', 
        'Department Store',
        'Other'
    ) NOT NULL,
    created_by_user INT,
    FOREIGN KEY (created_by_user) REFERENCES Users(user_ID)
);



-- promotions table
CREATE TABLE Promotions (
    promo_id INT PRIMARY KEY AUTO_INCREMENT,
    store_id INT,
    product_id INT,
    discount DECIMAL(5, 2),
    description VARCHAR(255),
    start_date DATE,
    end_date DATE,
    FOREIGN KEY (store_id) REFERENCES Stores(store_id) ON DELETE CASCADE,
    FOREIGN KEY (product_id) REFERENCES Products(product_id) ON DELETE CASCADE
);

-- promotions table
CREATE TABLE IF NOT EXISTS Products (
    product_id INT PRIMARY KEY AUTO_INCREMENT,
    product_name VARCHAR(100) NOT NULL,
    category ENUM(
        'Electronics', 
        'Clothing', 
        'Food', 
        'Furniture', 
        'Sports Equipment', 
        'Toys & Games', 
        'Books', 
        'Arts & Crafts', 
        'Personal Care',
        'Other'
    ) NOT NULL,
    price DECIMAL(10, 2)
);

SELECT* FROM stores;
SELECT* FROM users;
SELECT* FROM products;
SELECT* FROM promotions;