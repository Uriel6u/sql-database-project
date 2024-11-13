INSERT INTO Users (name, location, interests) VALUES 
('Alice Johnson', 'New York, NY', 'Electronics, Fashion'),
('Bob Smith', 'Los Angeles, CA', 'Sports, Home Goods'),
('Carol Williams', 'Chicago, IL', 'Books, Electronics');

INSERT INTO Stores (store_name, location, contact_info) VALUES 
('TechHub', '123 Main St, New York, NY', 'contact@techhub.com'),
('SportsMart', '456 Oak Ave, Los Angeles, CA', 'info@sportsmart.com'),
('HomeGoods Plus', '789 Pine Rd, Chicago, IL', 'service@homegoodsplus.com');

INSERT INTO Products (product_name, category, price) VALUES 
('4K Smart TV', 'Electronics', 699.99),
('Running Shoes', 'Sports', 89.99),
('Coffee Maker', 'Home Goods', 49.99),
('Wireless Headphones', 'Electronics', 159.99),
('Yoga Mat', 'Sports', 29.99);

INSERT INTO Promotions (store_id, product_id, discount, start_date, end_date) VALUES 
(1, 1, 15.00, '2024-11-01', '2024-11-30'),
(2, 2, 20.00, '2024-11-01', '2024-11-15'),
(3, 3, 10.00, '2024-11-01', '2024-11-30'),
(1, 4, 25.00, '2024-11-15', '2024-11-30'),
(2, 5, 15.00, '2024-11-01', '2024-11-30');