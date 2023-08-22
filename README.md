# gender_model

### github link:
docker push zhangle59/gender_model_image:lastest

### api use:   
```bash
curl -X POST -H "Content-Type: application/json" -d '{"first_name": "peter"}' http://localhost:5002/api/predict_gender_v1
```