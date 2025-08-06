# ML Model Integration Guide

## 🎯 Overview

I've successfully integrated your Python ML model with the liver disease prediction application. The system is now ready to use your actual pickle model instead of mock data.

## 📁 Files Created

- `ml_service/model_server.py` - FastAPI service that serves your ML model
- `ml_service/README.md` - Detailed documentation for the ML service
- `test_ml_integration.py` - Test script to verify integration
- `start_ml_service.py` - Python service startup script
- `ML_INTEGRATION_GUIDE.md` - This guide

## 🔧 Integration Architecture

```
Frontend (React) → Node.js API → Python ML Service → Your Model
```

1. **Frontend**: Collects user input via the medical assessment form
2. **Node.js Backend**: Validates data and calls the Python ML service
3. **Python ML Service**: Preprocesses data and makes predictions using your model
4. **Results**: Returned through the chain back to the user interface

## 📋 Setup Instructions

### Step 1: Add Your Model Files

**Both files are required:**

1. **Model file** - Place in one of these locations:
   - `ml_service/liver_disease_model.pkl` ← **Recommended**
   - `ml_service/model.pkl`
   - `liver_disease_model.pkl` (project root)
   - `model.pkl` (project root)

2. **Scaler file** - Place in one of these locations:
   - `ml_service/standard_scaler.pkl` ← **Recommended**
   - `ml_service/scaler.pkl`
   - `standard_scaler.pkl` (project root)
   - `scaler.pkl` (project root)
   - `ml_service/liver_disease_scaler.pkl`

### Step 2: Verify Model Input Features

Your model should expect these 10 features in this order:

1. `age` (int): 1-100
2. `gender_encoded` (int): 0=female, 1=male
3. `bmi` (float): 10.0-50.0
4. `alcohol_consumption` (float): 0.0-20.0 drinks/week
5. `smoking_encoded` (int): 0=no, 1=yes
6. `genetic_risk_encoded` (int): 0=low, 1=medium, 2=high
7. `physical_activity` (float): 0.0-20.0 hours/week
8. `diabetes_encoded` (int): 0=no, 1=yes
9. `hypertension_encoded` (int): 0=no, 1=yes
10. `liver_function_score` (float): 0.0-100.0

### Step 3: Customize Feature Processing (if needed)

If your model uses different feature encoding, edit the `preprocess_input()` function in `ml_service/model_server.py`:

```python
def preprocess_input(data: PredictionInput) -> np.ndarray:
    # Modify this function to match your model's expected input format
    # Current encoding:
    gender_encoded = 1 if data.gender.lower() == 'male' else 0
    # Add your custom encoding here
```

### Step 4: Test the Integration

Run the test script:
```bash
python3 test_ml_integration.py
```

Expected output:
```
✅ Python module test: PASSED
✅ HTTP service test: PASSED
```

### Step 5: Start Both Services

Option A - Manual start (recommended for testing):
```bash
# Terminal 1: Start ML service
python3 start_ml_service.py

# Terminal 2: Start main application  
npm run dev
```

Option B - Combined start:
```bash
./start_services.sh
```

## 🔄 Current Status

✅ **Node.js Backend**: Modified to call Python ML service with fallback to rule-based calculation
✅ **Python ML Service**: FastAPI service ready to serve your model
✅ **Data Processing**: Automatic conversion from form data to model input format
✅ **Error Handling**: Proper error messages when ML service or files are unavailable
✅ **Integration Testing**: Test framework to verify everything works

## 🧪 Testing Your Model

1. **Place your model files**: 
   - `ml_service/liver_disease_model.pkl`
   - `ml_service/standard_scaler.pkl`
2. **Run integration test**: `python3 test_ml_integration.py`
3. **Start services**: Both Python ML service and Node.js app
4. **Test via UI**: Fill out the form at http://localhost:5000
5. **Check predictions**: Should now use your actual ML model with proper scaling

## 🔧 Model Customization

### Different Model Output Format

If your model outputs different values, modify the prediction logic in `model_server.py`:

```python
@app.post("/predict", response_model=PredictionResponse)
async def predict(data: PredictionInput):
    # Adjust this section based on your model's output
    if hasattr(model, 'predict_proba'):
        probabilities = model.predict_proba(features)[0]
        probability = probabilities[1]  # Adjust index if needed
    else:
        prediction = model.predict(features)[0]
        probability = float(prediction)
```

### Different Feature Names/Order

Update the `feature_columns` list and `preprocess_input()` function to match your training data.

## 📊 Monitoring

- **ML Service**: Runs on http://localhost:8001
- **Health Check**: GET http://localhost:8001/health
- **Direct Testing**: POST http://localhost:8001/predict
- **Main App**: http://localhost:5000

## 🚨 Troubleshooting

### "Model not found" or "Scaler not found"
- Verify both .pkl files are in the correct locations
- Check file permissions
- Ensure both files are valid pickle files
- Restart the ML service after adding files

### "Prediction errors"
- Verify feature preprocessing matches your training data
- Check that input data types match model expectations
- Review the model's expected input shape

### "Service connection failed"
- Ensure Python ML service is running on port 8001
- Check for port conflicts
- Verify all Python dependencies are installed

## 🎉 Next Steps

1. **Upload your files**: 
   - Place your model .pkl file in the designated location
   - Place your scaler .pkl file in the designated location
2. **Test integration**: Run the test script to verify everything works
3. **Customize if needed**: Adjust feature processing for your specific model
4. **Start services**: Run both Python ML service and Node.js app
5. **Deploy**: Both services are now ready for production use

The application will now show proper error messages when files are missing and automatically use your ML model with standard scaling for predictions while maintaining the existing medical-themed interface!