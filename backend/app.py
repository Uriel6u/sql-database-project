
from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.security import check_password_hash, generate_password_hash
import mysql.connector
from dotenv import load_dotenv
from collections import defaultdict
import os

load_dotenv()  # Load environment variables from .env file

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY')
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


cursor = db.cursor(dictionary=True)

@app.route("/")
def root():
    # Check if the user is logged in
    if 'username' in session:
        # Redirect to the home page if logged in
        return redirect(url_for('home'))
    else:
        # Redirect to the login page if not logged in
        return redirect(url_for('login'))

@app.route("/home")
def home():
    # Check if user is logged in
    if 'username' in session:
        # If logged in, render the home page with the username
        account_type = session['account_type']
        top_promotions = get_top_promotions()  # Get the top promotions
        return render_template(
            'shoppingService/home.html',
            username=session['username'],
            account_type=account_type,
            current_page='home',
            top_promotions=top_promotions  # Pass to the template
        )
    else:
        # If not logged in, redirect to the login page
        return redirect(url_for('login'))
    
@app.route("/get_top_promotions", methods=['POST'])
def get_top_promotions():
    query = """
    SELECT 
        p.promo_id, 
        p.discount, 
        p.description, 
        s.store_name, 
        s.location, 
        pr.category
    FROM Promotions p
    JOIN Stores s ON p.store_id = s.store_id
    JOIN Products pr ON p.product_id = pr.product_id
    """
    cursor.execute(query)
    promotions = cursor.fetchall()

    if not promotions:
        print("No promotions found.")  # Debugging line
        return {}

    # Group promotions by category and sort each category's promotions by discount
    grouped_promotions = defaultdict(list)
    for promo in promotions:
        grouped_promotions[promo['category']].append(promo)

    # For each category, sort the promotions by discount and get top 4
    top_promotions = {}
    for category, promos in grouped_promotions.items():
        sorted_promos = sorted(promos, key=lambda x: x['discount'], reverse=True)  # Sort by discount
        top_promotions[category] = sorted_promos[:4]  # Take only the top 4

    return top_promotions

    
@app.route('/search', methods=['GET'])
def search():

    # Fetch the account type in session
    account_type = session['account_type']

    # Fetch cities for dropdown
    cursor.execute("SELECT DISTINCT city FROM Stores")
    cities = [row['city'] for row in cursor.fetchall()]

    # Hardcoded store types (ENUM values in the database)
    store_types = [
        "Electronics", "Clothing", "Grocery", "Furniture", "Sports",
        "Books", "Personal Care", "Department Store", "Other"
    ]

    # Hardcoded product categories (ENUM values from Products table)
    product_categories = [
        "Electronics", "Clothing", "Food", "Furniture", "Sports Equipment",
        "Toys & Games", "Books", "Arts & Crafts", "Personal Care", "Other"
    ]

    return render_template(
        'shoppingService/search.html',
        account_type=account_type,
        cities=cities,
        store_types=store_types,
        product_categories=product_categories,
        stores=[],
        promotions=[],
        search_type=None
    )




@app.route('/search_stores', methods=['POST'])
def search_stores():

    # Fetch the account type in session
    account_type = session['account_type']

    # Fetch cities for dropdown
    cursor.execute("SELECT DISTINCT city FROM Stores")
    cities = [row['city'] for row in cursor.fetchall()]

    # Hardcoded store types
    store_types = [
        "Electronics", "Clothing", "Grocery", "Furniture", "Sports",
        "Books", "Personal Care", "Department Store", "Other"
    ]

    # Retrieve form data
    store_name = request.form.get('store_name')
    selected_store_type = request.form.get('store_type')
    selected_city = request.form.get('store_city')

    # Base query
    query = "SELECT * FROM Stores WHERE 1=1"
    params = []

    # Add filters dynamically
    if store_name:
        query += " AND store_name LIKE %s"
        params.append(f"%{store_name}%")
    if selected_store_type:
        query += " AND store_type = %s"
        params.append(selected_store_type)
    if selected_city:
        query += " AND city = %s"
        params.append(selected_city)

    cursor.execute(query, params)
    stores = cursor.fetchall()

    return render_template(
        'shoppingService/search.html',
        account_type=account_type,
        stores=stores,
        promotions=[],
        search_type='stores',
        cities=cities,
        store_types=store_types
    )


    
@app.route('/search_promotions', methods=['POST'])
def search_promotions():

    # Fetch the account type in session
    account_type = session['account_type']

    # Fetch cities for dropdown
    cursor.execute("SELECT DISTINCT city FROM Stores")
    cities = [row['city'] for row in cursor.fetchall()]

    # Hardcoded product categories
    product_categories = [
        "Electronics", "Clothing", "Food", "Furniture", "Sports Equipment",
        "Toys & Games", "Books", "Arts & Crafts", "Personal Care", "Other"
    ]

    # Retrieve form data
    min_discount = request.form.get('min_discount') or 0
    max_discount = request.form.get('max_discount') or 100
    selected_category = request.form.get('discount_category')
    selected_city = request.form.get('city')

    # Base query with joins
    query = """
    SELECT p.promo_id, p.discount, p.description, s.store_name, s.city, pr.category
    FROM Promotions p
    JOIN Stores s ON p.store_id = s.store_id
    JOIN Products pr ON p.product_id = pr.product_id
    WHERE p.discount BETWEEN %s AND %s
    """
    params = [min_discount, max_discount]

    # Add filters dynamically
    if selected_category:
        query += " AND pr.category = %s"
        params.append(selected_category)
    if selected_city:
        query += " AND s.city = %s"
        params.append(selected_city)

    cursor.execute(query, params)
    promotions = cursor.fetchall()

    return render_template(
        'shoppingService/search.html',
        account_type=account_type,
        promotions=promotions,
        stores=[],
        search_type='promotions',
        cities=cities,
        product_categories=product_categories,
        min_discount=min_discount,
        max_discount=max_discount,
        selected_category=selected_category,
        selected_city=selected_city
    )





@app.route("/about")
def about():
    # Check if user is logged in
    if 'username' in session:
        # If logged in, render the home page with the username
        account_type = session['account_type']
        return render_template('shoppingService/about.html', account_type=account_type, current_page='about')
    else:
        # If not logged in, redirect to the login page
        return redirect(url_for('login'))

#login functionality
@app.route('/login', methods= ['GET','POST'])
def login():
        if request.method == 'POST':
            username = request.form['username']
            pwd = request.form['password']
           
            # Use a parameterized query to prevent SQL injection
            query = "SELECT user_ID, username, password, account_type FROM Users WHERE username = %s"
            cursor.execute(query, (username,))
            user = cursor.fetchone()

            if user and check_password_hash(user['password'], pwd):
                session['user_id'] = user['user_ID'] # store user id
                session['username'] = user['username']# store username 
                session['account_type'] = user['account_type'] # store account type in session
                return redirect(url_for('home'))
            else:
                return render_template('userAuth/login.html', error='Invalid username or password')
        return render_template('userAuth/login.html')

#Register functionality
@app.route('/register', methods= ['GET','POST'])
def register():
    if request.method == 'POST':
        # Debugging line to print the form data to the console
        print("Form data received:", request.form)
        username = request.form['username'] # basic info
        name = request.form['name']
        pwd = request.form['password']
        email = request.form['email']
        city = request.form['city']
        state = request.form['state']
        account_type = request.form['account_type'] # to get option of users or business
        # testing print account_type to confirm the correct value
        print("Final account type before insert:", account_type)  # This should print 'user' or 'business'
        # Check if the username or email already exists
        cursor.execute("SELECT * FROM users WHERE username = %s OR email = %s", (username, email))
        existing_user = cursor.fetchone()

        if existing_user:
            return render_template('userAuth/register.html', error="Username or email already exists. Please choose a different one.")
        #insert new user infomation
        # Hash the password before storing it in the database
        hashed_password = generate_password_hash(pwd)
        # Insert the new user into the Users table (with a parameterized query)
        query = "INSERT INTO users (username, name, password, email, city, state, account_type) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        try:
            cursor.execute(query, (username, name, hashed_password, email, city, state, account_type))
            db.commit()  # Commit the transaction to save changes
              # Verify the saved account_type testing part2
            cursor.execute("SELECT account_type FROM users WHERE username = %s", (username,))
            account_type_saved = cursor.fetchone()
            print("Account type saved in DB:", account_type_saved)
        except mysql.connector.Error as err:
            if err.errno == 1062:  # Error code for duplicate entry
                print(f"Duplicate entry error: {err}")
                return render_template('userAuth/register.html', error="Registration failed. Email or username already exists.")
            else:
                print(f"Error: {err}")
                return render_template('userAuth/register.html', error="Registration failed. Try again.")
        # After registering, redirect to the login page
        return redirect(url_for('login'))
    # render registration form
    return render_template('userAuth/register.html')
    

@app.route('/logout')
def logout():
     session.pop('username', None)
     return redirect(url_for('home'))



@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if 'username' not in session:
        return redirect(url_for('login'))


@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if 'username' not in session:
        return redirect(url_for('login'))

    username = session['username']
    account_type = session['account_type']

    if request.method == 'POST':
        # Get new profile information from the form
        new_city = request.form['city']
        new_state = request.form['state']

        # Update user profile in the database
        try:
            cursor.execute("UPDATE users SET city = %s, state = %s WHERE username = %s", (new_city, new_state, username))
            db.commit()
            message = "Profile updated successfully."
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            error = "Could not update profile. Try again."
            return render_template('shoppingService/profile.html', user=user, error=error)
    
    # Fetch the updated or current user data to display in the form
    cursor.execute("SELECT city, state FROM users WHERE username = %s", (username,))
    user = cursor.fetchone()

    # Render profile page with user data and any messages
    return render_template('shoppingService/profile.html', user=user, message=locals().get('message'), account_type=account_type, current_page='profile')

@app.route('/add_store', methods=['GET', 'POST'])
def add_store():

    account_type = session['account_type']

    if request.method == 'POST':
        store_name = request.form['store_name']
        location = request.form['location']
        city = request.form['city']
        contact_info = request.form['contact_info']
        store_type = request.form['store_type']
        user_id = session['user_id']  # get id of the logged-in business Account

        query = "INSERT INTO Stores (store_name, location, city, contact_info, store_type, created_by_user) VALUES (%s, %s, %s, %s, %s, %s)"
        cursor.execute(query, (store_name, location, city, contact_info, store_type, user_id))
        db.commit()
        # return the home page initially or if the form submission is invalid.
        return redirect(url_for('home'))
    
        
    return render_template('shoppingService/add_store.html', account_type=account_type, current_page='add_store')

@app.route('/add_promotions', methods=['GET', 'POST'])
def add_promotions():

    account_type = session['account_type']

    if request.method == 'POST':
        store_id = request.form['store_id']
        product_id = request.form['product_id']
        discount = request.form['discount']
        description = request.form['description']
        start_date = request.form['start_date']
        end_date = request.form['end_date']


        query = "INSERT INTO Promotions (store_id, product_id, discount, description, start_date, end_date) VALUES (%s, %s, %s, %s, %s, %s)"
        cursor.execute(query, (store_id, product_id, discount, description, start_date, end_date))
        db.commit()
        # return the home page initially or if the form submission is invalid.
        return redirect(url_for('home'))
     # here we fetch the stores that belong to this store id, 
    cursor.execute("SELECT store_id, store_name FROM Stores WHERE created_by_user = %s", (session['user_id'],))
    stores = cursor.fetchall()
   
    # here we must use fetch to pull products data
    cursor.execute("SELECT product_id, product_name FROM Products")
    products = cursor.fetchall()
    #render our add promotions page and pass stores n products variables to be visible on template
    return render_template('shoppingService/add_promotions.html', stores=stores, products=products, account_type=account_type, current_page='add_promotions')

@app.route('/add_product', methods=['GET', 'POST'])
def add_product():

    account_type = session['account_type']

    if request.method == 'POST':
        product_name = request.form['product_name']
        category = request.form['category']
        price = request.form['price']
        

        query = "INSERT INTO Products (product_name, category, price) VALUES (%s, %s, %s)"
        cursor.execute(query, (product_name, category, price))
        db.commit()
        # return the home page initially or if the form submission is invalid.
        return redirect(url_for('home'))
    
        
    return render_template('shoppingService/add_product.html', account_type=account_type, current_page='add_product')

if __name__ == '__main__':
    app.run(debug=False)