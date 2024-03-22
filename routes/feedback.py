from flask import Flask, render_template, request, redirect, url_for, session, flash
from pymongo import MongoClient
from hashlib import sha256
import uuid
from functools import wraps
import config
import certifi

# Connecting to MongoDB database
client = MongoClient(config.MONGO_URI, tlsCAFile=certifi.where())
db = client["gg"]
col = db["gg"]

def feedback_routes(app):
    # Decorator to check if the user is logged in
    def login_required(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'username' not in session:
                flash('Please log in to continue', 'error')
                return redirect(url_for('login'))
            return f(*args, **kwargs)
        return decorated_function

    @app.route('/add_feedback', methods=['GET', 'POST'])
    @login_required
    def add_feedback():
        """
        Endpoint to add feedback.
        """
        if request.method == 'POST':
            feedback = request.form['feedback']
            current_user = session['username']
            # Updating user's feedback in the database
            col.update_one({'username': current_user}, {'$push': {'feedback': feedback}})
            flash('Feedback added successfully.', 'success')
            return redirect(url_for('add_feedback'))
        else:
            current_user = session['username']
            user_data = col.find_one({'username': current_user})
            if user_data:
                feedback = user_data.get('feedback', [])
                feedback_enum = list(enumerate(feedback))
        return render_template('feedback.html', feedback_enum=feedback_enum)

    @app.route('/update_feedback/<int:feedback_index>', methods=['POST'])
    @login_required
    def update_feedback(feedback_index):
        """
        Endpoint to update feedback.
        """
        new_feedback = request.form['new_feedback']
        current_user = session['username']
        # Updating the specified feedback for the user in the database
        col.update_one({'username': current_user}, {'$set': {'feedback.' + str(feedback_index): new_feedback}})
        flash('Feedback updated successfully.', 'success')
        return redirect(url_for('add_feedback'))

    @app.route('/delete_feedback/<int:feedback_index>', methods=['POST'])
    @login_required
    def delete_feedback(feedback_index):
        """
        Endpoint to delete feedback.
        """
        current_user = session['username']
        # Removing the specified feedback for the user from the database
        col.update_one({'username': current_user}, {'$unset': {'feedback.' + str(feedback_index): ""}})
        col.update_one({'username': current_user}, {'$pull': {'feedback': None}})
        flash('Feedback deleted successfully.', 'success')
        return redirect(url_for('add_feedback'))
