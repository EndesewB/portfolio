from flask import Flask, render_template, request, session, redirect, url_for, jsonify
import json

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Replace with a secure secret key

# Function to load user data from data.json
def load_user_data():
    try:
        with open('data.json', 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/signup', methods=['POST'])
def signup():
    username = request.form.get('username')
    email = request.form.get('email')
    password = request.form.get('password')
    confirm_password = request.form.get('confirm_password')

    if password != confirm_password:
        return jsonify({'error': 'Passwords do not match'}), 400

    users = load_user_data()
    if username in users:
        return jsonify({'error': 'Username already exists'}), 400

    users[username] = {'email': email, 'password': password}

    with open('data.json', 'w') as file:
        json.dump(users, file, indent=4)

    session['username'] = username
    return render_template('dashboard.html', username=username)

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')

    users = load_user_data()
    matched_user = users.get(username)

    if matched_user is None or matched_user['password'] != password:
        return jsonify({'error': 'Invalid username or password'}), 401

    session['username'] = username
    return jsonify({'message': 'Login successful', 'username': username}), 200

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))

    username = session['username']

    users = load_user_data()
    user_data = users.get(username)

    if user_data:
        stored_password = user_data.get('password')

        if request.method == 'POST':
            entered_password = request.form.get('password1')
            if entered_password == stored_password:
                return render_template('dashboard.html')
            else:
                return jsonify({'error': 'Invalid password'}), 401

        return render_template('dashboard.html', username=username)
    
    return "User not found"

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
