import os
import json
import logging
from datetime import datetime
from flask import render_template, request, redirect, url_for, flash, session, send_file, abort
from werkzeug.utils import secure_filename
from app import app, db
from models import User, Question, Response, Submission, Category
from report_generator import generate_excel_report, generate_word_report

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
        
        # Get first category
        first_category = Category.query.order_by(Category.order_num).first()
        if first_category:
            return redirect(url_for('category_intro', category_name=first_category.name))
        else:
            flash('No questions available. Please contact administrator.', 'error')
            return redirect(url_for('index'))
    
    return render_template('login.html')

@app.route('/category/<category_name>')
def category_intro(category_name):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    category = Category.query.filter_by(name=category_name).first()
    if not category:
        abort(404)
    
    return render_template('category_intro.html', category=category)

@app.route('/start/<category_name>')
def start_category(category_name):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    # Get first question in this category
    question = Question.query.filter_by(category=category_name).order_by(Question.order_num).first()
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
        return redirect(url_for('login'))
    
    user_id = session['user_id']
    question_id = request.form['question_id']
    answer = request.form.get('answer', '')
    comment = request.form.get('comment', '')
    
    question = Question.query.get_or_404(question_id)
    
    # Handle file upload
    file_path = None
    if 'file' in request.files:
        file = request.files['file']
        if file and file.filename != '' and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            # Add timestamp to avoid conflicts
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_')
            filename = timestamp + filename
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
    
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

@app.route('/complete_audit')
def complete_audit():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    user_id = session['user_id']
    user = User.query.get(user_id)
    
    try:
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
        
        logging.info(f"Reports generated for user {user.email}: Excel: {excel_path}, Word: {word_path}")
        
    except Exception as e:
        logging.error(f"Error generating reports for user {user.email}: {str(e)}")
        flash('There was an error generating your reports. Please contact support.', 'error')
    
    return render_template('thank_you.html', user=user)

@app.route('/admin')
def admin_login():
    return render_template('admin_login.html')

@app.route('/admin/authenticate', methods=['POST'])
def admin_authenticate():
    username = request.form['username']
    password = request.form['password']
    
    # Simple admin authentication
    if username == 'admin' and password == 'password123':
        session['admin_logged_in'] = True
        return redirect(url_for('admin_dashboard'))
    else:
        flash('Invalid credentials', 'error')
        return redirect(url_for('admin_login'))

@app.route('/admin/dashboard')
def admin_dashboard():
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))
    
    # Get all submissions with user information
    submissions = db.session.query(Submission, User).join(User).order_by(Submission.submitted_at.desc()).all()
    
    return render_template('admin_dashboard.html', submissions=submissions)

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
            return send_file(submission.excel_path, 
                           as_attachment=True,
                           download_name=f"{user.company_name}_audit_responses.xlsx")
    elif file_type == 'word' and submission.word_report_path:
        if os.path.exists(submission.word_report_path):
            return send_file(submission.word_report_path,
                           as_attachment=True,
                           download_name=f"{user.company_name}_audit_report.docx")
    
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
