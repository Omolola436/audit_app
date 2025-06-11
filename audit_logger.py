import traceback
from datetime import datetime
from flask import request

def get_client_ip():
    """Extract client IP address from request"""
    try:
        # Check for forwarded IP first (proxy/load balancer)
        forwarded_for = request.environ.get('HTTP_X_FORWARDED_FOR')
        if forwarded_for:
            # X-Forwarded-For can contain multiple IPs, get the first one
            public_ip = forwarded_for.split(',')[0].strip()
        else:
            public_ip = request.environ.get('REMOTE_ADDR', 'unknown')
        
        # Get internal IP
        internal_ip = request.environ.get('REMOTE_ADDR', 'unknown')
        
        # Combine both if different
        if public_ip != internal_ip and forwarded_for:
            return f"{public_ip}, {internal_ip}"
        else:
            return public_ip
    except:
        return 'unknown'

def log_audit_event(event_type, user=None, description="", error=None):
    """Log audit events to database"""
    try:
        from app import db
        from models import AuditLog
        
        ip_address = get_client_ip()
        
        # If error occurred, include error details in description
        if error:
            error_details = f" - Error: {type(error).__name__}: {str(error)}"
            description = description + error_details
        
        audit_log = AuditLog(
            event_type=event_type,
            user=user or "anonymous",
            ip_address=ip_address,
            description=description
        )
        
        db.session.add(audit_log)
        db.session.commit()
            
    except Exception as e:
        # Fallback logging to prevent audit logging failures from breaking the app
        print(f"Audit logging failed: {str(e)}")

# Success Events
def log_login_success(user_email):
    """Log successful login"""
    log_audit_event("Login Success", user_email, "User successfully logged in")

def log_admin_access(user_email, action="Admin login successful"):
    """Log admin panel access and actions"""
    log_audit_event("Admin Access", user_email, action)

def log_logout(user_email):
    """Log user logout"""
    log_audit_event("Logout", user_email, "User logged out")

def log_file_uploaded(user_email, filename):
    """Log file upload"""
    log_audit_event("File Uploaded", user_email, f"File uploaded: {filename}")

def log_questionnaire_submitted(user_email):
    """Log questionnaire submission"""
    log_audit_event("Questionnaire Submitted", user_email, "User completed and submitted questionnaire")

def log_audit_score_generated(user_email, company_name):
    """Log audit score generation"""
    log_audit_event("Audit Score Generated", user_email, f"Audit reports generated for {company_name}")

# Error Events
def log_login_failure(user_email=None, reason="Invalid credentials"):
    """Log failed login attempt"""
    log_audit_event("Login Failed", user_email, f"Login failed: {reason}")

def log_unauthorized_access(user_email=None, endpoint="", method=""):
    """Log unauthorized access attempt"""
    description = f"Unauthorized access attempt to {endpoint}"
    if method:
        description += f" using {method}"
    log_audit_event("Unauthorized Access Attempt", user_email, description)

def log_form_submission_failed(user_email=None, reason="Validation error"):
    """Log form submission failure"""
    log_audit_event("Form Submission Failed", user_email, f"Form submission failed: {reason}")

def log_internal_server_error(user_email=None, error=None, context=""):
    """Log internal server errors"""
    description = f"Internal server error: {context}" if context else "Internal server error occurred"
    log_audit_event("Internal Server Error", user_email, description, error)

def log_file_upload_error(user_email=None, filename="", reason=""):
    """Log file upload errors"""
    description = f"File upload failed"
    if filename:
        description += f" for {filename}"
    if reason:
        description += f": {reason}"
    log_audit_event("File Upload Error", user_email, description)

def get_audit_logs(limit=100):
    """Retrieve audit logs from database for admin dashboard"""
    try:
        from app import db
        from models import AuditLog
        
        logs = AuditLog.query.order_by(AuditLog.timestamp.desc()).limit(limit).all()
        
        # Convert to dictionary format for template compatibility
        log_list = []
        for log in logs:
            log_dict = {
                'timestamp': log.timestamp.isoformat(),
                'event_type': log.event_type,
                'user_id': log.user,
                'ip_address': log.ip_address,
                'action_description': log.description
            }
            log_list.append(log_dict)
        
        return log_list
    except Exception as e:
        print(f"Error reading audit logs: {str(e)}")
        return []