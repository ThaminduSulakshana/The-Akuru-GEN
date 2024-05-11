from flask import Flask, render_template, request, redirect, url_for, session, flash, Response 
from pymongo import MongoClient
import config
from functools import wraps
import certifi
import re
import os
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader

# Connecting to MongoDB database
client = MongoClient(config.MONGO_URI, tlsCAFile=certifi.where())
db = client["gg"]
col = db["gg"]

def generate_pdf(feedback_data):
    # Create a PDF document
    pdf_filename = "feedback_details.pdf"
    c = canvas.Canvas(pdf_filename)

    
    # Get the absolute path to the image
    img_path = os.path.join(os.getcwd(), 'static', 'img', 'nav-logo.png')

    # Load and place the image in the PDF (centered at the top)
    img = ImageReader(img_path)
    img_width, img_height = img.getSize()
    # Increase the image size by scaling factor (e.g., 2.0 for doubling size)
    scale_factor = 0.5
    new_width = img_width * scale_factor
    new_height = img_height * scale_factor
    center_x = (letter[0] - new_width) / 2
    c.drawImage(img, center_x, letter[1] - new_height - 20, width=new_width, height=new_height)

    # Draw dividing line
    c.setStrokeColorRGB(0, 0, 0)  # Black color for the line
    img_line_y = letter[1] - new_height - 20  # Position the line just below the image
    c.line(50, img_line_y, letter[0] - 50, img_line_y)

    # Starting y position for user details below the line
    y_position = img_line_y - 50  # Adjust vertical spacing here

    # Set font and font size for user details
    c.setFont("Helvetica-Bold", 16)
    c.drawString(100, y_position, "User Feedback Report")
    y_position -= 40
    
    c.setFont("Helvetica", 12)
     # Starting y position
    for feedback in feedback_data:
        c.drawString(100, y_position, f"Email: {feedback['email']}")
        c.drawString(100, y_position - 20, f"Outcome: {feedback['outcome']}")
        c.drawString(100, y_position - 40, f"Details: {feedback['details']}")
        y_position -= 120  # Adjust y position for next feedback
    
    c.save()
    return pdf_filename

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
    
    @app.route('/download_feedback_pdf')
    @login_required
    def download_feedback_pdf():
        current_user = session['username']
        user_data = col.find_one({'username': current_user})
        
        if user_data:
            feedback_data = user_data.get('feedback', [])
            pdf_filename = generate_pdf(feedback_data)
            
            # Serve the PDF file for download
            with open(pdf_filename, 'rb') as pdf_file:
                pdf_content = pdf_file.read()
                response = Response(pdf_content, mimetype='application/pdf')
                response.headers['Content-Disposition'] = f'attachment; filename={pdf_filename}'
                return response
        else:
            flash('Error generating PDF.', 'error')
            return redirect(url_for('add_feedback'))
