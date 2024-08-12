from flask import Flask, request, render_template_string
import sqlite3
import os

app = Flask(__name__)

# Ευπάθεια: Στατικός κωδικός στον κώδικα
SECRET_KEY = "supersecretkey123"

def get_db_connection():
    conn = sqlite3.connect('database.db')
    return conn

@app.route('/')
def index():
    return 'Welcome to the Vulnerable Web App!'

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = get_db_connection()
        cursor = conn.cursor()

        # Ευπάθεια: SQL Injection
        query = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"
        cursor.execute(query)
        user = cursor.fetchone()

        if user:
            return f'Welcome, {username}!'
        else:
            return 'Invalid credentials'
    return '''
        <form method="post">
            Username: <input type="text" name="username"><br>
            Password: <input type="password" name="password"><br>
            <input type="submit" value="Login">
        </form>
    '''

@app.route('/search')
def search():
    query = request.args.get('query', '')

    # Ευπάθεια: XSS
    html = f'<h2>Search Results for "{query}"</h2>'
    return render_template_string(html)

@app.route('/admin')
def admin():
    token = request.args.get('token')

    # Ευπάθεια: Hardcoded admin token
    if token == "admintoken123":
        return 'Welcome, admin!'
    else:
        return 'Unauthorized access', 403

if __name__ == "__main__":
    app.run(debug=True)
