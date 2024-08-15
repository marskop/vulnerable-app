from flask import Flask, request, render_template_string, make_response, redirect, jsonify
import sqlite3
import os
import subprocess

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
            # Ευπάθεια: Insecure Session Management (Set session ID to username directly)
            resp = make_response(f'Welcome, {username}!')
            resp.set_cookie('session_id', username)  # Insecure cookie handling
            return resp
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

@app.route('/redirect')
def unsafe_redirect():
    url = request.args.get('url')
    
    # Ευπάθεια: Open Redirect
    return redirect(url)

@app.route('/file')
def file_read():
    filename = request.args.get('file')
    
    # Ευπάθεια: Path Traversal
    with open(filename, 'r') as f:
        return f.read()

@app.route('/command')
def command_execution():
    cmd = request.args.get('cmd')
    
    # Ευπάθεια: Command Injection
    output = subprocess.check_output(cmd, shell=True)
    return jsonify(output=output.decode('utf-8'))

@app.route('/xxe', methods=['POST'])
def xxe():
    xml = request.data
    
    # Ευπάθεια: XML External Entity (XXE)
    result = subprocess.run(['xmllint', '--noout', '--xmlout'], input=xml, text=True, capture_output=True)
    return result.stdout

@app.route('/unrestricted_upload', methods=['POST'])
def unrestricted_upload():
    file = request.files['file']
    
    # Ευπάθεια: Unrestricted File Upload
    file.save(os.path.join('/uploads', file.filename))
    return 'File uploaded successfully'

@app.route('/insecure_deserialization', methods=['POST'])
def insecure_deserialization():
    serialized_data = request.data
    
    # Ευπάθεια: Insecure Deserialization
    deserialized_data = eval(serialized_data.decode('utf-8'))  # Extremely dangerous!
    return jsonify(deserialized_data)

if __name__ == "__main__":
    app.run(debug=True)
