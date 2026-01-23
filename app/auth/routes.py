from flask import render_template, redirect, url_for, flash, request, jsonify, Response
from flask_login import login_user, logout_user, login_required, current_user
from flask_jwt_extended import create_access_token
import typing
from datetime import datetime

from app.auth import auth_bp
from app.auth.admin_user import AdminUser
from config import Config


@auth_bp.route('/login', methods=['GET', 'POST'])
def login() -> typing.Union[str, 'Response']:
    """
    Render admin login page or handle login logic.
    Returns: HTML page or Redirect.
    """
    if current_user.is_authenticated:
        return redirect(url_for('auth.dashboard'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        # Verify against config (not database!)
        if Config.verify_admin(username, password):
            admin = AdminUser()
            login_user(admin, remember=True)
            flash('Login successful!', 'success')
            return redirect(url_for('auth.dashboard'))
        
        flash('Invalid credentials', 'error')
    
    return render_template('admin/login.html')


@auth_bp.route('/logout')
@login_required
def logout():
    """Logout admin."""
    logout_user()
    flash('Logged out successfully', 'success')
    return redirect(url_for('auth.login'))


@auth_bp.route('/dashboard')
@login_required
def dashboard():
    """Admin dashboard."""
    return render_template('admin/dashboard.html')


@auth_bp.route('/api/token', methods=['POST'])
def get_token():
    """Get JWT token for API access."""
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    # Verify against config
    if Config.verify_admin(username, password):
        token = create_access_token(identity='admin')
        return jsonify(access_token=token)
    
    return jsonify(error='Invalid credentials'), 401