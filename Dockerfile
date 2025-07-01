# Step 1: Use an official Python runtime as a parent image
# python:3.11-slim is a good choice for being lightweight and modern.
FROM python:3.11-slim

# Step 2: Set the working directory inside the container
WORKDIR /app

# Step 3: Copy the requirements file into the container
# We copy this first to leverage Docker's layer caching. If requirements.txt
# doesn't change, this layer won't be rebuilt, speeding up subsequent builds.
COPY backend/requirements.txt .

# Step 4: Install any needed packages specified in requirements.txt
# --no-cache-dir keeps the image size smaller
RUN pip install --no-cache-dir -r requirements.txt

# Step 5: Copy the rest of the backend application code into the container
COPY backend/ .

# Step 6: Inform Docker that the container listens on port 5000
EXPOSE 5000

# Step 7: Set environment variables for best practices with Python in Docker
ENV PYTHONUNBUFFERED=1

# Step 8: Define the command to run the application using a production WSGI server
# Gunicorn is a standard for production Flask apps.
# It looks for the 'app' variable inside the 'main.py' file.
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "main:app"]
CMD ["python", "seed_db.py"]