from flask import Flask, render_template, request, redirect, url_for, session, flash
from pymongo import MongoClient
import config
from functools import wraps
import certifi
import re

# Connecting to MongoDB database
client = MongoClient(config.MONGO_URI, tlsCAFile=certifi.where())
db = client["gg"]
col = db["gg"]

def feedback_routes(app):
    def login_required(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'username' not in session:
                flash('Please log in to continue', 'error')
                return redirect(url_for('login'))
            return f(*args, **kwargs)
        return decorated_function

    def validate_email(email):
        return bool(re.match(r'^[\w.-]+@[\w.-]+\.\w+$', email))

    @app.route('/add_feedback', methods=['GET', 'POST'])
    @login_required
    def add_feedback():
        if request.method == 'POST':
            email = request.form['email']
            outcome = request.form['outcome']
            feedback_details = request.form['feedback_details']
            current_user = session['username']

            if not validate_email(email):
                flash('Invalid email format.', 'error')
                return redirect(url_for('add_feedback'))

            col.update_one({'username': current_user}, {'$push': {
                'feedback': {'email': email, 'outcome': outcome, 'details': feedback_details}
            }})
            flash('Feedback added successfully', 'success')
            return redirect(url_for('add_feedback'))
        else:
            current_user = session['username']
            user_data = col.find_one({'username': current_user})
            if user_data:
                feedback = user_data.get('feedback', [])
                feedback_enum = list(enumerate(feedback))

            all_feedback_data = col.find({}, {'username': 1, 'feedback': 1})
            all_feedback = []
            for data in all_feedback_data:
                for fb in data.get('feedback', []):
                    all_feedback.append({'username': data['username'], 'feedback': fb})

        return render_template('feedback.html', username=session['username'], feedback_enum=feedback_enum, all_feedback=all_feedback)


    @app.route('/update_feedback/<int:feedback_index>', methods=['POST'])
    @login_required
    def update_feedback(feedback_index):
        new_email = request.form['email']
        new_outcome = request.form['outcome']
        new_feedback_details = request.form['feedback_details']
        current_user = session['username']

        if not validate_email(new_email):
            flash('Invalid email format.', 'error')
            return redirect(url_for('add_feedback'))

        col.update_one({'username': current_user, 'feedback.email': new_email}, {'$set': {
            'feedback.$.outcome': new_outcome,
            'feedback.$.details': new_feedback_details
        }})
        flash('Feedback updated successfully.', 'success')
        return redirect(url_for('add_feedback'))

    @app.route('/delete_feedback/<int:feedback_index>', methods=['POST'])
    @login_required
    def delete_feedback(feedback_index):
        current_user = session['username']
        col.update_one({'username': current_user}, {'$unset': {'feedback.' + str(feedback_index): ""}})
        col.update_one({'username': current_user}, {'$pull': {'feedback': None}})
        flash('Feedback deleted successfully.', 'success')
        return redirect(url_for('add_feedback'))
    
    
