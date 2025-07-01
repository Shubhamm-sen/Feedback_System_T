# routes.py

from flask import render_template, request, redirect, url_for, flash, session, jsonify, Blueprint
from datetime import datetime
from werkzeug.security import generate_password_hash
from auth import authenticate_user, get_current_user, role_required 
from mongoengine.queryset.visitor import Q

# Import all the necessary functions from our auth module
# from auth import authenticate_user, get_current_user, manager_required, employee_required, admin_required

# --- NO 'from models import ...' AT THE TOP ---

bp = Blueprint('main', __name__)

# --- Core Navigation and Auth Routes ---

@bp.route('/')
def index():
    if not session.get('user_id'):
        return redirect(url_for('main.login'))
    
    user = get_current_user()
    if user:
        # --- CHANGE: Added redirect for admin role ---
        if user.role == 'admin':
            return redirect(url_for('main.admin_dashboard'))
        elif user.role == 'manager':
            return redirect(url_for('main.manager_dashboard'))
        else:
            return redirect(url_for('main.employee_dashboard'))
    
    # If user in session is somehow invalid, clear it
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
            session['user_id'] = str(user.id)
            session['user_role'] = user.role
            flash(f'Welcome, {user.full_name}!', 'success')
            
            # --- CHANGE: Added redirect for admin role ---
            if user.role == 'admin':
                return redirect(url_for('main.admin_dashboard'))
            elif user.role == 'manager':
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

# --- NEW: Admin Routes ---

@bp.route('/admin/dashboard')
@role_required('admin')
def admin_dashboard():
    from models import User, Team
    all_users = User.objects.all()
    all_teams = Team.objects.all()
    # Find all managers to populate the "Create Team" dropdown
    managers = User.objects(role='manager')
    return render_template('admin_dashboard.html', users=all_users, teams=all_teams, managers=managers)

@bp.route('/admin/create-team', methods=['POST'])
@role_required('admin')
def admin_create_team():
    from models import User, Team
    team_name = request.form.get('name')
    manager_id = request.form.get('manager_id')
    manager = User.objects(pk=manager_id, role='manager').first()

    if not all([team_name, manager]):
        flash('Team Name and a valid Manager are required.', 'danger')
        return redirect(url_for('main.admin_dashboard'))
    
    # Check if team name already exists
    if Team.objects(name=team_name).first():
        flash(f'A team named "{team_name}" already exists.', 'warning')
        return redirect(url_for('main.admin_dashboard'))

    new_team = Team(name=team_name, manager=manager)
    new_team.save()
    flash(f'Team "{team_name}" created successfully!', 'success')
    return redirect(url_for('main.admin_dashboard'))

@bp.route('/admin/team/<team_id>')
@role_required('admin')
def admin_manage_team(team_id):
    from models import User, Team
    team = Team.objects(pk=team_id).first_or_404()
    # Find employees who are NOT currently in any team to add them
    unassigned_employees = User.objects(role='employee', team=None)
    return render_template('manage_team.html', team=team, unassigned_employees=unassigned_employees)

@bp.route('/admin/team/<team_id>/add', methods=['POST'])
@role_required('admin')
def admin_add_team_member(team_id):
    from models import User, Team
    team = Team.objects(pk=team_id).first_or_404()
    employee_id = request.form.get('employee_id')
    employee = User.objects(pk=employee_id, role='employee').first()

    if employee:
        team.members.append(employee)
        team.save()
        # Also update the user's record to point to the team
        employee.team = team
        employee.save()
        flash(f'{employee.full_name} added to {team.name}.', 'success')
    else:
        flash('Invalid employee selected.', 'danger')

    return redirect(url_for('main.admin_manage_team', team_id=team_id))

@bp.route('/admin/team/remove/<employee_id>')
@role_required('admin')
def admin_remove_team_member(employee_id):
    from models import User
    employee = User.objects(pk=employee_id).first_or_404()
    team_id = employee.team.id
    
    # Remove user from the team's member list
    employee.team.update(pull__members=employee)
    # Unset the user's team field
    employee.team = None
    employee.save()
    
    flash(f'{employee.full_name} has been removed from the team.', 'success')
    return redirect(url_for('main.admin_manage_team', team_id=team_id))


@bp.route('/admin/create-user', methods=['POST'])
@role_required('admin')
def admin_create_user():
    from models import User
    
    # Get form data
    email = request.form.get('email')
    full_name = request.form.get('full_name')
    password = request.form.get('password')
    role = request.form.get('role')

    # Basic validation
    if not all([email, full_name, password, role]):
        flash('All fields are required.', 'danger')
        return redirect(url_for('main.admin_dashboard'))

    # Check if user already exists
    if User.objects(email=email).first():
        flash('A user with that email already exists.', 'danger')
        return redirect(url_for('main.admin_dashboard'))

    # Create and save the new user
    hashed_password = generate_password_hash(password)
    new_user = User(email=email, full_name=full_name, password_hash=hashed_password, role=role)
    new_user.save()

    flash(f'User "{full_name}" created successfully!', 'success')
    return redirect(url_for('main.admin_dashboard'))

@bp.route('/admin/delete/<user_id>', methods=['POST'])
@role_required('admin')
def admin_delete_user(user_id):
    from models import User, Team, Feedback
    current_user = get_current_user()
    user_to_delete = User.objects(pk=user_id).first()

    if not user_to_delete:
        flash('User not found.', 'danger')
        return redirect(url_for('main.admin_dashboard'))

    # Safety check: admin cannot delete themselves
    if user_to_delete.id == current_user.id:
        flash('You cannot delete your own account.', 'danger')
        return redirect(url_for('main.admin_dashboard'))
    
    # --- NEW: Cleanup Logic ---
    
    # 1. If the user is a manager, find their team and set its manager to None.
    #    (Alternatively, you could prevent deletion or reassign the team)
    if user_to_delete.role == 'manager':
        Team.objects(manager=user_to_delete).update(set__manager=None)

    # 2. Remove the user from any team's `members` list.
    Team.objects(members=user_to_delete).update(pull__members=user_to_delete)

    # 3. Delete all feedback authored by or sent to this user.
    Feedback.objects(Q(author=user_to_delete) | Q(recipient=user_to_delete)).delete()
    
    # --- END Cleanup Logic ---

    # Finally, delete the user themselves
    user_to_delete.delete()
    flash(f'User "{user_to_delete.full_name}" and all associated data has been deleted.', 'success')
    
    return redirect(url_for('main.admin_dashboard'))

# --- Manager and Employee Routes ---

# @bp.route('/manager/dashboard')
# @role_required('manager')
# def manager_dashboard():
#     from models import Team, Feedback
#     current_user = get_current_user()
#     team = Team.objects(manager=current_user).first()
#     team_employees = team.members if team else []
#     # Get feedback given BY this manager and TO this manager
#     feedback_given = Feedback.objects(author=current_user).order_by('-created_at')
#     feedback_received = Feedback.objects(recipient=current_user).order_by('-created_at')
#     return render_template('manager_dashboard.html', user=current_user, team_employees=team_employees, feedback_given=feedback_given, feedback_received=feedback_received)

# In routes.py
# @bp.route('/manager/dashboard')
# @role_required('manager')
# def manager_dashboard():
#     from models import Team, Feedback
#     current_user = get_current_user()
#     team = Team.objects(manager=current_user).first()
#     team_employees = team.members if team else []
    
#     # Get feedback given BY this manager and TO this manager
#     feedback_given = Feedback.objects(author=current_user).order_by('-created_at')
#     feedback_received = Feedback.objects(recipient=current_user).order_by('-created_at')

#     # --- THE FIX: Use a Q object for a proper OR query ---
#     # This creates a single, more efficient query to the database
#     all_related_feedback = Feedback.objects(
#         Q(author=current_user) | Q(recipient=current_user)
#     )

#     # Calculate statistics based on the combined query result
#     sentiment_counts = {'positive': 0, 'neutral': 0, 'negative': 0}
#     for feedback in all_related_feedback:
#         sentiment_counts[feedback.sentiment] += 1
        
#     acknowledged_count = all_related_feedback.filter(status='acknowledged').count()
#     total_feedback = all_related_feedback.count()
#     # --- END FIX ---

#     return render_template(
#         'manager_dashboard.html', 
#         user=current_user, 
#         team_employees=team_employees, 
#         feedback_given=feedback_given, 
#         feedback_received=feedback_received,
#         sentiment_counts=sentiment_counts,
#         acknowledged_count=acknowledged_count,
#         total_feedback=total_feedback
#     )



# In routes.py

# In routes.py

@bp.route('/manager/dashboard')
@role_required('manager')
def manager_dashboard():
    from models import Team, Feedback
    from mongoengine.queryset.visitor import Q
    
    current_user = get_current_user()
    
    # --- Data for display lists ---
    team = Team.objects(manager=current_user).first()
    team_employees = team.members if team else []
    
    # --- CHANGE: We will base all stats ONLY on feedback GIVEN by the manager ---
    feedback_given = Feedback.objects(author=current_user).order_by('-created_at')
    
    # For display purposes, we still want to show feedback they've received
    feedback_received = Feedback.objects(recipient=current_user).order_by('-created_at')

    # --- Data for stats cards and sentiment chart ---
    # All calculations will now use the `feedback_given` queryset
    
    total_feedback_count = feedback_given.count()
    acknowledged_count = feedback_given.filter(status='acknowledged').count()
    pending_count = total_feedback_count - acknowledged_count
    
    # Calculate sentiment based only on feedback given
    sentiment_counts = {'positive': 0, 'neutral': 0, 'negative': 0}
    for feedback in feedback_given:
        sentiment_counts[feedback.sentiment] += 1
    
    # This calculation is no longer needed but kept for reference if you want to add it back
    # if total_feedback_count > 0:
    #     acknowledgment_percentage = int((acknowledged_count / total_feedback_count) * 100)
    # else:
    #     acknowledgment_percentage = 0

    return render_template(
        'manager_dashboard.html', 
        user=current_user,
        team_employees=team_employees,
        feedback_given=feedback_given,
        feedback_received=feedback_received,
        total_feedback_count=total_feedback_count,
        acknowledged_count=acknowledged_count,
        pending_count=pending_count
        # Note: We are not passing sentiment_counts yet, we will do that in the API
    )



@bp.route('/employee/dashboard')
@role_required('employee')
def employee_dashboard():
    from models import Feedback
    current_user = get_current_user()
    # Get feedback received BY this employee and given BY this employee
    feedback_received = Feedback.objects(recipient=current_user).order_by('-created_at')
    feedback_given = Feedback.objects(author=current_user).order_by('-created_at')
    return render_template('employee_dashboard.html', user=current_user, feedback_received=feedback_received, feedback_given=feedback_given)

@bp.route('/feedback/new', methods=['GET', 'POST'])
def create_feedback():
    # ... (the recipient logic at the top remains the same) ...
    from models import User, Feedback, Team
    current_user = get_current_user()
    if not current_user: return redirect(url_for('main.login'))
    # ... (recipient logic remains the same) ...
    recipients = []
    if current_user.role == 'manager':
        team = Team.objects(manager=current_user).first()
        if team: recipients = team.members
    elif current_user.role == 'employee':
        if current_user.team:
            recipients.append(current_user.team.manager)
            for member in current_user.team.members:
                if member.id != current_user.id: recipients.append(member)
    else: 
        recipients = User.objects(id__ne=current_user.id)

    if request.method == 'POST':
        recipient_id = request.form.get('recipient_id')
        # --- CHANGE: Get new fields from form ---
        strengths = request.form.get('strengths')
        improvements = request.form.get('improvements')
        sentiment = request.form.get('sentiment')

        if not all([recipient_id, strengths, improvements, sentiment]):
            flash('All fields are required.', 'danger')
            return redirect(url_for('main.create_feedback'))

        recipient = User.objects(pk=recipient_id).first()
        if not recipient or recipient not in recipients:
            flash('Invalid recipient selected.', 'danger')
            return redirect(url_for('main.create_feedback'))

        # --- CHANGE: Save new fields to database ---
        Feedback(
            author=current_user,
            recipient=recipient,
            strengths=strengths,
            improvements=improvements,
            sentiment=sentiment
        ).save()

        flash('Feedback submitted successfully!', 'success')
        return redirect(url_for(f'main.{current_user.role}_dashboard'))

    return render_template('feedback_form.html', recipients=recipients, edit_mode=False)


@bp.route('/feedback/edit/<feedback_id>', methods=['GET', 'POST'])
def edit_feedback(feedback_id):
    from models import Feedback
    current_user = get_current_user()
    feedback_item = Feedback.objects(pk=feedback_id).first_or_404()

    # Authorization Check: Only the author can edit
    if feedback_item.author != current_user:
        flash('You are not authorized to edit this feedback.', 'danger')
        return redirect(url_for(f'main.{current_user.role}_dashboard'))

    if request.method == 'POST':
        # Update the feedback object with form data
        feedback_item.strengths = request.form.get('strengths')
        feedback_item.improvements = request.form.get('improvements')
        feedback_item.sentiment = request.form.get('sentiment')
        feedback_item.save()
        flash('Feedback updated successfully!', 'success')
        return redirect(url_for(f'main.{current_user.role}_dashboard'))

    # For a GET request, show the form with the existing data
    return render_template('feedback_form.html', edit_mode=True, feedback=feedback_item)


# --- NEW: Delete Feedback Route ---
@bp.route('/feedback/delete/<feedback_id>', methods=['POST'])
def delete_feedback(feedback_id):
    from models import Feedback
    current_user = get_current_user()
    feedback_item = Feedback.objects(pk=feedback_id).first_or_404()

    # Authorization Check: Only the author can delete
    if feedback_item.author != current_user:
        flash('You are not authorized to delete this feedback.', 'danger')
    else:
        feedback_item.delete()
        flash('Feedback has been deleted.', 'success')
    
    return redirect(url_for(f'main.{current_user.role}_dashboard'))




@bp.route('/feedback/<feedback_id>/acknowledge', methods=['POST'])
@role_required('employee')
def acknowledge_feedback(feedback_id):
    from models import Feedback
    current_user = get_current_user()
    
    # Find the feedback, ensuring it was sent to the currently logged-in employee
    feedback_item = Feedback.objects(pk=feedback_id, recipient=current_user).first()
    
    if feedback_item and feedback_item.status == 'pending':
        feedback_item.status = 'acknowledged'
        feedback_item.acknowledged_at = datetime.utcnow()
        feedback_item.save()
        flash('Feedback acknowledged!', 'success')
    elif not feedback_item:
        flash('Feedback not found or you do not have permission to acknowledge it.', 'danger')
    else:
        flash('This feedback has already been acknowledged.', 'info')
        
    return redirect(url_for('main.employee_dashboard'))    


@bp.route('/api/sentiment-data')
@role_required('manager')
def sentiment_data():
    from models import Feedback
    current_user = get_current_user()
    
    # --- CHANGE: Query ONLY feedback where the manager is the author ---
    feedback_given = Feedback.objects(author=current_user)
    
    sentiment_counts = {'positive': 0, 'neutral': 0, 'negative': 0}
    for feedback in feedback_given:
        sentiment_counts[feedback.sentiment] += 1
        
    return jsonify(sentiment_counts)

@bp.route('/manager/feedback/<feedback_id>/acknowledge', methods=['POST'])
@role_required('manager')
def manager_acknowledge_feedback(feedback_id):
    from models import Feedback
    current_user = get_current_user()
    
    # Find the feedback, ensuring it was sent to the currently logged-in manager
    feedback_item = Feedback.objects(pk=feedback_id, recipient=current_user).first()
    
    if feedback_item and feedback_item.status == 'pending':
        feedback_item.status = 'acknowledged'
        feedback_item.acknowledged_at = datetime.utcnow()
        feedback_item.save()
        flash('Feedback from your team member has been acknowledged!', 'success')
    elif not feedback_item:
        flash('Feedback not found or you do not have permission to acknowledge it.', 'danger')
    else:
        flash('This feedback has already been acknowledged.', 'info')
        
    return redirect(url_for('main.manager_dashboard'))    



@bp.context_processor
def inject_user():
    # This makes 'current_user' available in all templates
    return {'current_user': get_current_user()}