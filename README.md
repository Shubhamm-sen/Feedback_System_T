# Internal Feedback Tool

This is a full-featured, database-driven web application for managing internal company feedback. It provides a platform for employees, managers, and administrators to create, view, and manage feedback within a team structure. The application is built with Flask and MongoDB and is containerized with Docker for easy deployment.

## Key Features

- **Role-Based Access Control:** Separate dashboards and permissions for Admin, Manager, and Employee roles.
- **Admin Dashboard:**
    - Create, view, and delete user accounts (Managers & Employees).
    - Create, view, and manage teams by assigning managers and adding/removing members.
- **Manager Dashboard:**
    - View team members.
    - Give feedback to team members and receive feedback from them.
    - Acknowledge feedback received.
    - View a sentiment analysis chart based on feedback given.
- **Employee Dashboard:**
    - Give feedback to their manager and team peers.
    - Receive and acknowledge feedback.
    - View the status of feedback they have sent.
- **Full CRUD Functionality:** Users can create, edit, and delete the feedback they have authored.
- **Database Backend:** Uses MongoDB for persistent and scalable data storage.
- **Dockerized:** Includes a `Dockerfile` for easy, consistent deployment in any environment.

## Tech Stack

- **Backend:** Flask, MongoEngine
- **Database:** MongoDB
- **Frontend:** Jinja2, Bootstrap 5, Chart.js, Select2
- **Deployment:** Gunicorn, Docker

---

## Getting Started

You can run this project locally for development or as a Docker container.

### A. Running with Docker (Recommended)

This is the easiest way to get the application running.

**Prerequisites:**
- [Docker](https://www.docker.com/get-started) installed on your machine.

**Steps:**

1.  **Build the Docker image:**
    From the root directory of the project, run:
    ```bash
    docker build -t feedback-tool .
    ```

2.  **Run the Docker container:**
    You must provide the `MONGODB_URI` as an environment variable.
    ```bash
    docker run -d -p 5000:5000 \
      -e MONGODB_URI="mongodb+srv://<user>:<password>@<cluster-url>/feedback_db?retryWrites=true&w=majority" \
      -e SESSION_SECRET="a-very-strong-secret-key-for-sessions" \
      -e JWT_SECRET_KEY="another-strong-secret-for-jwt" \
      --name feedback-app \
      feedback-tool
    ```
    - `-d`: Runs the container in the background.
    - `-p 5000:5000`: Maps port 5000 on your computer to port 5000 in the container.
    - `-e`: Sets the required environment variables.
    - `--name`: Gives your container a friendly name.

3.  **Seed the Database (First-time run):**
    After the container is running, execute the seeder script inside it:
    ```bash
    docker exec feedback-app python seed_db.py
    ```

4.  **Access the application:**
    Open your web browser and go to `http://localhost:5000`.

---

### B. Running Locally (for Development)

**Prerequisites:**
- Python 3.9+
- A running MongoDB instance (local or from [MongoDB Atlas](https://www.mongodb.com/cloud/atlas))

**Steps:**

1.  **Clone the repository:**
    ```bash
    git clone <your-repo-url>
    cd <your-repo-name>
    ```

2.  **Set up a virtual environment:**
    ```bash
    cd backend
    python -m venv .venv
    source .venv/bin/activate  # On Windows, use `.venv\Scripts\activate`
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure Environment Variables:**
    Create a file named `.env` in the `backend` directory and add the following, replacing the placeholder values:
    ```
    MONGODB_URI="mongodb+srv://<user>:<password>@<cluster-url>/feedback_db?retryWrites=true&w=majority"
    SESSION_SECRET="a-very-strong-secret-key-for-sessions"
    JWT_SECRET_KEY="another-strong-secret-for-jwt"
    ```
    *Note: The application will run without this, but it's a security best practice.*

5.  **Seed the Database:**
    Run the seeder script to populate the database with sample users and teams.
    ```bash
    python seed_db.py
    ```
    This will print the login credentials for the default accounts.

6.  **Run the Flask application:**
    ```bash
    python main.py
    ```

7.  **Access the application:**
    Open your web browser and go to `http://localhost:5000`.

## Application Structure

The project is contained within the `backend/` directory.

- `app.py`: Main Flask application setup and configuration using the App Factory pattern.
- `routes.py`: Application routes, view handlers, and main business logic.
- `auth.py`: Authentication logic and authorization decorators (`@role_required`).
- `extensions.py`: Initialization of Flask extensions (e.g., MongoEngine).
- `models.py`: MongoEngine data model definitions (User, Feedback, Team).
- `main.py`: Entry point for running the Flask development server.
- `seed_db.py`: A script to clear and populate the database with sample data.
- `templates/`: Jinja2 HTML templates for all pages.
- `static/`: Static assets (CSS, JavaScript).