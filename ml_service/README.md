# ML Service Integration

This directory contains the Python machine learning service for liver disease prediction.

## Setup

1. **Place your model file** in one of these locations:
   - `ml_service/liver_disease_model.pkl` (recommended)
   - `ml_service/model.pkl`
   - `liver_disease_model.pkl` (project root)
   - `model.pkl` (project root)

2. **Place your scaler file** in one of these locations:
   - `ml_service/standard_scaler.pkl` (recommended)
   - `ml_service/scaler.pkl`
   - `standard_scaler.pkl` (project root)
   - `scaler.pkl` (project root)
   - `ml_service/liver_disease_scaler.pkl`

3. **Optional: Feature columns file**
   If your model requires specific feature ordering, save the feature names as:
   - `ml_service/liver_disease_model_features.pkl`
   - Or update the `feature_columns` list in `model_server.py`

## Required Files

Both files are **required** for the ML service to work:
- **Model file (.pkl)**: Your trained machine learning model
- **Scaler file (.pkl)**: Standard scaler used during training

## Model Requirements

Your pickle model should expect these features in this order (adjust in `model_server.py` if needed):

1. `age` (int): Patient age (1-100)
2. `gender_encoded` (int): 0 = female, 1 = male  
3. `bmi` (float): Body Mass Index (10-50)
4. `alcohol_consumption` (float): Drinks per week (0-20)
5. `smoking_encoded` (int): 0 = no, 1 = yes
6. `genetic_risk_encoded` (int): 0 = low, 1 = medium, 2 = high
7. `physical_activity` (float): Hours per week (0-20)
8. `diabetes_encoded` (int): 0 = no, 1 = yes  
9. `hypertension_encoded` (int): 0 = no, 1 = yes
10. `liver_function_score` (float): Score 0-100

## Running the Service

The ML service runs automatically with the main application. It serves on port 8001.

### Manual Testing

```bash
# Test the service directly
curl -X POST "http://localhost:8001/predict" \
-H "Content-Type: application/json" \
-d '{
  "age": 45,
  "gender": "male", 
  "bmi": 28.5,
  "alcoholConsumption": 10,
  "smoking": "yes",
  "geneticRisk": "medium",
  "physicalActivity": 3,
  "diabetes": "no", 
  "hypertension": "yes",
  "liverFunctionScore": 65
}'
```

## Customization

If your model has different:
- **Feature encoding**: Update `preprocess_input()` function
- **Output format**: Update the prediction logic in `/predict` endpoint
- **Feature order**: Update `feature_columns` list
- **Risk thresholds**: Update `calculate_risk_level()` function

## Troubleshooting

1. **Model not found**: Check file paths and ensure your .pkl file is in the correct location
2. **Prediction errors**: Verify your model expects the same features as defined in `preprocess_input()`
3. **Port conflicts**: Change port 8001 in both `model_server.py` and the Node.js service call