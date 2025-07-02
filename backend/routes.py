# routes.py

from flask import render_template, request, redirect, url_for, flash, session, jsonify, Blueprint
from datetime import datetime
from werkzeug.security import generate_password_hash
from auth import authenticate_user, get_current_user, role_required
from supabase import create_client
import os

bp = Blueprint('main', __name__)

supabase_url = os.getenv("SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_KEY")
supabase = create_client(supabase_url, supabase_key)

@bp.route('/')
def index():
    if not session.get('user_id'):
        return redirect(url_for('main.login'))

    user = get_current_user()
    if user:
        if user['role'] == 'admin':
            return redirect(url_for('main.admin_dashboard'))
        elif user['role'] == 'manager':
            return redirect(url_for('main.manager_dashboard'))
        else:
            return redirect(url_for('main.employee_dashboard'))

    session.clear()
    return redirect(url_for('main.login'))

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        if not email or not password:
            flash('Please provide both email and password', 'danger')
            return redirect(url_for('main.login'))

        user = authenticate_user(email, password)
        if user:
            session['user_id'] = user['id']
            session['user_role'] = user['role']
            flash(f"Welcome, {user['full_name']}!", 'success')

            if user['role'] == 'admin':
                return redirect(url_for('main.admin_dashboard'))
            elif user['role'] == 'manager':
                return redirect(url_for('main.manager_dashboard'))
            else:
                return redirect(url_for('main.employee_dashboard'))
        else:
            flash('Invalid email or password', 'danger')
            return redirect(url_for('main.login'))

    return render_template('login.html')

@bp.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out successfully.', 'info')
    return redirect(url_for('main.login'))

@bp.context_processor
def inject_user():
    return {'current_user': get_current_user()}
