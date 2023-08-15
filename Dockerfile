FROM python:3.9.6

# working directory
WORKDIR /app
# install requirements.txt file
RUN pip install -r requirements.txt

# copy file
ADD ./model ./model
ADD server.py server.py

# Exposing port 5001
EXPOSE 5001
# start docker
CMD ['gunicorn', '--bind', '0.0.0.0:5001', 'server:app']