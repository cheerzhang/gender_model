from flask import Flask, request, jsonify
import pandas as pd
import joblib
from gender_model.config import Config

app = Flask(__name__)
model = joblib.load('gender_model/model/gender_model.pkl')
vectorizer = joblib.load('gender_model/model/gender_vectorizer.pkl')
app.config.from_object(Config)
api_path_prefix = app.config['API_PATH_PREFIX']

@app.route(f'{api_path_prefix}/health', methods=['GET'])
def check_health():
    res = {'alive': 1}  # Convert the prediction to a list
    return jsonify(res)

@app.route(f'{api_path_prefix}/predict_gender', methods=['POST'])
def predict_gender():
    json_data = request.get_json()

    df = pd.DataFrame(json_data, index=[0])

    X_pred_vec = vectorizer.transform(df['first_name'].values)
    y_pred = model.predict(X_pred_vec)

    predicted_genders = ['M' if pred == 1 else 'F' for pred in y_pred]
    res = {'Predict of gender': predicted_genders}
    return jsonify(res)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)  