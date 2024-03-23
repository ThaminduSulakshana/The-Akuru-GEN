from flask import Flask, render_template, request, redirect, url_for, session, flash
from pymongo import MongoClient
from hashlib import sha256
import config
import certifi
import uuid
from functools import wraps

# Create Flask app instance
app = Flask(__name__)
app.secret_key = b'\xcc^\x91\xea\x17-\xd0W\x03\xa7\xf8J0\xac8\xc5'  # Secret key for session management
app.config.from_object(config)  # Load configurations

# Connect to MongoDB database
client = MongoClient(config.MONGO_URI, tlsCAFile=certifi.where())
db = client["gg"]
col = db["gg"]

# Decorator to check if the user is logged in
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            flash('Please log in to continue', 'error')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# Home route
@app.route('/')
def home():
    return render_template('home.html')

# Import user-related routes
from routes.user import user_routes
user_routes(app)

# Import subscription-related routes
from routes.sub import subscribe_routes
subscribe_routes(app)

# Import translation-related routes
from routes.translate import translation_routes
translation_routes(app)

# Import question answering-related routes
from routes.Qanswering import Qanswering_routes
Qanswering_routes(app)

# Import billing-related routes
from routes.billing import billing_routes
billing_routes(app)

# Import feedback-related routes
from routes.feedback import feedback_routes
feedback_routes(app)


if __name__ == '__main__':
    app.run(debug=True, port=5000)
