from flask import Flask, render_template, request, redirect, url_for, session, flash
from pymongo import MongoClient
from hashlib import sha256
import config
import certifi
import uuid
from functools import wraps  # Import wraps for the decorator

app = Flask(__name__)
app.secret_key = b'\xcc^\x91\xea\x17-\xd0W\x03\xa7\xf8J0\xac8\xc5'
app.config.from_object(config)

client = MongoClient(config.MONGO_URI,tlsCAFile=certifi.where())
db = client["Userdatabase"]
col = db["users"]

# Decorator to check if the user is logged in
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            flash('Please log in to continue', 'error')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = col.find_one({'username': username})
        if user and sha256(password.encode("utf-8")).hexdigest() == user['password']:
            session['username'] = username
            return redirect(url_for('welcome'))
        else:
            return render_template('login.html', error='Invalid username or password')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        if password == confirm_password:
            hashed_password = sha256(password.encode("utf-8")).hexdigest()
            col.insert_one({'_id': uuid.uuid4().hex, 'username': username, 'password': hashed_password})
            return redirect(url_for('login'))
        else:
            return render_template('register.html', error='Passwords do not match')
    return render_template('register.html')

@app.route('/welcome')
def welcome():
    if 'username' in session:
        return render_template('profile.html', username=session['username'])
    else:
        flash('Please log in to continue', 'error')
        return redirect(url_for('login'))
    
@app.route('/delete_profile', methods=['GET', 'POST'])
@login_required
def delete_profile():
    if request.method == 'POST':
        username = session['username']
        col.delete_one({'username': username})
        session.pop('username', None)
        flash('Your profile has been deleted.', 'info')
        return redirect(url_for('home'))
    return render_template('profile.html')

@app.route('/update_profile', methods=['GET', 'POST'])
@login_required
def update_profile():
    if request.method == 'POST':
        new_username = request.form['new_username']
        col.update_one({'username': session['username']}, {'$set': {'username': new_username}})
        session['username'] = new_username
        flash('Your profile has been updated.', 'success')
        return redirect(url_for('welcome'))
    return render_template('profile.html', username=session['username'])

if __name__ == '__main__':
    app.run(debug=True)
