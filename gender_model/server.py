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


app.logger.addHandler(logging.StreamHandler(sys.stdout))
app.logger.addHandler(logging.StreamHandler(sys.stderr))
app.logger.setLevel(logging.DEBUG)

@app.route(f'{api_path_prefix}/health', methods=['GET'])
def check_health():
    try:
        X_pred_vec = vectorizer.transform(['peter'])
        y_pred = model.predict(X_pred_vec)
        y_pred = int(y_pred[0])
        # app.logger.info(f'predict of peter is: {y_pred}')
        # app.logger.info('dummy log for info')
        # app.logger.debug('dummy log for debug')
        # app.logger.warning('dummy log for warning')
        res = {'alive': y_pred}
        return jsonify(res)
    except Exception as e:
        # app.logger.error(f"Exception occurred: {str(e)}")
        # app.logger.error('dummy log for error')
        # app.logger.critical('dummy log for critical')
        res = {'alive': 0}
        return jsonify(res), 500

@app.route(f'{api_path_prefix}/predict_gender_v1', methods=['POST'])
def predict_gender():
    try:
        json_data = request.get_json()
        # df = pd.DataFrame(json_data, index=[0])
        df = pd.DataFrame(json_data)
        X_pred_vec = vectorizer.transform(df['first_name'].values)
        y_pred = model.predict(X_pred_vec)
        app.logger.debug(y_pred)
        predicted_genders = ['M' if pred == 1 else 'F' for pred in y_pred]
        res = {'Predict of gender': predicted_genders}
        # app.logger.info(f"predict of {df['first_name'].values} is: {predicted_genders}")
        return jsonify(res)
    except Exception as e:
        # app.logger.error(f"Exception occurred: {str(e)}")
        res = {'err': e}
        return jsonify(res), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)