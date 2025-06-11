import json
import traceback
from datetime import datetime
from flask import request
import os

def get_client_info():
    """Extract client information from request"""
    try:
        ip_address = request.environ.get('HTTP_X_FORWARDED_FOR', request.environ.get('REMOTE_ADDR', 'unknown'))
        user_agent = request.headers.get('User-Agent', 'unknown')
        return ip_address, user_agent
    except:
        return 'unknown', 'unknown'

def log_audit_event(event_type, user=None, description="", error=None):
    """Log audit events to audit_log.json"""
    try:
        ip_address, device_info = get_client_info()
        
        entry = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "event_type": event_type,
            "user_id": user or "anonymous",
            "ip_address": ip_address,
            "device_info": device_info,
            "action_description": description
        }
        
        if error:
            entry["exception_type"] = type(error).__name__
            entry["stack_trace"] = traceback.format_exc()
        
        # Ensure logs directory exists
        log_dir = os.path.join(os.getcwd(), 'logs')
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        
        log_file_path = os.path.join(log_dir, 'audit_log.json')
        
        with open(log_file_path, 'a', encoding='utf-8') as log_file:
            log_file.write(json.dumps(entry) + '\n')
            
    except Exception as e:
        # Fallback logging to prevent audit logging failures from breaking the app
        print(f"Audit logging failed: {str(e)}")

def log_login_success(user_email):
    """Log successful login"""
    log_audit_event("login_success", user_email, "User successfully logged in")

def log_login_failure(user_email=None, reason="Invalid credentials"):
    """Log failed login attempt"""
    log_audit_event("login_failure", user_email, f"Login failed: {reason}")

def log_logout(user_email):
    """Log user logout"""
    log_audit_event("logout", user_email, "User logged out")

def log_error(error, user=None, context=""):
    """Log application errors"""
    description = f"Application error: {context}" if context else "Unhandled application error"
    log_audit_event("error", user, description, error)

def log_admin_access(user_email, action):
    """Log admin panel access and actions"""
    log_audit_event("admin_access", user_email, f"Admin action: {action}")

def get_audit_logs(limit=100):
    """Retrieve audit logs for admin dashboard"""
    try:
        log_file_path = os.path.join(os.getcwd(), 'logs', 'audit_log.json')
        if not os.path.exists(log_file_path):
            return []
        
        logs = []
        with open(log_file_path, 'r', encoding='utf-8') as log_file:
            for line in log_file:
                try:
                    log_entry = json.loads(line.strip())
                    logs.append(log_entry)
                except json.JSONDecodeError:
                    continue
        
        # Return most recent logs first
        return logs[-limit:] if len(logs) > limit else logs[::-1]
    except Exception as e:
        print(f"Error reading audit logs: {str(e)}")
        return []