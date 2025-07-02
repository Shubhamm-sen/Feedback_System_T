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

# ✅ Feedback creation route (reusable form)
@bp.route('/feedback/create', methods=['GET', 'POST'])
@role_required('manager')
def create_feedback():
    manager_id = session.get('user_id')

    if request.method == 'POST':
        recipient_id = request.form.get('recipient_id')
        strengths = request.form.get('strengths')
        improvements = request.form.get('improvements')
        sentiment = request.form.get('sentiment')

        if not recipient_id or not strengths or not improvements or not sentiment:
            flash('All fields are required.', 'danger')
            return redirect(url_for('main.create_feedback'))

        try:
            created_at = datetime.utcnow().isoformat()
            supabase.table('feedback').insert({
                "author_id": manager_id,
                "recipient_id": recipient_id,
                "strengths": strengths,
                "improvements": improvements,
                "sentiment": sentiment,
                "status": "pending",
                "created_at": created_at
            }).execute()

            flash("✅ Feedback submitted successfully!", "success")
            return redirect(url_for('main.manager_dashboard'))

        except Exception as e:
            print(f"[Create Feedback Error] {e}")
            flash("❌ Failed to submit feedback. Try again.", "danger")
            return redirect(url_for('main.create_feedback'))

    response = supabase.table('users').select('id, full_name, role').eq('manager_id', manager_id).execute()
    recipients = response.data if response.data else []

    return render_template('feedback_form.html', edit_mode=False, recipients=recipients)

# ✅ Feedback edit route
@bp.route('/feedback/<feedback_id>/edit', methods=['GET', 'POST'])
@role_required('manager')
def edit_feedback(feedback_id):
    if request.method == 'POST':
        strengths = request.form.get('strengths')
        improvements = request.form.get('improvements')
        sentiment = request.form.get('sentiment')

        try:
            supabase.table('feedback').update({
                "strengths": strengths,
                "improvements": improvements,
                "sentiment": sentiment
            }).eq('id', feedback_id).execute()

            flash("✅ Feedback updated successfully.", "success")
            return redirect(url_for('main.manager_dashboard'))

        except Exception as e:
            print(f"[Edit Feedback Error] {e}")
            flash("❌ Could not update feedback.", "danger")
            return redirect(url_for('main.edit_feedback', feedback_id=feedback_id))

    try:
        fb_res = supabase.table('feedback').select('*').eq('id', feedback_id).single().execute()
        feedback = fb_res.data

        recipient_res = supabase.table('users').select('id, full_name').eq('id', feedback['recipient_id']).single().execute()
        feedback['recipient'] = recipient_res.data

        return render_template('feedback_form.html', edit_mode=True, feedback=feedback)

    except Exception as e:
        print(f"[Fetch Feedback Error] {e}")
        flash("❌ Feedback not found.", "danger")
        return redirect(url_for('main.manager_dashboard'))

# ✅ Feedback delete route
@bp.route('/feedback/<feedback_id>/delete', methods=['POST'])
@role_required('manager')
def delete_feedback(feedback_id):
    try:
        supabase.table('feedback').delete().eq('id', feedback_id).execute()
        flash("🗑️ Feedback deleted.", "info")
    except Exception as e:
        print(f"[Delete Feedback Error] {e}")
        flash("❌ Failed to delete feedback.", "danger")
    return redirect(url_for('main.manager_dashboard'))
