import xgboost as xgb
from flask import Flask, request, jsonify
import pandas as pd
from util import data_util  # You need to import data_util if it's defined in a separate file
import joblib

app = Flask(__name__)

@app.route('/predict_gender', methods=['POST'])
def predict_gender():
    json_data = request.get_json()

    model = joblib.load('./model/gender_model.pkl')
    vectorizer = joblib.load('./model/gender_vectorizer.pkl')
    df = pd.DataFrame(json_data, index=[0])

    X_pred_vec = vectorizer.transform(df['first_name'].values)
    y_pred = model.predict(X_pred_vec)

    predicted_genders = ['M' if pred == 1 else 'F' for pred in y_pred]
    res = {'Predict of gender': predicted_genders}
    return jsonify(res)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)