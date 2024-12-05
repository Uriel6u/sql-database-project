# Import jsonify to return JSON responses
from flask import Flask, jsonify, render_template, request, redirect, url_for, session
from werkzeug.security import check_password_hash, generate_password_hash
import mysql.connector
from dotenv import load_dotenv
import os
import random
from faker import Faker
from datetime import datetime, date
load_dotenv()  # Load environment variables from .env file


try:
    db = mysql.connector.connect(
        host=os.getenv('DB_HOST'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        database=os.getenv('DB_NAME')
    )
    cursor = db.cursor(dictionary=True)
except mysql.connector.Error as err:
    print(f"Error: {err}")




fake = Faker()
# Store and Product Mapping
store_type_to_categories = {
    'Electronics': ['Electronics'],
    'Clothing': ['Clothing'],
    'Grocery': ['Food'],
    'Furniture': ['Furniture'],
    'Sports': ['Sports Equipment', 'Toys & Games'],
    'Books': ['Books', 'Arts & Crafts'],
    'Personal Care': ['Personal Care'],
    'Department Store': ['Electronics', 'Clothing', 'Food', 'Furniture', 'Books']
}

category_products = {
    'Electronics': ['Laptop', 'Smartphone', 'TV', 'Headphones', 'Camera'],
    'Clothing': ['T-Shirt', 'Jeans', 'Jacket', 'Shoes', 'Hat'],
    'Food': ['Bananas', 'Milk', 'Chicken', 'Bread', 'Cheese'],
    'Furniture': ['Sofa', 'Chair', 'Table', 'Bed', 'Bookshelf'],
    'Sports Equipment': ['Basketball', 'Soccer Ball', 'Tennis Racket', 'Yoga Mat', 'Hockey Stick'],
    'Toys & Games': ['Board Game', 'Video Game', 'Card Game', 'Puzzle', 'Lego Set'],
    'Books': ['Mystery Novel', 'Biography', 'Sci-Fi Novel', 'Cookbook', 'History Book'],
    'Arts & Crafts': ['Paint Set', 'Sketchbook', 'Clay', 'Easel', 'Craft Kit'],
    'Personal Care': ['Shampoo', 'Conditioner', 'Toothpaste', 'Deodorant', 'Lotion']
}
# Generate Stores
def generate_stores(n):
    store_name_templates = {
        'Electronics': ['TechWorld', 'Digital Dreams', 'Smart Solutions', 'GadgetHub'],
        'Clothing': ['Fashion Haven', 'Style Stop', 'Clothes Corner', 'Apparel Alley'],
        'Grocery': ['FreshMart', 'Green Grocers', 'Daily Harvest', 'Everyday Groceries'],
        'Furniture': ['Comfort Living', 'Furniture Depot', 'Home Essentials', 'Room Retreat'],
        'Sports': ['PlayZone', 'ActiveLife', 'Sports Gear', 'ProFit Sports'],
        'Books': ['Readers\' Retreat', 'Novelty Books', 'Pages & Co.', 'Barnes & Books'],
        'Personal Care': ['Glow & Go', 'Healthy Essentials', 'Care Corner', 'SelfCare Spa'],
        'Department Store': ['ValueMart', 'BigSavings', 'The General Store', 'Family Center']
    }

    addresses_and_cities = [
    # Nashville
    ("2131 Abbott Martin Rd, Nashville, TN 37215", "Nashville"),
    ("3909 Gallatin Pike, Nashville, TN 37216", "Nashville"),
    ("1010 Murfreesboro Pike, Nashville, TN 37217", "Nashville"),
    ("7301 Hwy 70 S, Nashville, TN 37221", "Nashville"),
    ("5825 Nolensville Pike, Nashville, TN 37211", "Nashville"),
    # Memphis
    ("123 Beale St, Memphis, TN 38103", "Memphis"),
    ("2400 Union Ave, Memphis, TN 38112", "Memphis"),
    ("3450 Poplar Ave, Memphis, TN 38111", "Memphis"),
    ("7980 Winchester Rd, Memphis, TN 38125", "Memphis"),
    ("5200 Park Ave, Memphis, TN 38119", "Memphis"),
    # Chattanooga
    ("201 Broad St, Chattanooga, TN 37402", "Chattanooga"),
    ("1100 Market St, Chattanooga, TN 37402", "Chattanooga"),
    ("600 River St, Chattanooga, TN 37405", "Chattanooga"),
    ("2100 Hamilton Place Blvd, Chattanooga, TN 37421", "Chattanooga"),
    ("315 Frazier Ave, Chattanooga, TN 37405", "Chattanooga"),
    # Knoxville
    ("7600 Kingston Pike, Knoxville, TN 37919", "Knoxville"),
    ("210 N Peters Rd, Knoxville, TN 37923", "Knoxville"),
    ("400 S Gay St, Knoxville, TN 37902", "Knoxville"),
    ("134 N Forest Park Blvd, Knoxville, TN 37919", "Knoxville"),
    ("500 W Church Ave, Knoxville, TN 37902", "Knoxville"),
    # Murfreesboro
    ("1231 NW Broad St, Murfreesboro, TN 37129", "Murfreesboro"),
    ("2615 Medical Center Pkwy, Murfreesboro, TN 37129", "Murfreesboro"),
    ("205 N Thompson Ln, Murfreesboro, TN 37129", "Murfreesboro"),
    ("400 W Northfield Blvd, Murfreesboro, TN 37129", "Murfreesboro"),
    ("1520 Memorial Blvd, Murfreesboro, TN 37129", "Murfreesboro"),
    # Franklin
    ("1800 Galleria Blvd, Franklin, TN 37067", "Franklin"),
    ("500 Cool Springs Blvd, Franklin, TN 37067", "Franklin"),
    ("1101 Murfreesboro Rd, Franklin, TN 37064", "Franklin"),
    ("230 Franklin Rd, Franklin, TN 37064", "Franklin"),
    ("700 Cool Springs Blvd, Franklin, TN 37067", "Franklin"),
    # Other Cities in Tennessee
    ("100 S Main St, Shelbyville, TN 37160", "Shelbyville"),
    ("315 W Jackson St, Cookeville, TN 38501", "Cookeville"),
    ("1501 E Spring St, Cookeville, TN 38506", "Cookeville"),
    ("123 Church St, Lebanon, TN 37087", "Lebanon"),
    ("1501 W Main St, Lebanon, TN 37087", "Lebanon"),
    ("600 S Cumberland St, Lebanon, TN 37087", "Lebanon"),
    ("789 Dixie Ave, Johnson City, TN 37604", "Johnson City"),
    ("210 E Mountcastle Dr, Johnson City, TN 37601", "Johnson City"),
    ("5000 Clinton Hwy, Oak Ridge, TN 37830", "Oak Ridge"),
    ("220 S Illinois Ave, Oak Ridge, TN 37830", "Oak Ridge"),
    ("123 Broadway St, Maryville, TN 37801", "Maryville"),
    ("456 Lamar Alexander Pkwy, Maryville, TN 37801", "Maryville")
]

    for _ in range(n):
        store_type = random.choice(list(store_name_templates.keys()))
        store_name = random.choice(store_name_templates[store_type])
        location, city = random.choice(addresses_and_cities)
        contact_info = fake.phone_number()
        created_by_user = 1  # Default business user ID for testing

        query = """
        INSERT INTO Stores (store_name, location, city, contact_info, store_type, created_by_user)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query, (store_name, location, city, contact_info, store_type, created_by_user))
    db.commit()


# Define price ranges for each product category
category_price_ranges = {
    'Electronics': (100, 2000),
    'Clothing': (10, 150),
    'Food': (1, 50),
    'Furniture': (50, 5000),
    'Sports Equipment': (20, 500),
    'Toys & Games': (5, 100),
    'Books': (5, 50),
    'Arts & Crafts': (10, 200),
    'Personal Care': (5, 50),
}
# Generate the Products
def generate_products(n):
    for _ in range(n):
        # select a random category and product
        category = random.choice(list(category_products.keys()))
        product_name = random.choice(category_products[category])
        
        # Get realistic price range for the category
        price_range = category_price_ranges.get(category, (5, 500))  # Default to 5-500 if no range defined
        price = round(random.uniform(price_range[0], price_range[1]), 2)  # Generate price within range

        # Insert product into database
        query = "INSERT INTO Products (product_name, category, price) VALUES (%s, %s, %s)"
        cursor.execute(query, (product_name, category, price))
    db.commit()

    print(f"{n} products generated successfully!")



def generate_promotions(n):
    from datetime import datetime

   # Get current year as a valid date object
    current_year = datetime.now().year
    year_end_date = date(current_year, 12, 31)  # Convert to a date object

    # Fetch stores with their types
    cursor.execute("SELECT store_id, store_type, store_name FROM Stores")
    stores = cursor.fetchall()  # [{'store_id': 1, 'store_type': 'Electronics', 'store_name': 'TechWorld'}, ...]

    # Fetch products with their categories
    cursor.execute("SELECT product_id, category, product_name FROM Products")
    products = cursor.fetchall()  # [{'product_id': 1, 'category': 'Electronics', 'product_name': 'Laptop'}, ...]

    # Map categories to products for easy lookup
    category_to_products = {}
    product_id_to_name = {}
    for product in products:
        category = product['category']
        product_id = product['product_id']
        product_name = product['product_name']

        if category not in category_to_products:
            category_to_products[category] = []
        category_to_products[category].append(product_id)

        product_id_to_name[product_id] = product_name

    # Store type to realistic discount ranges
    store_type_discount_ranges = {
        'Electronics': (10, 30),  # 10% to 30% off
        'Clothing': (15, 50),  # 15% to 50% off
        'Grocery': (5, 20),  # 5% to 20% off
        'Furniture': (10, 40),  # 10% to 40% off
        'Sports': (10, 30),  # 10% to 30% off
        'Books': (5, 25),  # 5% to 25% off
        'Personal Care': (5, 20),  # 5% to 20% off
        'Department Store': (10, 50),  # 10% to 50% off
        'Other': (5, 30)  # 5% to 30% off
    }

    for _ in range(n):
        # Select a random store
        store = random.choice(stores)
        store_id, store_type, store_name = store['store_id'], store['store_type'], store['store_name']

        # Get valid product categories for this store type
        valid_categories = store_type_to_categories.get(store_type, [])
        valid_products = [
            product_id for category in valid_categories
            for product_id in category_to_products.get(category, [])
        ]

        # Skip if no valid products for this store
        if not valid_products:
            continue

        # Select a random product
        product_id = random.choice(valid_products)
        product_name = product_id_to_name[product_id]

        # Generate a realistic discount
        discount_range = store_type_discount_ranges.get(store_type, (5, 30))
        discount = random.randint(discount_range[0], discount_range[1])  # Whole number percentage

        # Generate description
        description = f"{discount}% off {product_name} in {store_name}"

        # Generate promotion dates within the current year
        start_date = fake.date_this_year(before_today=True, after_today=False)
        end_date = fake.date_between(start_date=start_date, end_date=year_end_date)

        # Insert promotion into database
        query = """
        INSERT INTO Promotions (store_id, product_id, discount, description, start_date, end_date)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query, (store_id, product_id, discount, description, start_date, end_date))

    db.commit()

    print(f"{n} promotions generated successfully!")



# Generate Data
generate_stores(20)  # 20 stores
generate_products(50)  # 50 products
generate_promotions(100)  # 100 promotions

print("Mock data generated successfully!")

# Close the database connection
cursor.close()
db.close()