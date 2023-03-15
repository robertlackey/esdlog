# Use an official Python runtime as a parent image
FROM python:3.9-alpine

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN apk add --no-cache gcc musl-dev libffi-dev openssl-dev postgresql-dev \
    && pip install --no-cache-dir -r requirements.txt \
    && apk del gcc musl-dev libffi-dev openssl-dev

# Expose port 8000 for the app
EXPOSE 8000

# Set the environment variable for Flask
ENV FLASK_APP=app.py

# Start Gunicorn
CMD ["gunicorn", "--workers", "4", "--bind", "0.0.0.0:8000", "--certfile", "/app/certs/cert.crt", "--keyfile", "/app/certs/cert.key", "wsgi:app"]
