from flask import Flask, render_template, request, redirect, url_for, session, flash
from pymongo import MongoClient
from hashlib import sha256
import uuid
from functools import wraps
import config
import certifi
import re

# Connecting to MongoDB database
client = MongoClient(config.MONGO_URI, tlsCAFile=certifi.where())
db = client["gg"]
col = db["gg"]

def billing_routes(app):
    # Decorator to check if the user is logged in
    def login_required(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'username' not in session:
                flash('Please log in to continue', 'error')
                return redirect(url_for('login'))
            return f(*args, **kwargs)
        return decorated_function

        # Function to validate card number
    def validate_card_number(card_number):
        # Card number should only contain digits and be of length 16
        return bool(re.match(r'^\d{16}$', card_number))

    # Function to validate expiry date
    def validate_expiry_date(expiry_date):
        # Expiry date should be in the format MM/YY and MM should be in range 01-12 and YY should be in range 00-99
        return bool(re.match(r'^(0[1-9]|1[0-2])\/(0[0-9]|1[0-9]|2[0-9])$', expiry_date))

    # Function to validate CVV
    def validate_cvv(cvv):
        # CVV should only contain 3 digits
        return bool(re.match(r'^\d{3}$', cvv))

    @app.route('/add_billing', methods=['GET', 'POST'])
    @login_required
    def add_billing():
        """
        Endpoint to add a billing address.
        """
        if request.method == 'POST':
            billing_address = request.form['billing_address']
            card_nickname = request.form['card_nickname']
            card_number = request.form['card_number']
            expiry_date = request.form['expiry_date']
            cvv = request.form['cvv']
            current_user = session['username']

            # Validate card number
            if not validate_card_number(card_number):
                flash('Invalid card number. Please enter a 16-digit number.', 'error')
                return redirect(url_for('add_billing'))

            # Validate expiry date
            if not validate_expiry_date(expiry_date):
                flash('Invalid expiry date. Please enter a date in the format MM/YY.', 'error')
                return redirect(url_for('add_billing'))

            # Validate CVV
            if not validate_cvv(cvv):
                flash('Invalid CVV. Please enter a 3-digit number.', 'error')
                return redirect(url_for('add_billing'))

            # Updating user's billing addresses in the database
            col.update_one(
                {'username': current_user},
                {
                    '$push': {
                        'billing_addresses': {
                            'billing_address': billing_address,
                            'card_nickname': card_nickname,
                            'card_number': card_number,
                            'expiry_date': expiry_date,
                            'cvv': cvv
                        }
                    }
                }
            )
            flash('Billing address added successfully.', 'success')
            return redirect(url_for('add_billing'))
        else:
            current_user = session['username']
            user_data = col.find_one({'username': current_user})
            if user_data:
                billing_addresses = user_data.get('billing_addresses', [])
                billing_addresses_enum = list(enumerate(billing_addresses))
        return render_template('billing.html', username=session['username'], billing_addresses_enum=billing_addresses_enum)
    
    @app.route('/update_billing/<int:billing_index>', methods=['POST'])
    @login_required
    def update_billing(billing_index):
        """
        Endpoint to update a billing address.
        """
        new_billing_address = request.form['new_billing_address' + str(billing_index)]
        new_card_nickname = request.form['new_card_nickname' + str(billing_index)]
        new_card_number = request.form['new_card_number' + str(billing_index)]
        new_expiry_date = request.form['new_expiry_date' + str(billing_index)]
        new_cvv = request.form['new_cvv' + str(billing_index)]
        current_user = session['username']

        # Validate card number
        if not validate_card_number(new_card_number):
            flash('Invalid card number. Please enter a 16-digit number.', 'error')
            return redirect(url_for('add_billing'))

        # Validate expiry date
        if not validate_expiry_date(new_expiry_date):
            flash('Invalid expiry date. Please enter a date in the format MM/YY.', 'error')
            return redirect(url_for('add_billing'))

        # Validate CVV
        if not validate_cvv(new_cvv):
            flash('Invalid CVV. Please enter a 3-digit number.', 'error')
            return redirect(url_for('add_billing'))

        # Updating the specified billing address for the user in the database
        col.update_one(
            {'username': current_user, 'billing_addresses.' + str(billing_index): {'$exists': True}},
            {
                '$set': {
                    'billing_addresses.' + str(billing_index) + '.billing_address': new_billing_address,
                    'billing_addresses.' + str(billing_index) + '.card_nickname': new_card_nickname,
                    'billing_addresses.' + str(billing_index) + '.card_number': new_card_number,
                    'billing_addresses.' + str(billing_index) + '.expiry_date': new_expiry_date,
                    'billing_addresses.' + str(billing_index) + '.cvv': new_cvv
                }
            }
        )
        flash('Billing address updated successfully.', 'success')
        return redirect(url_for('add_billing'))


    @app.route('/delete_billing/<int:billing_index>', methods=['POST'])
    @login_required
    def delete_billing(billing_index):
        """
        Endpoint to delete a billing address.
        """
        current_user = session['username']
        # Removing the specified billing address for the user from the database
        col.update_one({'username': current_user}, {'$unset': {'billing_addresses.' + str(billing_index): ""}})
        col.update_one({'username': current_user}, {'$pull': {'billing_addresses': None}})
        flash('Billing address deleted successfully.', 'success')
        return redirect(url_for('add_billing'))
