from flask import session, redirect, url_for, flash
from functools import wraps
import bcrypt
from backend.supabase_client import supabase  # Make sure this file exists and has Supabase client

# --- Role-based access decorator ---
def role_required(required_role):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            user_id = session.get('user_id')
            if not user_id:
                flash('Please log in to access this page.', 'warning')
                return redirect(url_for('main.login'))

            # Fetch user from Supabase
            response = supabase.table('users').select('*').eq('id', user_id).single().execute()
            user = response.data

            if not user or user.get('role') != required_role:
                flash('Access denied. You do not have the required permissions.', 'danger')
                return redirect(url_for('main.login'))

            return f(*args, **kwargs)
        return decorated_function
    return decorator

# --- Authentication Function ---
def authenticate_user(email: str, password: str):
    try:
        response = supabase.table('users').select('*').eq('email', email).single().execute()
        user = response.data

        if user and bcrypt.checkpw(password.encode(), user['password_hash'].encode()):
            return user
    except Exception as e:
        print(f"[Auth Error] {e}")
    return None

# --- Get Current User from Session ---
def get_current_user():
    user_id = session.get('user_id')
    if not user_id:
        return None
    response = supabase.table('users').select('*').eq('id', user_id).single().execute()
    return response.data if response.data else None
