from flask import Flask, request, jsonify
import pandas as pd
import joblib
import sys
from gender_model.config import Config
import logging

app = Flask(__name__)
model = joblib.load('gender_model/model/logistic_gender.pkl')
vectorizer = joblib.load('gender_model/model/countvectorizer_gender.pkl')
app.config.from_object(Config)
api_path_prefix = app.config['API_PATH_PREFIX']
api_model_version = app.config['MODEL_VERSION']

'''
# Create a custom logger
logger = logging.getLogger(__name__)
# ... Rest of your logging configuration ...
stdout_handler = logging.StreamHandler(stream=sys.stdout)
stdout_handler.setLevel(logging.INFO)
stderr_handler = logging.StreamHandler(stream=sys.stderr)
stderr_handler.setLevel(logging.WARNING)
# Define log formats
log_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
stdout_handler.setFormatter(log_format)
stderr_handler.setFormatter(log_format)
# Add the handlers to the logger based on log levels
logger.addHandler(stdout_handler)  # INFO, NOTICE, DEBUG will go to STDOUT
logger.addHandler(stderr_handler)  # WARNING, ERROR, CRITICAL will go to STDERR

# for gunicorn
logger_gunicorn = logging.getLogger('gunicorn.info')
stdout_handler_gunicorn = logging.StreamHandler(stream=sys.stdout)
stdout_handler_gunicorn.setLevel(logging.INFO)
logger_gunicorn.addHandler(stdout_handler_gunicorn)
'''

app.logger.addHandler(logging.StreamHandler(sys.stdout))
app.logger.addHandler(logging.StreamHandler(sys.stderr))
app.logger.setLevel(logging.INFO)

@app.route(f'{api_path_prefix}/health', methods=['GET'])
def check_health():
    try:
        X_pred_vec = vectorizer.transform(['peter'])
        y_pred = model.predict(X_pred_vec)
        y_pred = int(y_pred[0])
        app.logger.info(f'predict of peter is: {y_pred}')
        res = {'alive': y_pred}
        return jsonify(res)
    except Exception as e:
        app.logger.error(f"Exception occurred: {str(e)}")
        res = {'alive': 0}
        return jsonify(res), 500

@app.route(f'{api_path_prefix}/predict_gender_v1', methods=['POST'])
def predict_gender():
    try:
        json_data = request.get_json()
        df = pd.DataFrame(json_data, index=[0])
        X_pred_vec = vectorizer.transform(df['first_name'].values)
        y_pred = model.predict(X_pred_vec)
        predicted_genders = ['M' if pred == 1 else 'F' for pred in y_pred]
        res = {'Predict of gender': predicted_genders}
        app.logger.info(f"predict of {df['first_name'].values} is: {predicted_genders}")
        return jsonify(res)
    except Exception as e:
        app.logger.error(f"Exception occurred: {str(e)}")
        res = {'err': e}
        return jsonify(res), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)