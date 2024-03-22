from flask import render_template, request, redirect, url_for, session, flash
from pymongo import MongoClient
from hashlib import sha256
import uuid
from functools import wraps
import config
import certifi

# Connecting to MongoDB
client = MongoClient(config.MONGO_URI, tlsCAFile=certifi.where())
db = client["gg"]
col = db["gg"]

def subscribe_routes(app):
    # Decorator to check if the user is logged in
    def login_required(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'username' not in session:
                flash('Please log in to continue', 'error')
                return redirect(url_for('login'))
            return f(*args, **kwargs)
        return decorated_function

    @app.route('/subscribe', methods=['GET', 'POST'])
    @login_required
    def subscribe():
        """
        Endpoint for subscribing to different packages.
        """
        if request.method == 'POST':
            subscription_level = request.form.get('subscription_level')

            # Check if the selected subscription level is valid
            if subscription_level in {'free', 'standard', 'premium'}:
                # Update the user's subscription level in the database
                username = session['username']
                col.update_one({'username': username}, {'$set': {'subscription_level': subscription_level}})
                
                # Update session data with the new subscription level
                session['subscription_level'] = subscription_level
                flash(f'You have subscribed to the {subscription_level.capitalize()} package.', 'success')

            return redirect(url_for('subscribe'))
        
        # Render the subscription page with default subscription set to 'free'
        return render_template('subscribe.html', default_subscription='free')
