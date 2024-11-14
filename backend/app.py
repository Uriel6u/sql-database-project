# Import jsonify to return JSON responses
from flask import Flask, jsonify, render_template, request, redirect, url_for, session
from werkzeug.security import check_password_hash, generate_password_hash
import mysql.connector
from dotenv import load_dotenv
import os

load_dotenv()  # Load environment variables from .env file

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY')
try:
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="uriel4sqlroshi$",
        database="shoppingdb"
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
        return render_template('shoppingService/home.html', username=session['username'])
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
            query = "SELECT username, password FROM users WHERE username = %s"
            cursor.execute(query, (username,))
            user = cursor.fetchone()

            if user and check_password_hash(user['password'], pwd):
                session['username'] = user['username']
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
        username = request.form['username']
        name = request.form['name']
        pwd = request.form['password']
        email = request.form['email']
        city = request.form['city']
        state = request.form['state']

        # Check if the username or email already exists
        cursor.execute("SELECT * FROM users WHERE username = %s OR email = %s", (username, email))
        existing_user = cursor.fetchone()

        if existing_user:
            return render_template('userAuth/register.html', error="Username or email already exists. Please choose a different one.")
        #insert new user infomation
        # Hash the password before storing it in the database
        hashed_password = generate_password_hash(pwd)
        # Insert the new user into the Users table (with a parameterized query)
        query = "INSERT INTO users (username, name, password, email, city, state) VALUES (%s, %s, %s, %s, %s, %s)"
        try:
            cursor.execute(query, (username, name, hashed_password, email, city, state))
            db.commit()  # Commit the transaction to save changes
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

@app.route('/check-secret')
def check_secret():
    return f"SECRET_KEY is: {app.secret_key}"

@app.route('/check-db')
def check_db():
    try:
        # Replace 'your_table' with an existing table name in your database
        cursor.execute("SELECT * FROM users LIMIT 1")
        result = cursor.fetchone()
        if result:
            return f"Database connection successful. Sample data: {result}"
        else:
            return "Database connection successful but no data found."
    except mysql.connector.Error as err:
        return f"Database connection failed: {err}"

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if 'username' not in session:
        return redirect(url_for('login'))

    username = session['username']

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
    return render_template('shoppingService/profile.html', user=user, message=locals().get('message'))


if __name__ == '__main__':
    app.run(debug=True)