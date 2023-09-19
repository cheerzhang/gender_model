from flask import Flask, request, jsonify, render_template
import pandas as pd
import joblib
import sys
from gender_model.config import Config, config_Logger
from flask_restx import Api, Resource, fields, Namespace

app = Flask(__name__)
model = joblib.load('gender_model/model/logistic_gender.pkl')
vectorizer = joblib.load('gender_model/model/countvectorizer_gender.pkl')
app.config.from_object(Config)
api_path_prefix = app.config['API_PATH_PREFIX']
api_model_version = app.config['MODEL_VERSION']
logger = config_Logger(app.logger).config_level()

@app.route('/', methods=['GET'])
def index():
    return render_template('home_page.html')


api = Api(
    app, 
    version='1.0', 
    title='Gender Predict',
    description='Predict the gender base on first name',
    doc='/api/doc'
)
ns = api.namespace('Gender V1', description='Predict the gender base on first name')



input_model = api.model('InputModel', {
    'first_name': fields.String(description='First name for gender prediction')
})
prediction_model = api.model('PredictionModel', {
    "Predict of gender": fields.List(fields.String(default=''), description='Predicted gender', as_list=True)
})
@api.route(f'{api_path_prefix}/predict_gender_v1', methods=['POST'])
class PredictGender(Resource):
    @api.doc(params={'data': 'List of objects with first_name'})
    @api.expect([input_model], validate=True)
    @api.marshal_with(prediction_model)
    def post(self):
        try:
            json_data = request.get_json()
            df = pd.DataFrame(json_data)
            X_pred_vec = vectorizer.transform(df['first_name'].values)
            y_pred = model.predict(X_pred_vec)
            predicted_genders = ['M' if pred == 1 else 'F' for pred in y_pred]
            logger.info(f"predict gender of {df['first_name'].values} is: {predicted_genders}")
            res = {'gender': predicted_genders}
            return res
        except Exception as e:
            res = {'error': str(e)}
            return jsonify(res), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)