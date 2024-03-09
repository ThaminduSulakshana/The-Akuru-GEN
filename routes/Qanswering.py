from flask import render_template, request, redirect, url_for, session, flash
from pymongo import MongoClient
from hashlib import sha256
import uuid
from functools import wraps
import config
import certifi
import pickle

client = MongoClient(config.MONGO_URI, tlsCAFile=certifi.where())
db = client["gg"]
col = db["gg"]

# Load the question-answering pipeline from the pickle file
with open('models/question_answerer_pipeline.pkl', 'rb') as model_file:
    question_answerer = pickle.load(model_file)

def Qanswering_routes(app):

    # Decorator to check if the user is logged in
    def login_required(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'username' not in session:
                flash('Please log in to continue', 'error')
                return redirect(url_for('login'))
            return f(*args, **kwargs)
        return decorated_function

    @app.route('/Qanswering')
    @login_required
    def Qanswering():
        if 'subscription_level' in session and session['subscription_level'] == 'standard':
            flash('You do not have access to Qanswering with the Standard package. Please upgrade to Premium.', 'error')
            return redirect(url_for('subscribe'))

        return render_template('Qanswering.html')

    @app.route('/answer', methods=['POST'])
    def answer():
        context = request.form['context']
        question = request.form['question']

        # Use the question-answering pipeline to get the answer
        answer = question_answerer(question=question, context=context)

        return render_template('Qanswering.html', context=context, question=question, answer=answer['answer'])
