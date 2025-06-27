from datetime import datetime
from app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), nullable=False)
    company_name = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    responses = db.relationship('Response', backref='user', lazy=True, cascade='all, delete-orphan')
    submissions = db.relationship('Submission', backref='user', lazy=True, cascade='all, delete-orphan')

class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(100), nullable=False)
    question_text = db.Column(db.Text, nullable=False)
    question_type = db.Column(db.String(50), nullable=False)  # 'multiple_choice', 'file_upload'
    options = db.Column(db.Text)  # JSON string for multiple choice options
    requires_file = db.Column(db.Boolean, default=False)
    order_num = db.Column(db.Integer, nullable=False)
    
    # Relationships
    responses = db.relationship('Response', backref='question', lazy=True)

class Response(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'), nullable=False)
    answer = db.Column(db.Text)
    comment = db.Column(db.Text)
    file_path = db.Column(db.String(500))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Submission(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    excel_path = db.Column(db.String(500))
    word_report_path = db.Column(db.String(500))
    submitted_at = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(50), default='completed')
    uploaded_admin_pdf_path = db.Column(db.String(500))  # Path to uploaded PDF

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.Text)
    order_num = db.Column(db.Integer, nullable=False)

class AuditLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    event_type = db.Column(db.String(100), nullable=False)
    user = db.Column(db.String(200))
    ip_address = db.Column(db.String(100))
    description = db.Column(db.Text, nullable=False)