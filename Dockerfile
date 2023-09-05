FROM python:3.9.6

# Working directory
WORKDIR /app

# Copy and install requirements
COPY . /app
RUN pip install -r requirements.txt

# Exposing port 5002
EXPOSE 5002
# start docker
# CMD ["gunicorn", "--bind", "0.0.0.0:5002", "--capture-output", "gender_model.server:app"]
CMD ["gunicorn", "--bind", "0.0.0.0:5002", "--capture-output", "--log-file", "-", "gender_model.server:app"]
