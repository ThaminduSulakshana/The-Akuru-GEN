from flask import render_template, request, redirect, url_for, session, flash
from pymongo import MongoClient
from hashlib import sha256
import uuid
from functools import wraps
import config
import certifi

client = MongoClient(config.MONGO_URI, tlsCAFile=certifi.where())
db = client["gg"]
col = db["gg"]

def user_routes(app):
 
    # Decorator to check if the user is logged in
    def login_required(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'username' not in session:
                flash('Please log in to continue', 'success')
                return redirect(url_for('login'))
            return f(*args, **kwargs)
        return decorated_function   
    
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
                flash('Invalid username or password', 'error')
        return render_template('login.html')


    @app.route('/register', methods=['GET', 'POST'])
    def register():
        if request.method == 'POST':
            username = request.form['username']
            email = request.form['email']
            password = request.form['password']
            confirm_password = request.form['confirm_password']
            # Check if username or email already exists
            existing_user = col.find_one({'$or': [{'username': username}, {'email': email}]})
            if existing_user:
                flash('Username or email already exists', 'error')
            elif password == confirm_password:
                hashed_password = sha256(password.encode("utf-8")).hexdigest()
                col.insert_one({'_id': uuid.uuid4().hex, 'username': username, 'email': email, 'password': hashed_password})
                flash('Registration successful! You can now log in.', 'success')
                return redirect(url_for('login'))
            else:
                flash('Passwords do not match', 'error')
        return render_template('register.html')

    @app.route('/welcome')
    @login_required
    def welcome():
        return render_template('profile.html', username=session['username'])

    @app.route('/delete_profile', methods=['GET', 'POST'])
    @login_required
    def delete_profile():
        if request.method == 'POST':
            username = session['username']
            col.delete_one({'username': username})
            session.pop('username', None)
            flash('Your profile has been deleted.', 'info')
            return redirect(url_for('login'))
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
    
    @app.route('/update_email', methods=['GET', 'POST'])
    @login_required
    def update_email():
        if request.method == 'POST':
            new_email = request.form['new_email']
            col.update_one({'username': session['username']}, {'$set': {'email': new_email}})
            flash('Your email has been updated.', 'success')
            return redirect(url_for('welcome'))
        return render_template('update_email.html', email=session['email'])


    @app.route('/logout')
    def logout():
        session.pop('username', None)
        flash('You have been logged out.', 'success')
        return redirect(url_for('login'))

    return app
