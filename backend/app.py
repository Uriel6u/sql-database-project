

# Import jsonify to return JSON responses
from flask import Flask, jsonify, render_template, request, redirect, url_for, session
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
    return "<p>Home Page</p>"



if __name__ == '__main__':
    app.run(debug=True)