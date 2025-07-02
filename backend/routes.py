from flask import render_template, request, redirect, url_for, flash, session, jsonify, Blueprint
from datetime import datetime
from auth import authenticate_user, get_current_user, role_required
from supabase_client import supabase  # ✅ Use centralized client

bp = Blueprint('main', __name__)

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
                return jsonify({
                    "success": True,
                    "message": msg,
                    "user": user,
                    "token": "SESSION_TOKEN_PLACEHOLDER"
                }), 200

            flash(msg, 'success')
            if user['role'] == 'admin':
                return redirect(url_for('main.admin_dashboard'))
            elif user['role'] == 'manager':
                return redirect(url_for('main.manager_dashboard'))
            else:
                return redirect(url_for('main.employee_dashboard'))

        msg = 'Invalid email or password.'
        if request.is_json:
            return jsonify({"success": False, "message": msg}), 401
        flash(msg, 'danger')
        return redirect(url_for('main.login'))

    return render_template('login.html')

# ✅ Logout route
@bp.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out successfully.', 'info')
    return redirect(url_for('main.login'))

# ✅ Inject user into templates
@bp.context_processor
def inject_user():
    return {'current_user': get_current_user()}

# ✅ Dummy role-based dashboards
@bp.route('/admin')
@role_required('admin')
def admin_dashboard():
    return render_template('admin_dashboard.html')

@bp.route('/manager')
@role_required('manager')
def manager_dashboard():
    return render_template('manager_dashboard.html')

@bp.route('/employee')
@role_required('employee')
def employee_dashboard():
    return render_template('employee_dashboard.html')
