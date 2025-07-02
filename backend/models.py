# models.py — Supabase Version
import os
from dotenv import load_dotenv
from supabase import create_client

load_dotenv()

# --- Supabase Setup ---
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# --- USERS ---

def get_user_by_email(email):
    response = supabase.table("users").select("*").eq("email", email).single().execute()
    return response.data if response.data else None

def get_user_by_id(user_id):
    response = supabase.table("users").select("*").eq("id", user_id).single().execute()
    return response.data if response.data else None

def create_user(email, password_hash, full_name, role, team_id=None):
    return supabase.table("users").insert({
        "email": email,
        "password_hash": password_hash,
        "full_name": full_name,
        "role": role,
        "team_id": team_id
    }).execute()


# --- TEAMS ---

def create_team(name, manager_id):
    return supabase.table("teams").insert({
        "name": name,
        "manager_id": manager_id,
    }).execute()

def get_team_by_manager(manager_id):
    response = supabase.table("teams").select("*").eq("manager_id", manager_id).single().execute()
    return response.data if response.data else None

def assign_employee_to_team(employee_id, team_id):
    return supabase.table("users").update({"team_id": team_id}).eq("id", employee_id).execute()


# --- FEEDBACK ---

def give_feedback(author_id, recipient_id, strengths, improvements, sentiment):
    return supabase.table("feedback").insert({
        "author_id": author_id,
        "recipient_id": recipient_id,
        "strengths": strengths,
        "improvements": improvements,
        "sentiment": sentiment,
        "status": "pending"
    }).execute()

def acknowledge_feedback(feedback_id):
    return supabase.table("feedback").update({
        "status": "acknowledged"
    }).eq("id", feedback_id).execute()

def get_feedback_for_user(user_id):
    response = supabase.table("feedback").select("*").eq("recipient_id", user_id).execute()
    return response.data if response.data else []

def get_feedback_by_author(author_id):
    response = supabase.table("feedback").select("*").eq("author_id", author_id).execute()
    return response.data if response.data else []
