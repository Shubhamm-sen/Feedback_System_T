# seed_db.py

from app import create_app
from werkzeug.security import generate_password_hash
import datetime

# Create the app instance so we can work with the database.
app = create_app()

def run_seed():
    """Seeds the database with sample data."""
    # The app_context makes the configured app and its extensions available.
    with app.app_context():
        # We import the models *inside* the context, now that the db object is ready.
        from models import User, Team, Feedback

        print("Clearing existing data...")
        Feedback.objects.delete()
        Team.objects.delete()
        User.objects.delete()
        print("Cleared existing data.")

        # --- CHANGE: Create a default Admin user ---
        admin_pwd = generate_password_hash('adminpass')
        admin = User(email='admin@example.com', password_hash=admin_pwd, full_name='Admin User', role='admin').save()
        print(f"Created Admin: {admin.full_name}")

        # --- Create a sample Manager user ---
        manager1_pwd = generate_password_hash('managerpass')
        manager1 = User(email='manager@example.com', password_hash=manager1_pwd, full_name='Jane Doe', role='manager').save()
        print(f"Created Manager: {manager1.full_name}")

        # --- Create a sample Employee user ---
        emp1_pwd = generate_password_hash('emppass1')
        emp1 = User(email='employee1@example.com', password_hash=emp1_pwd, full_name='John Smith', role='employee').save()
        print(f"Created Employee: {emp1.full_name}")

        # --- Create a Team and Assign Users ---
        dev_team = Team(name='Development', manager=manager1).save()
        dev_team.members.append(emp1)
        dev_team.save()
        print(f"Created Team: {dev_team.name}")

        # Update the employee with their team reference
        emp1.team = dev_team
        emp1.save()
        print("Assigned employee to the team.")

        # --- CHANGE: Create sample Feedback using the new 'content' field ---
        # # Employee -> Manager feedback
        # Feedback(
        #     author=emp1,
        #     recipient=manager1,
        #     content="The new project timeline is very aggressive. I'm concerned about burnout.",
        #     sentiment="negative"
        # ).save()

        # # Manager -> Employee feedback
        # Feedback(
        #     author=manager1,
        #     recipient=emp1,
        #     content="Great work on the latest feature! Your problem-solving skills were a huge help.",
        #     sentiment="positive",
        #     status="acknowledged" # Let's make one already acknowledged
        # ).save()
        # print("Created sample feedback.")
        

        Feedback(
            author=emp1,
            recipient=manager1,
            strengths="Very supportive and provides clear direction on projects.",
            improvements="Sometimes meetings could be shorter or handled via email.",
            sentiment="positive"
        ).save()

        Feedback(
            author=manager1,
            recipient=emp1,
            strengths="Excellent work on the latest feature! Your problem-solving skills were a huge help.",
            improvements="Let's focus on adding more unit tests for new code in the next sprint.",
            sentiment="positive",
            status="acknowledged"
        ).save()
        print("Created sample feedback.")


if __name__ == '__main__':
    print("Starting database seed...")
    run_seed()
    print("\n--- Seeding complete! ---")
    print("\nLogins created:")
    print("  Admin:    admin@example.com / adminpass")
    print("  Manager:  manager@example.com / managerpass")
    print("  Employee: employee1@example.com / emppass1")