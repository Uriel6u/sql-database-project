

# Import jsonify to return JSON responses
from flask import Flask, jsonify, render_template, request, redirect, url_for, session
from werkzeug.security import check_password_hash, generate_password_hash
import mysql.connector
app = Flask(__name__)
app.secret_key = 'your_secret-key'

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
def home():
    # if user is logged in, go to homeapage with logged in info
    if 'username' in session:
            return render_template('home.html', username=session['username'])
    else:
         return render_template('home.html')

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
                return render_template('login.html', error='Invalid username or password')
        return render_template('login.html')

#Register functionality
@app.route('/register', methods= ['GET','POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        pwd = request.form['password']

        #inset into table users code here
        # Hash the password before storing it in the database
        hashed_password = generate_password_hash(pwd)
        # Insert the new user into the Users table (with a parameterized query)
        query = "INSERT INTO users (username, password) VALUES (%s, %s)"
        try:
            cursor.execute(query, (username, hashed_password))
            db.commit()  # Commit the transaction to save changes
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return render_template('register.html', error="Registration failed. Try again.")
        #after registering, redirect to login page
        return redirect(url_for('login'))
    # render registration form
    return render_template('register.html')


@app.route('/logout')
def logout():
     session.pop('username', None)
     return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)