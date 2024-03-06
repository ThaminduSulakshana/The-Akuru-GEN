from flask import Flask, render_template, request, redirect, url_for, session, flash
from pymongo import MongoClient
from hashlib import sha256
import config
import certifi
import uuid
from functools import wraps


app = Flask(__name__)
app.secret_key = b'\xcc^\x91\xea\x17-\xd0W\x03\xa7\xf8J0\xac8\xc5'
app.config.from_object(config)

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

@app.route('/')
def home():
    return render_template('home.html')

from routes.user import user_routes
user_routes(app)

from routes.sub import subscribe_routes
subscribe_routes(app)

from routes.translate import translation_routes
translation_routes(app)

from routes.Qanswering import Qanswering_routes
Qanswering_routes(app)


# @app.route('/Qanswering')
# @login_required
# def Qanswering():
#     if 'subscription_level' in session and session['subscription_level'] == 'standard':
#         flash('You do not have access to Qanswering with the Standard package. Please upgrade to Premium.', 'error')
#         return redirect(url_for('subscribe'))
    
#     return render_template('Qanswering.html')

    

if __name__ == '__main__':
    app.run(debug=True)
