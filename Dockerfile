FROM python:3.9.6

# Working directory
WORKDIR /app

# Copy and install requirements
COPY . /app
RUN pip install -r requirements.txt

# Exposing port 5002
EXPOSE 5002

# Start your application using gunicorn when the container runs 
CMD ["gunicorn", "--access-logfile", "-", "--error-logfile", "-", "gender_model.server:app"]