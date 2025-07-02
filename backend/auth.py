from flask import session, redirect, url_for, flash
from functools import wraps
from supabase import create_client
import os

# ✅ Initialize Supabase client
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError("❌ Supabase credentials missing in environment.")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# ✅ Role-required decorator
def role_required(required_role):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            user_id = session.get('user_id')
            if not user_id:
                flash('Please log in to access this page.', 'warning')
                return redirect(url_for('main.login'))

            try:
                response = supabase.table('users').select('*').eq('id', user_id).single().execute()
                user = response.data
                if not user or user.get('role') != required_role:
                    flash('Access denied. You do not have the required permissions.', 'danger')
                    return redirect(url_for('main.login'))
            except Exception as e:
                print(f"[Role Check Error] {e}")
                flash('Error checking user role.', 'danger')
                return redirect(url_for('main.login'))

            return f(*args, **kwargs)
        return decorated_function
    return decorator

# ✅ Authenticate user with plaintext password (no hashing)
def authenticate_user(email, password):
    try:
        response = supabase.table('users').select('*').eq('email', email).single().execute()
        user = response.data
        if user and user.get('password_hash') == password:
            return user
    except Exception as e:
        print(f"[Auth Error] {e}")
    return None

# ✅ Get current logged-in user from session
def get_current_user():
    user_id = session.get('user_id')
    if not user_id:
        return None
    try:
        response = supabase.table('users').select('*').eq('id', user_id).single().execute()
        return response.data if response.data else None
    except Exception as e:
        print(f"[Session Error] {e}")
        return None
