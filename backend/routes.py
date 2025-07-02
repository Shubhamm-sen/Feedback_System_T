from flask import render_template, request, redirect, url_for, flash, session, jsonify, Blueprint
from datetime import datetime
from werkzeug.security import generate_password_hash
from auth import authenticate_user, get_current_user, role_required
from supabase import create_client
import os

bp = Blueprint('main', __name__)

# ✅ Load Supabase client securely
supabase_url = os.getenv("SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_KEY")
supabase = create_client(supabase_url, supabase_key)

# ✅ Homepage: redirect based on session role
@bp.route('/')
def index():
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('main.login'))

    user = get_current_user()
    if user:
        role = user.get('role')
        if role == 'admin':
            return redirect(url_for('main.admin_dashboard'))
        elif role == 'manager':
            return redirect(url_for('main.manager_dashboard'))
        else:
            return redirect(url_for('main.employee_dashboard'))

    session.clear()
    return redirect(url_for('main.login'))

# ✅ Login route — POST with JSON support for frontend
@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Support both form and JSON payloads
        data = request.get_json() if request.is_json else request.form
        email = data.get('email')
        password = data.get('password')

        if not email or not password:
            msg = 'Please provide both email and password.'
            if request.is_json:
                return jsonify({"success": False, "message": msg}), 400
            flash(msg, 'danger')
            return redirect(url_for('main.login'))

        user = authenticate_user(email, password)
        if user:
            session['user_id'] = user['id']
            session['user_role'] = user['role']
            msg = f"Welcome, {user['full_name']}!"

            if request.is_json:
                return jsonify({"success": True, "message": msg, "user": user, "token": "
