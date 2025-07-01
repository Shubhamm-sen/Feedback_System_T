# Backend - Internal Feedback Tool

This directory contains the Flask backend application for the feedback system.

## Structure

- `app.py` - Main Flask application setup and configuration
- `routes.py` - Application routes and view handlers
- `auth.py` - Authentication and authorization logic
- `data_store.py` - In-memory data storage and sample data
- `models.py` - Data model definitions (User, Feedback, Team)
- `main.py` - Entry point for running the application
- `templates/` - Jinja2 HTML templates for server-side rendering
- `static/` - Static assets (CSS, JavaScript, images)

## Features

- Session-based authentication with role-based access control
- Manager and Employee role separation
- Feedback creation, editing, and acknowledgment system
- Dashboard analytics with sentiment analysis
- Real-time updates and timeline visualization
- In-memory data storage (ready for database integration)

## API Endpoints

- `/` - Home page with role-based redirection
- `/login` - Authentication endpoint
- `/logout` - Session termination
- `/manager/dashboard` - Manager dashboard
- `/employee/dashboard` - Employee dashboard
- `/feedback/create` - Feedback creation form
- `/feedback/edit/<id>` - Feedback editing
- `/feedback/acknowledge/<id>` - Feedback acknowledgment
- `/api/sentiment-data` - Sentiment analytics API

## Configuration

The application uses environment variables for configuration:
- `SESSION_SECRET` - Flask session encryption key
- `JWT_SECRET_KEY` - JWT token signing key

## Running

Run the application using:
```bash
python main.py
```

The server will start on `http://0.0.0.0:5000`