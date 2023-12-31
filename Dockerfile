FROM python:3.9-slim

# Working directory
WORKDIR /app

# Copy and install requirements
COPY . /app
RUN pip install -r requirements.txt

# Exposing port 5002
EXPOSE 5002

# Start your application using gunicorn when the container runs 
CMD gunicorn -b 0.0.0.0:5002 --access-logfile '-' --error-logfile '-' gender_model.server:app