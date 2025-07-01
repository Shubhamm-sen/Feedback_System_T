# # auth.py

# from flask import session, redirect, url_for, flash
# from werkzeug.security import check_password_hash
# from functools import wraps

# # --- NO 'from models import ...' AT THE TOP ---

# def role_required(required_role):
#     def decorator(f):
#         @wraps(f)
#         def decorated_function(*args, **kwargs):
#             from models import User  # Import is INSIDE
#             user_id = session.get('user_id')
#             if not user_id:
#                 flash('Please log in to access this page.', 'warning')
#                 return redirect(url_for('main.login'))
#             user = User.objects(pk=user_id).first()
#             if not user or user.role != required_role:
#                 flash('Access denied. You do not have the required permissions.', 'danger')
#                 return redirect(url_for('main.login'))
#             return f(*args, **kwargs)
#         return decorated_function
#     return decorator

# def manager_required(f):
#     """Convenience decorator for requiring 'manager' role."""
#     return role_required('manager')

# def employee_required(f):
#     """Convenience decorator for requiring 'employee' role."""
#     return role_required('employee')

# # --- CHANGE: Added admin_required decorator for our new role ---
# def admin_required(f):
#     """Convenience decorator for requiring 'admin' role."""
#     return role_required('admin')

# def authenticate_user(email: str, password: str):
#     from models import User  # Import is INSIDE
#     user = User.objects(email=email).first()
#     if user and check_password_hash(user.password_hash, password):
#         return user
#     return None

# def get_current_user():
#     from models import User  # Import is INSIDE
#     user_id = session.get('user_id')
#     if not user_id:
#         return None
#     return User.objects(pk=user_id).first()



# auth.py (Simplified Version)

from flask import session, redirect, url_for, flash
from werkzeug.security import check_password_hash
from functools import wraps

# We only need ONE decorator function.
def role_required(required_role):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            from models import User
            user_id = session.get('user_id')
            if not user_id:
                flash('Please log in to access this page.', 'warning')
                return redirect(url_for('main.login'))
            user = User.objects(pk=user_id).first()
            if not user or user.role != required_role:
                flash('Access denied. You do not have the required permissions.', 'danger')
                return redirect(url_for('main.login'))
            return f(*args, **kwargs)
        return decorated_function
    return decorator

# --- The rest of the file is the same ---

def authenticate_user(email: str, password: str):
    from models import User
    user = User.objects(email=email).first()
    if user and check_password_hash(user.password_hash, password):
        return user
    return None

def get_current_user():
    from models import User
    user_id = session.get('user_id')
    if not user_id:
        return None
    return User.objects(pk=user_id).first()