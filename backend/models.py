# models.py
import datetime
from extensions import db

#
# --- We are removing the old @dataclass definitions ---
#

class User(db.Document):
    """ User model for Employees, Managers, and Admins. """
    email = db.EmailField(required=True, unique=True)
    password_hash = db.StringField(required=True)
    full_name = db.StringField(required=True, max_length=100)
    # --- CHANGE: Added 'admin' to the list of choices ---
    role = db.StringField(required=True, choices=('employee', 'manager', 'admin'))
    team = db.ReferenceField('Team')
    created_at = db.DateTimeField(default=datetime.datetime.utcnow)

    # Required for Flask-Login compatibility
    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)


class Team(db.Document):
    """ Team model to group users under a manager. """
    name = db.StringField(required=True, unique=True, max_length=100)
    manager = db.ReferenceField('User', required=True)
    members = db.ListField(db.ReferenceField('User'))
    created_at = db.DateTimeField(default=datetime.datetime.utcnow)


class Feedback(db.Document):
    """ Feedback model. """
    # This assumes a model where anyone can give feedback to anyone.
    # We can adjust if feedback is only Manager->Employee or Employee->Manager.
    author = db.ReferenceField('User', required=True)
    recipient = db.ReferenceField('User', required=True)
    strengths = db.StringField(default="") # Making these optional
    improvements = db.StringField(default="") # Making these optional
    # content = db.StringField(required=True) # Adding a general content field

    strengths = db.StringField(required=True)
    improvements = db.StringField(required=True)

    sentiment = db.StringField(required=True, choices=('positive', 'neutral', 'negative'))
    status = db.StringField(required=True, default='pending', choices=('pending', 'acknowledged'))
    created_at = db.DateTimeField(default=datetime.datetime.utcnow)
    acknowledged_at = db.DateTimeField()
    
    meta = {
        'indexes': ['author', 'recipient']
    }