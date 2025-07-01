# Internal Feedback Tool

## Overview

This is a Flask-based internal feedback management system that enables managers and employees to share structured, ongoing feedback in a secure environment. The application provides role-based access control with separate dashboards for managers and employees, allowing for efficient feedback submission, viewing, and acknowledgment.

## Project Structure

The project is organized into separate frontend and backend directories:

### Frontend Directory (`/frontend`)
- `index.html` - Standalone login page with modern glass morphism design
- `css/style.css` - Custom styles and animations
- `js/auth.js` - Client-side authentication handling
- `README.md` - Frontend documentation

### Backend Directory (`/backend`)
- `app.py` - Flask application setup and configuration
- `routes.py` - Application routes and view handlers
- `auth.py` - Authentication and authorization logic
- `data_store.py` - In-memory data storage system
- `models.py` - Data model definitions
- `main.py` - Backend entry point
- `templates/` - Jinja2 HTML templates
- `static/` - Backend static assets
- `README.md` - Backend documentation

### Root Directory
- `main.py` - Project entry point that imports from backend
- `replit.md` - Project documentation and preferences

## System Architecture

### Backend Framework
- **Flask**: Lightweight Python web framework chosen for rapid development and simplicity
- **Flask-JWT-Extended**: JWT-based authentication system for stateless session management
- **Flask-CORS**: Cross-origin resource sharing support for potential API usage
- **Werkzeug**: WSGI utilities including password hashing and proxy handling

### Frontend Technology
- **Server-side rendered templates**: Using Jinja2 templating engine
- **Bootstrap 5**: Dark theme UI framework for responsive design
- **Chart.js**: Data visualization for sentiment analysis charts
- **Font Awesome**: Icon library for enhanced UI

### Authentication & Authorization
- **JWT tokens**: Non-expiring tokens for demo purposes (configurable in production)
- **Role-based access control**: Manager and Employee roles with specific permissions
- **Password hashing**: Werkzeug's secure password hashing implementation

## Key Components

### Data Models
- **User**: Stores user information including role, manager relationships
- **Feedback**: Structured feedback with strengths, improvements, and sentiment
- **Team**: Team structure linking managers to employees

### Data Storage
- **In-memory storage**: Current implementation uses Python dictionaries for demonstration
- **Sample data initialization**: Pre-populated with demo users and relationships

### Authentication System
- **Role decorators**: `@manager_required` and `@employee_required` for route protection
- **JWT identity management**: Token-based user identification
- **Session management**: Flask sessions for web interface state

### Route Structure
- **Public routes**: Login and index (with redirects)
- **Manager routes**: Dashboard, feedback creation/editing, team management
- **Employee routes**: Personal dashboard, feedback acknowledgment

## Data Flow

1. **Authentication Flow**:
   - User submits credentials → Backend validates → JWT token generated → User redirected to role-specific dashboard

2. **Feedback Creation**:
   - Manager selects employee → Fills feedback form → Data stored → Employee notified on dashboard

3. **Feedback Viewing**:
   - Employees see timeline of received feedback → Can acknowledge feedback → Status updates to manager view

4. **Dashboard Analytics**:
   - Real-time calculation of feedback metrics → Chart.js visualization → Responsive updates

## External Dependencies

### Frontend Libraries (CDN)
- Bootstrap 5 with Replit dark theme
- Chart.js for data visualization
- Font Awesome for icons

### Python Packages
- Flask ecosystem (Flask, Flask-JWT-Extended, Flask-CORS)
- Werkzeug for security utilities
- Standard library modules (os, logging, datetime, uuid, json)

## Deployment Strategy

### Current Setup
- **Development server**: Flask built-in server on port 5000
- **Environment variables**: JWT secrets and session keys
- **Proxy configuration**: ProxyFix for deployment behind reverse proxies

### Production Considerations
- Replace in-memory storage with persistent database
- Update JWT expiration settings
- Configure proper secret key management
- Add HTTPS/SSL support
- Implement proper logging and monitoring

### Environment Variables
- `SESSION_SECRET`: Flask session encryption key
- `JWT_SECRET_KEY`: JWT token signing key

## Changelog
- June 28, 2025: Initial setup with Flask feedback application
- June 28, 2025: Enhanced UI with modern glass morphism design and animations
- June 28, 2025: Fixed authentication to use session-based system
- June 28, 2025: Removed database setup per user request - using in-memory storage
- June 28, 2025: Separated frontend and backend files into organized directory structure

## User Preferences

Preferred communication style: Simple, everyday language.
Frontend preference: Use only JavaScript/JSX, not TypeScript.
Database preference: User will add database manually when ready.