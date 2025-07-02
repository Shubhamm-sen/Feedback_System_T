# import json
# import os
# from datetime import datetime
# from typing import Dict, List, Optional
# from models import User, Feedback, Team
# from werkzeug.security import generate_password_hash
# import uuid

# class DataStore:
#     def __init__(self):
#         self.users: Dict[str, User] = {}
#         self.feedback: Dict[str, Feedback] = {}
#         self.teams: Dict[str, Team] = {}
#         self._initialize_sample_data()
    
#     def _initialize_sample_data(self):
#         """Initialize with sample users and teams for demo purposes"""
#         # Create sample manager
#         manager_id = str(uuid.uuid4())
#         manager = User(
#             id=manager_id,
#             username="manager1",
#             email="manager@company.com",
#             password_hash=generate_password_hash("password123"),
#             role="manager"
#         )
#         self.users[manager_id] = manager
        
#         # Create sample employees
#         employee1_id = str(uuid.uuid4())
#         employee1 = User(
#             id=employee1_id,
#             username="employee1",
#             email="employee1@company.com",
#             password_hash=generate_password_hash("password123"),
#             role="employee",
#             manager_id=manager_id
#         )
#         self.users[employee1_id] = employee1
        
#         employee2_id = str(uuid.uuid4())
#         employee2 = User(
#             id=employee2_id,
#             username="employee2",
#             email="employee2@company.com",
#             password_hash=generate_password_hash("password123"),
#             role="employee",
#             manager_id=manager_id
#         )
#         self.users[employee2_id] = employee2
        
#         # Create sample team
#         team_id = str(uuid.uuid4())
#         team = Team(
#             id=team_id,
#             name="Development Team",
#             manager_id=manager_id,
#             employee_ids=[employee1_id, employee2_id]
#         )
#         self.teams[team_id] = team
        
#         # Update users with team info
#         manager.team_id = team_id
#         employee1.team_id = team_id
#         employee2.team_id = team_id
    
#     def get_user_by_username(self, username: str) -> Optional[User]:
#         for user in self.users.values():
#             if user.username == username:
#                 return user
#         return None
    
#     def get_user_by_id(self, user_id: str) -> Optional[User]:
#         return self.users.get(user_id)
    
#     def create_feedback(self, manager_id: str, employee_id: str, strengths: str, 
#                        improvements: str, sentiment: str) -> Feedback:
#         feedback_id = str(uuid.uuid4())
#         feedback = Feedback(
#             id=feedback_id,
#             manager_id=manager_id,
#             employee_id=employee_id,
#             strengths=strengths,
#             improvements=improvements,
#             sentiment=sentiment,
#             created_at=datetime.now(),
#             updated_at=datetime.now()
#         )
#         self.feedback[feedback_id] = feedback
#         return feedback
    
#     def update_feedback(self, feedback_id: str, strengths: str, improvements: str, 
#                        sentiment: str) -> Optional[Feedback]:
#         if feedback_id in self.feedback:
#             feedback = self.feedback[feedback_id]
#             feedback.strengths = strengths
#             feedback.improvements = improvements
#             feedback.sentiment = sentiment
#             feedback.updated_at = datetime.now()
#             return feedback
#         return None
    
#     def acknowledge_feedback(self, feedback_id: str) -> Optional[Feedback]:
#         if feedback_id in self.feedback:
#             feedback = self.feedback[feedback_id]
#             feedback.acknowledged = True
#             feedback.acknowledged_at = datetime.now()
#             return feedback
#         return None
    
#     def get_feedback_for_employee(self, employee_id: str) -> List[Feedback]:
#         return [f for f in self.feedback.values() if f.employee_id == employee_id]
    
#     def get_feedback_by_manager(self, manager_id: str) -> List[Feedback]:
#         return [f for f in self.feedback.values() if f.manager_id == manager_id]
    
#     def get_team_employees(self, manager_id: str) -> List[User]:
#         team = None
#         for t in self.teams.values():
#             if t.manager_id == manager_id:
#                 team = t
#                 break
        
#         if team:
#             return [self.users[emp_id] for emp_id in team.employee_ids if emp_id in self.users]
#         return []
    
#     def get_feedback_by_id(self, feedback_id: str) -> Optional[Feedback]:
#         return self.feedback.get(feedback_id)

# # Global data store instance
# data_store = DataStore()
