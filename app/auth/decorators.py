"""Admin authentication decorator for Flask routes."""

from functools import wraps
from flask import jsonify, redirect, url_for, request
from flask_login import current_user
from flask_jwt_extended import verify_jwt_in_request


def admin_required(f):
    """Decorator that accepts Flask-Login session OR JWT token."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Check Flask-Login session
        # current_user.is_authenticated returns False for AnonymousUser
        if hasattr(current_user, 'is_authenticated') and current_user.is_authenticated:
            # Double check it's actually our admin, not anonymous
            if hasattr(current_user, 'id') and current_user.id == 'admin':
                return f(*args, **kwargs)
        
        # Try JWT (API token)
        try:
            verify_jwt_in_request()
            return f(*args, **kwargs)
        except:
            pass
        
        # Neither worked - return appropriate error
        if request.is_json:
            return jsonify(error='Unauthorized'), 401
        return redirect(url_for('auth.login'))
    
    return decorated_function