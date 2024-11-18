# Import jsonify to return JSON responses
from flask import Flask, jsonify, render_template, request, redirect, url_for, session
from werkzeug.security import check_password_hash, generate_password_hash
import mysql.connector
from dotenv import load_dotenv
import os
import random
from faker import Faker
load_dotenv()  # Load environment variables from .env file

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY')
try:
    db = mysql.connector.connect(
    host=os.getenv('DB_HOST', 'localhost'),
    user=os.getenv('DB_USER', 'root'),
    password=os.getenv('DB_PASSWORD', 'uriel4sqlroshi$'),
    database=os.getenv('DB_NAME', 'shoppingdb')
)
    cursor = db.cursor(dictionary=True)  # Enables dictionary-style access
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
        ("2131 Abbott Martin Rd, Nashville, TN 37215", "Nashville"),
        ("3909 Gallatin Pike, Nashville, TN 37216", "Nashville"),
        ("1010 Murfreesboro Pike, Nashville, TN 37217", "Nashville"),
        ("7301 Hwy 70 S, Nashville, TN 37221", "Nashville"),
        ("5825 Nolensville Pike, Nashville, TN 37211", "Nashville")
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



# Generate Products
def generate_products(n):
    for _ in range(n):
        category = random.choice(list(category_products.keys()))
        product_name = random.choice(category_products[category])
        price = round(random.uniform(5, 500), 2)

        query = "INSERT INTO Products (product_name, category, price) VALUES (%s, %s, %s)"
        cursor.execute(query, (product_name, category, price))
    db.commit()




# Generate Promotions
def generate_promotions(n):
    cursor.execute("SELECT store_id, store_type FROM Stores")
    stores = cursor.fetchall()

    cursor.execute("SELECT product_id, category FROM Products")
    products = cursor.fetchall()

    category_to_products = {}
    for product in products:
        category = product['category']
        if category not in category_to_products:
            category_to_products[category] = []
        category_to_products[category].append(product['product_id'])

    for _ in range(n):
        store = random.choice(stores)
        store_id, store_type = store['store_id'], store['store_type']

        valid_categories = store_type_to_categories.get(store_type, [])
        valid_products = [
            product_id for category in valid_categories
            for product_id in category_to_products.get(category, [])
        ]

        if not valid_products:
            continue

        product_id = random.choice(valid_products)
        discount = round(random.uniform(10, 70), 2)
        description = fake.sentence(nb_words=10)
        start_date = fake.date_between(start_date="-30d", end_date="today")
        end_date = fake.date_between(start_date="today", end_date="+30d")

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