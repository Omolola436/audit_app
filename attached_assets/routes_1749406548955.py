import os
import json
import logging
from datetime import datetime
from flask import render_template, request, redirect, url_for, session, flash, jsonify, send_file, abort
from werkzeug.utils import secure_filename
from app import app, db
from models import User, Question, Response, Submission, Category
from report_generator import generate_excel_report, generate_word_report

# Add custom Jinja filter
@app.template_filter('from_json')
def from_json_filter(value):
    """Convert JSON string to Python object"""
    if value:
        return json.loads(value)
    return []

# Initialize sample data
def init_sample_data():
    if Question.query.count() == 0:
        categories_data = [
            {"name": "Accountability and Governance", "description": "The extent to which information governance accountability, policies and procedures, performance measurement controls, and reporting mechanisms to monitor data protection compliance to NDPA is in place and in operation throughout the organization", "order_num": 1},
            {"name": "Awareness and Training", "description": "The provision and monitoring of staff data protection, records management and information security training, including awareness of data protection regulation requirements relating to their roles and responsibilities.", "order_num": 2},
            {"name": "Data Processing and Sharing", "description": "The design and operation of controls to ensure processing and sharing of personal data complies with the principles of NDPA.", "order_num": 3},
            {"name": "Administration", "description": "Managing/handling all aspects of data protection procedures, and practices digitally.", "order_num": 4},
            {"name": "Capturing", "description": "The process of collecting and acquiring data in a secure and compliant manner digitally.", "order_num": 5},
            {"name": "Actions on Security", "description": "Measures to safeguard data from unauthorized access, breaches, and misuse.", "order_num": 6}
        ]
        
        for cat_data in categories_data:
            category = Category(**cat_data)
            db.session.add(category)
        
        questions_data = [
            {"category": "Accountability and Governance", "question_text": "Is your top-management aware of the Nigeria Data Protection Act (NDPA) and the potential implications on your organization?", "question_type": "multiple_choice", "options": json.dumps(["Yes", "Partially", "No"]), "order_num": 1},
            {"category": "Accountability and Governance", "question_text": "Have you implemented any information security standard in your organization before? If YES, specify.", "question_type": "multiple_choice", "options": json.dumps(["Yes", "Partially", "No"]), "order_num": 2},
            {"category": "Accountability and Governance", "question_text": "Do you have a documented data breach incident management procedure?", "question_type": "multiple_choice", "options": json.dumps(["Yes", "Partially", "No"]), "order_num": 3},
            {"category": "Accountability and Governance", "question_text": "Do you collect and process personal information through digital mediums?", "question_type": "multiple_choice", "options": json.dumps(["Yes", "Partially", "No"]), "order_num": 4},
            {"category": "Accountability and Governance", "question_text": "Have you organized any NDPA awareness seminar for your members of staff or suppliers?", "question_type": "multiple_choice", "options": json.dumps(["Yes", "Partially", "No"]), "order_num": 5},
            {"category": "Accountability and Governance", "question_text": "Have you conducted a detailed audit of your privacy and data protection practices?", "question_type": "multiple_choice", "options": json.dumps(["Yes", "Partially", "No"]), "order_num": 6},
            
            {"category": "Awareness and Training", "question_text": "Have you provided data protection training to your staff?", "question_type": "multiple_choice", "options": json.dumps(["Yes", "Partially", "No"]), "order_num": 7},
            {"category": "Awareness and Training", "question_text": "Do your staff understand their roles and responsibilities under NDPA?", "question_type": "multiple_choice", "options": json.dumps(["Yes", "Partially", "No"]), "order_num": 8},
            {"category": "Awareness and Training", "question_text": "Do you have documented training materials for data protection? (Please upload evidence if available)", "question_type": "multiple_choice", "options": json.dumps(["Yes", "Partially", "No"]), "requires_file": False, "order_num": 9},
            
            {"category": "Data Processing and Sharing", "question_text": "Do you have documented procedures for data processing activities?", "question_type": "multiple_choice", "options": json.dumps(["Yes", "Partially", "No"]), "order_num": 10},
            {"category": "Data Processing and Sharing", "question_text": "Do you obtain proper consent before processing personal data?", "question_type": "multiple_choice", "options": json.dumps(["Yes", "Partially", "No"]), "order_num": 11},
            {"category": "Data Processing and Sharing", "question_text": "Do you have controls in place for data sharing with third parties?", "question_type": "multiple_choice", "options": json.dumps(["Yes", "Partially", "No"]), "order_num": 12},
            
            {"category": "Administration", "question_text": "Do you have digital systems for managing data protection compliance?", "question_type": "multiple_choice", "options": json.dumps(["Yes", "Partially", "No"]), "order_num": 13},
            {"category": "Administration", "question_text": "Are your data protection procedures documented digitally?", "question_type": "multiple_choice", "options": json.dumps(["Yes", "Partially", "No"]), "order_num": 14},
            
            {"category": "Capturing", "question_text": "Do you have secure methods for collecting personal data?", "question_type": "multiple_choice", "options": json.dumps(["Yes", "Partially", "No"]), "order_num": 15},
            {"category": "Capturing", "question_text": "Do you validate data accuracy during collection?", "question_type": "multiple_choice", "options": json.dumps(["Yes", "Partially", "No"]), "order_num": 16},
            
            {"category": "Actions on Security", "question_text": "Do you have access controls in place for personal data?", "question_type": "multiple_choice", "options": json.dumps(["Yes", "Partially", "No"]), "order_num": 17},
            {"category": "Actions on Security", "question_text": "Do you have incident response procedures for data breaches? (Please upload evidence if available)", "question_type": "multiple_choice", "options": json.dumps(["Yes", "Partially", "No"]), "requires_file": False, "order_num": 18}
        ]
        
        for q_data in questions_data:
            question = Question(**q_data)
            db.session.add(question)
        
        db.session.commit()
        logging.info("Sample data initialized")

# Initialize sample data on startup
with app.app_context():
    init_sample_data()

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    email = request.form.get('email')
    company_name = request.form.get('company_name')
    
    if not email or not company_name:
        flash('Email and Company Name are required', 'error')
        return redirect(url_for('index'))
    
    # Create or get user
    user = User.query.filter_by(email=email, company_name=company_name).first()
    if not user:
        user = User(email=email, company_name=company_name)
        db.session.add(user)
        db.session.commit()
    
    session['user_id'] = user.id
    session['current_question'] = 1
    
    # Get first category
    first_category = Category.query.order_by(Category.order_num).first()
    return redirect(url_for('category_intro', category_name=first_category.name))

@app.route('/category/<category_name>')
def category_intro(category_name):
    if 'user_id' not in session:
        return redirect(url_for('index'))
    
    category = Category.query.filter_by(name=category_name).first_or_404()
    return render_template('category_intro.html', category=category)

@app.route('/question/<int:question_id>')
def question(question_id):
    if 'user_id' not in session:
        return redirect(url_for('index'))
    
    question = Question.query.get_or_404(question_id)
    user_id = session['user_id']
    
    # Get existing response if any
    existing_response = Response.query.filter_by(user_id=user_id, question_id=question_id).first()
    
    # Get total questions and current position for progress
    total_questions = Question.query.count()
    current_position = question.order_num
    
    # Get previous and next questions
    prev_question = Question.query.filter(Question.order_num < question.order_num).order_by(Question.order_num.desc()).first()
    next_question = Question.query.filter(Question.order_num > question.order_num).order_by(Question.order_num).first()
    
    return render_template('question.html', 
                         question=question, 
                         existing_response=existing_response,
                         total_questions=total_questions,
                         current_position=current_position,
                         prev_question=prev_question,
                         next_question=next_question)

@app.route('/submit_answer', methods=['POST'])
def submit_answer():
    if 'user_id' not in session:
        return redirect(url_for('index'))
    
    user_id = session['user_id']
    question_id = request.form.get('question_id')
    answer = request.form.get('answer')
    comment = request.form.get('comment', '')
    
    if not answer:
        flash('Please select an answer', 'error')
        return redirect(url_for('question', question_id=question_id))
    
    # Handle file upload
    file_path = None
    if 'file' in request.files:
        file = request.files['file']
        if file and file.filename:
            filename = secure_filename(file.filename)
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_')
            filename = timestamp + filename
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
    
    # Save or update response
    existing_response = Response.query.filter_by(user_id=user_id, question_id=question_id).first()
    if existing_response:
        existing_response.answer = answer
        existing_response.comment = comment
        if file_path:
            existing_response.file_path = file_path
    else:
        response = Response(
            user_id=user_id,
            question_id=question_id,
            answer=answer,
            comment=comment,
            file_path=file_path
        )
        db.session.add(response)
    
    db.session.commit()
    
    # Navigate to next question or finish
    current_question = Question.query.get(question_id)
    next_question = Question.query.filter(Question.order_num > current_question.order_num).order_by(Question.order_num).first()
    
    if next_question:
        # Check if we're moving to a new category
        if next_question.category != current_question.category:
            category = Category.query.filter_by(name=next_question.category).first()
            return redirect(url_for('category_intro', category_name=category.name))
        else:
            return redirect(url_for('question', question_id=next_question.id))
    else:
        return redirect(url_for('submit_audit'))

@app.route('/start_category/<category_name>')
def start_category(category_name):
    if 'user_id' not in session:
        return redirect(url_for('index'))
    
    # Get first question in this category
    first_question = Question.query.filter_by(category=category_name).order_by(Question.order_num).first()
    if first_question:
        return redirect(url_for('question', question_id=first_question.id))
    else:
        return redirect(url_for('submit_audit'))

@app.route('/submit_audit')
def submit_audit():
    if 'user_id' not in session:
        return redirect(url_for('index'))
    
    user_id = session['user_id']
    user = User.query.get(user_id)
    
    # Generate reports
    try:
        excel_path = generate_excel_report(user_id)
        word_path = generate_word_report(user_id)
        
        # Save submission record
        submission = Submission(
            user_id=user_id,
            excel_path=excel_path,
            word_report_path=word_path
        )
        db.session.add(submission)
        db.session.commit()
        
        # Clear session
        session.clear()
        
        return render_template('thank_you.html', user=user)
        
    except Exception as e:
        logging.error(f"Error generating reports: {str(e)}")
        flash('Error generating reports. Please try again.', 'error')
        return redirect(url_for('question', question_id=1))

@app.route('/admin')
def admin_login():
    return render_template('admin_login.html')

@app.route('/admin/login', methods=['POST'])
def admin_authenticate():
    username = request.form.get('username')
    password = request.form.get('password')
    
    # Simple admin authentication (in production, use proper authentication)
    if username == 'admin' and password == 'admin123':
        session['admin'] = True
        return redirect(url_for('admin_dashboard'))
    else:
        flash('Invalid credentials', 'error')
        return redirect(url_for('admin_login'))

@app.route('/admin/dashboard')
def admin_dashboard():
    if not session.get('admin'):
        return redirect(url_for('admin_login'))
    
    submissions = db.session.query(Submission, User).join(User).order_by(Submission.submitted_at.desc()).all()
    return render_template('admin_dashboard.html', submissions=submissions)

@app.route('/admin/download/<int:submission_id>/<file_type>')
def download_file(submission_id, file_type):
    if not session.get('admin'):
        return redirect(url_for('admin_login'))
    
    submission = Submission.query.get_or_404(submission_id)
    
    if file_type == 'excel' and submission.excel_path:
        return send_file(submission.excel_path, as_attachment=True)
    elif file_type == 'word' and submission.word_report_path:
        return send_file(submission.word_report_path, as_attachment=True)
    else:
        abort(404)

@app.route('/admin/logout')
def admin_logout():
    session.pop('admin', None)
    return redirect(url_for('admin_login'))

# Error handlers
@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500
