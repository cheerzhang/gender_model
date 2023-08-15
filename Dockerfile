FROM python:3.9.6

# Working directory
WORKDIR /app

# Copy and install requirements
COPY requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt

# Copy remaining files
COPY ./model /app/model
COPY server.py /app/server.py

# Exposing port 5001
EXPOSE 5001
# start docker
CMD gunicorn --bind 0.0.0.0:5001 server:app