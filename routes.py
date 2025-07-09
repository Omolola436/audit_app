import os
import json
import logging
from datetime import datetime
from flask import render_template, request, redirect, url_for, flash, session, send_file, abort
from werkzeug.utils import secure_filename
from app import app, db
from urllib.parse import unquote
from urllib.parse import quote
from models import User, Question, Response, Submission, Category
from report_generator import generate_excel_report, generate_word_report
from audit_logger import (log_login_success, log_login_failure, log_logout, log_admin_access, 
                        log_file_uploaded, log_questionnaire_submitted, log_audit_score_generated,
                        log_unauthorized_access, log_form_submission_failed, log_internal_server_error,
                        log_file_upload_error, get_audit_logs)

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'doc', 'docx'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        company_name = request.form['company_name']
        
        try:
            # Check if user exists, if not create new user
            user = User.query.filter_by(email=email, company_name=company_name).first()
            if not user:
                user = User(email=email, company_name=company_name)
                db.session.add(user)
                db.session.commit()
            
            # Store user info in session
            session['user_id'] = user.id
            session['email'] = user.email
            session['company_name'] = user.company_name
            log_login_success(email)
        except Exception as e:
            log_internal_server_error(email, e, "User login process")
            flash('An error occurred during login. Please try again.', 'error')
            return render_template('login.html')
        
        # Get first category
        first_category = Category.query.order_by(Category.order_num).first()
        if first_category:
            return redirect(f"/category/{quote(first_category.name)}")
        else:
            flash('No questions available. Please contact administrator.', 'error')
            return redirect(url_for('index'))
    
    return render_template('login.html')

@app.route('/category/<category_name>')
def category_intro(category_name):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    # Decode URL-encoded name
    decoded_name = unquote(category_name)
    category = Category.query.filter_by(name=decoded_name).first()
    
    if not category:
        abort(404)
    
    return render_template('category_intro.html', category=category)

@app.route('/start/<category_name>')
def start_category(category_name):
    if 'user_id' not in session:
        return redirect(url_for('login'))

    decoded_name = unquote(category_name)
    question = Question.query.filter_by(category=decoded_name).order_by(Question.order_num).first()
    if question:
        return redirect(url_for('question', question_id=question.id))
    else:
        flash('No questions found for this category.', 'error')
        return redirect(url_for('index'))

@app.route('/question/<int:question_id>')
def question(question_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    question = Question.query.get_or_404(question_id)
    user_id = session['user_id']
    
    # Get existing response if any
    existing_response = Response.query.filter_by(user_id=user_id, question_id=question_id).first()
    
    # Get total questions count and current position
    total_questions = Question.query.count()
    current_position = Question.query.filter(Question.order_num <= question.order_num).count()
    
    # Get next and previous questions
    next_question = Question.query.filter(Question.order_num > question.order_num).order_by(Question.order_num).first()
    prev_question = Question.query.filter(Question.order_num < question.order_num).order_by(Question.order_num.desc()).first()
    
    return render_template('question.html', 
                         question=question, 
                         existing_response=existing_response,
                         total_questions=total_questions,
                         current_position=current_position,
                         next_question=next_question,
                         prev_question=prev_question)

@app.route('/submit_answer', methods=['POST'])
def submit_answer():
    if 'user_id' not in session:
        log_unauthorized_access(None, "/submit_answer", "POST")
        return redirect(url_for('login'))
    
    try:
        user_id = session['user_id']
        user_email = session.get('email')
        question_id = request.form.get('question_id')
        answer = request.form.get('answer', '')
        comment = request.form.get('comment', '')
        
        if not question_id:
            log_form_submission_failed(user_email, "Missing question ID")
            flash('Invalid form submission', 'error')
            return redirect(url_for('index'))
        
        question = Question.query.get_or_404(question_id)
        
        # Handle file upload
        file_path = None
        if 'file' in request.files:
            file = request.files['file']
            if file and file.filename and file.filename != '':
                if allowed_file(file.filename):
                    try:
                        filename = secure_filename(file.filename)
                        # Add timestamp to avoid conflicts
                        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_')
                        filename = timestamp + filename
                        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                        file.save(file_path)
                        log_file_uploaded(user_email, filename)
                    except Exception as e:
                        log_file_upload_error(user_email, file.filename, str(e))
                        flash('File upload failed. Please try again.', 'error')
                        return redirect(url_for('question', question_id=question_id))
                else:
                    log_file_upload_error(user_email, file.filename, "File type not supported")
                    flash('File type not supported', 'error')
                    return redirect(url_for('question', question_id=question_id))
        
        # Check if response already exists
        existing_response = Response.query.filter_by(user_id=user_id, question_id=question_id).first()
        
        if existing_response:
            # Update existing response
            existing_response.answer = answer
            existing_response.comment = comment
            if file_path:
                existing_response.file_path = file_path
        else:
            # Create new response
            response = Response(
                user_id=user_id,
                question_id=question_id,
                answer=answer,
                comment=comment,
                file_path=file_path
            )
            db.session.add(response)
        
        db.session.commit()
        
        # Get next question
        next_question = Question.query.filter(Question.order_num > question.order_num).order_by(Question.order_num).first()
        
        if next_question:
            # Check if we're moving to a new category
            if next_question.category != question.category:
                return redirect(url_for('category_intro', category_name=next_question.category))
            else:
                return redirect(url_for('question', question_id=next_question.id))
        else:
            # All questions completed, generate reports and redirect to thank you page
            return redirect(url_for('complete_audit'))
            
    except Exception as e:
        log_internal_server_error(session.get('email'), e, "Answer submission")
        flash('An error occurred while submitting your answer. Please try again.', 'error')
        return redirect(url_for('question', question_id=question_id) if 'question_id' in locals() else url_for('index'))

@app.route('/complete_audit')
def complete_audit():
    if 'user_id' not in session:
        log_unauthorized_access(None, "/complete_audit", "GET")
        return redirect(url_for('login'))
    
    user_id = session['user_id']
    user = User.query.get(user_id)
    
    try:
        # Log questionnaire submission
        log_questionnaire_submitted(user.email)
        
        # Generate reports
        excel_path = generate_excel_report(user_id)
        word_path = generate_word_report(user_id)
        
        # Create submission record
        submission = Submission(
            user_id=user_id,
            excel_path=excel_path,
            word_report_path=word_path,
            status='completed'
        )
        db.session.add(submission)
        db.session.commit()
        
        # Log audit score generation
        log_audit_score_generated(user.email, user.company_name)
        
        logging.info(f"Reports generated for user {user.email}: Excel: {excel_path}, Word: {word_path}")
        
    except Exception as e:
        log_internal_server_error(user.email if user else None, e, "Report generation")
        logging.error(f"Error generating reports for user {user.email if user else 'unknown'}: {str(e)}")
        flash('There was an error generating your reports. Please contact support.', 'error')
    
    return render_template('thank_you.html', user=user, 
                         EMAILJS_PUBLIC_KEY=os.environ.get('EMAILJS_PUBLIC_KEY'),
                         EMAILJS_SERVICE_ID=os.environ.get('EMAILJS_SERVICE_ID'),
                         EMAILJS_TEMPLATE_ID=os.environ.get('EMAILJS_TEMPLATE_ID'))

@app.route('/admin')
def admin_login():
    return render_template('admin_login.html')

@app.route('/admin/authenticate', methods=['POST'])
def admin_authenticate():
    username = request.form['username']
    password = request.form['password']
    
    # Simple admin authentication
    if username == 'admin' and password == 'admin123':
        session['admin_logged_in'] = True
        log_admin_access(username, "Admin login successful")
        return redirect(url_for('admin_dashboard'))
    else:
        log_login_failure(username, "Invalid admin credentials")
        flash('Invalid credentials', 'error')
        return redirect(url_for('admin_login'))

@app.route('/admin/dashboard')
def admin_dashboard():
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))
    
    # Get all submissions with user information and their uploaded files
    submissions_data = []
    submissions = db.session.query(Submission, User).join(User).order_by(Submission.submitted_at.desc()).all()
    
    # Debug: Log submission count
    logging.info(f"Found {len(submissions)} submissions in database")
    
    for submission, user in submissions:
        # Get all uploaded files for this user
        user_files = db.session.query(Response).filter(
            Response.user_id == user.id,
            Response.file_path.isnot(None)
        ).all()
        
        logging.info(f"User {user.email} has {len(user_files)} uploaded files")
        
        submissions_data.append({
            'submission': submission,
            'user': user,
            'uploaded_files': user_files
        })
    
    # Calculate stats
    total_submissions = len(submissions_data)
    unique_companies = len(set([user.company_name for submission, user in submissions])) if submissions else 0
    
    # Get recent audit logs
    audit_logs = get_audit_logs(50)
    
    log_admin_access("admin", "Accessed admin dashboard")
    
    return render_template('admin_dashboard.html', 
                         submissions_data=submissions_data, 
                         total_submissions=total_submissions,
                         unique_companies=unique_companies,
                         audit_logs=audit_logs)

@app.route('/admin/logout')
def admin_logout():
    session.pop('admin_logged_in', None)
    return redirect(url_for('admin_login'))

@app.route('/download/<int:submission_id>/<file_type>')
def download_file(submission_id, file_type):
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))
    
    submission = Submission.query.get_or_404(submission_id)
    user = User.query.get(submission.user_id)
    
    if file_type == 'excel' and submission.excel_path:
        if os.path.exists(submission.excel_path):
            # Use company name with safe characters for filename
            safe_company_name = user.company_name.replace(' ', '_').replace('/', '_').replace('\\', '_')
            return send_file(submission.excel_path, 
                           as_attachment=True,
                           download_name=f"{safe_company_name}_audit_responses.xlsx")
    elif file_type == 'word' and submission.word_report_path:
        if os.path.exists(submission.word_report_path):
            # Use company name with safe characters for filename
            safe_company_name = user.company_name.replace(' ', '_').replace('/', '_').replace('\\', '_')
            return send_file(submission.word_report_path,
                           as_attachment=True,
                           download_name=f"{safe_company_name}_audit_report.docx")
    
    flash('File not found', 'error')
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/upload', methods=['POST'])
def upload_pdf():
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))

    if 'pdf_file' not in request.files or 'submission_id' not in request.form:
        flash('Invalid upload request.', 'error')
        return redirect(url_for('admin_dashboard'))

    file = request.files['pdf_file']
    submission_id = request.form['submission_id']

    if file.filename == '':
        flash('No file selected.', 'error')
        return redirect(url_for('admin_dashboard'))

    if file and file.filename.lower().endswith('.pdf'):
        filename = secure_filename(f"{submission_id}_{file.filename}")
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        # Optional: Save PDF path to database if you have a column
        submission = Submission.query.get(submission_id)
        if submission:
            submission.uploaded_admin_pdf_path = filepath  # Make sure this column exists
            db.session.commit()

        flash('PDF uploaded successfully.', 'success')
    else:
        flash('Only PDF files are allowed.', 'error')

    return redirect(url_for('admin_dashboard'))

@app.route('/download/admin-pdf/<int:submission_id>')
def download_admin_pdf(submission_id):
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))

    submission = Submission.query.get_or_404(submission_id)

    if submission.uploaded_admin_pdf_path and os.path.exists(submission.uploaded_admin_pdf_path):
        filename = os.path.basename(submission.uploaded_admin_pdf_path)
        return send_file(submission.uploaded_admin_pdf_path, as_attachment=True, download_name=filename)

    flash('Uploaded PDF not found.', 'error')
    return redirect(url_for('admin_dashboard'))

@app.route('/download/user-file/<int:response_id>')
def download_user_file(response_id):
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))
    
    response = Response.query.get_or_404(response_id)
    
    if response.file_path and os.path.exists(response.file_path):
        # Get original filename from path
        filename = os.path.basename(response.file_path)
        return send_file(response.file_path, as_attachment=True, download_name=filename)
    
    flash('File not found', 'error')
    return redirect(url_for('admin_dashboard'))

@app.template_filter('from_json')
def from_json_filter(value):
    try:
        return json.loads(value) if value else []
    except:
        return []

@app.context_processor
def utility_processor():
    return dict(enumerate=enumerate)
