#!/usr/bin/env python3
"""
Machine Learning Model Server for Liver Disease Prediction
Serves a scikit-learn model via FastAPI
"""

import os
import joblib
import numpy as np
import pandas as pd
from typing import Dict, List, Any
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn

# Initialize FastAPI app
app = FastAPI(title="Liver Disease Prediction API", version="1.0.0")

# Global model variables
model = None
scaler = None
feature_columns = None

class PredictionInput(BaseModel):
    """Input schema for prediction requests"""
    age: int
    gender: str  # 'male' or 'female'
    bmi: float
    alcoholConsumption: float
    smoking: str  # 'yes' or 'no'
    geneticRisk: str  # 'low', 'medium', 'high'
    physicalActivity: float
    diabetes: str  # 'yes' or 'no'
    hypertension: str  # 'yes' or 'no'
    liverFunctionScore: float

class PredictionResponse(BaseModel):
    """Response schema for predictions"""
    riskScore: float
    riskLevel: str
    probability: float
    confidence: float

def load_model():
    """Load the trained model and scaler from pickle files"""
    global model, scaler, feature_columns
    
    # Look for model files in common locations
    model_paths = [
        "liver_disease_model.pkl",
        "model.pkl",
        "ml_service/liver_disease_model.pkl",
        "ml_service/model.pkl"
    ]
    
    scaler_paths = [
        "standard_scaler.pkl",
        "scaler.pkl",
        "ml_service/standard_scaler.pkl",
        "ml_service/scaler.pkl",
        "liver_disease_scaler.pkl",
        "ml_service/liver_disease_scaler.pkl"
    ]
    
    # Load model
    model_path = None
    for path in model_paths:
        if os.path.exists(path):
            model_path = path
            break
    
    if not model_path:
        print("Error: No model file found. ML service requires a trained model.")
        print(f"Searched paths: {model_paths}")
        print("Please place your model file in one of the above locations.")
        return False
    
    # Load scaler
    scaler_path = None
    for path in scaler_paths:
        if os.path.exists(path):
            scaler_path = path
            break
    
    if not scaler_path:
        print("Error: No scaler file found. ML service requires the standard scaler.")
        print(f"Searched paths: {scaler_paths}")
        print("Please place your scaler file in one of the above locations.")
        return False
    
    try:
        # Load model
        model = joblib.load(model_path)
        print(f"Model loaded successfully from {model_path}")
        
        # Load scaler
        scaler = joblib.load(scaler_path)
        print(f"Scaler loaded successfully from {scaler_path}")
        
        # Try to load feature columns if available
        feature_path = model_path.replace('.pkl', '_features.pkl')
        if os.path.exists(feature_path):
            feature_columns = joblib.load(feature_path)
            print(f"Feature columns loaded from {feature_path}")
        else:
            # Default feature order (you may need to adjust this based on your model)
            feature_columns = [
                'age', 'gender_encoded', 'bmi', 'alcohol_consumption',
                'smoking_encoded', 'genetic_risk_encoded', 'physical_activity',
                'diabetes_encoded', 'hypertension_encoded', 'liver_function_score'
            ]
            print("Using default feature columns")
        
        return True
    except Exception as e:
        print(f"Error loading model or scaler: {e}")
        return False

def preprocess_input(data: PredictionInput) -> np.ndarray:
    """Preprocess input data to match model's expected format"""
    
    if scaler is None:
        raise ValueError("Scaler not loaded. Cannot preprocess data.")
    
    # Convert categorical variables to numeric (adjust based on your model's encoding)
    gender_encoded = 1 if data.gender.lower() == 'male' else 0
    smoking_encoded = 1 if data.smoking.lower() == 'yes' else 0
    diabetes_encoded = 1 if data.diabetes.lower() == 'yes' else 0
    hypertension_encoded = 1 if data.hypertension.lower() == 'yes' else 0
    
    # Encode genetic risk (adjust based on your model)
    genetic_risk_map = {'low': 0, 'medium': 1, 'high': 2}
    genetic_risk_encoded = genetic_risk_map.get(data.geneticRisk.lower(), 1)
    
    # Create feature array (adjust order based on your model's training data)
    features = [
        data.age,
        gender_encoded,
        data.bmi,
        data.alcoholConsumption,
        smoking_encoded,
        genetic_risk_encoded,
        data.physicalActivity,
        diabetes_encoded,
        hypertension_encoded,
        data.liverFunctionScore
    ]
    
    # Convert to numpy array and scale features
    features_array = np.array(features).reshape(1, -1)
    scaled_features = scaler.transform(features_array)
    
    return scaled_features

def calculate_risk_level(probability: float) -> str:
    """Convert probability to risk level"""
    if probability < 0.3:
        return 'low'
    elif probability < 0.6:
        return 'medium'
    else:
        return 'high'

@app.on_event("startup")
async def startup_event():
    """Load model on startup"""
    load_model()

@app.get("/")
async def root():
    """Health check endpoint"""
    return {"message": "Liver Disease Prediction API is running"}

@app.get("/health")
async def health_check():
    """Detailed health check"""
    return {
        "status": "healthy",
        "model_loaded": model is not None,
        "scaler_loaded": scaler is not None,
        "feature_count": len(feature_columns) if feature_columns else 0,
        "ready_for_predictions": model is not None and scaler is not None
    }

@app.post("/predict", response_model=PredictionResponse)
async def predict(data: PredictionInput):
    """Make prediction using the loaded model"""
    
    if model is None:
        raise HTTPException(
            status_code=503, 
            detail="ML model not loaded. Please ensure model file is available and restart the service."
        )
    
    if scaler is None:
        raise HTTPException(
            status_code=503, 
            detail="Standard scaler not loaded. Please ensure scaler file is available and restart the service."
        )
    
    try:
        # Preprocess input (includes scaling)
        features = preprocess_input(data)
        
        # Make prediction
        if hasattr(model, 'predict_proba'):
            # For classification models with probability output
            probabilities = model.predict_proba(features)[0]
            # Assume binary classification: [no_disease, has_disease]
            probability = probabilities[1] if len(probabilities) > 1 else probabilities[0]
        else:
            # For regression models or classifiers without predict_proba
            prediction = model.predict(features)[0]
            probability = float(prediction)
        
        # Calculate risk score (0-100)
        risk_score = min(100, max(0, probability * 100))
        risk_level = calculate_risk_level(probability)
        
        # Calculate confidence (you may want to implement a more sophisticated method)
        confidence = 0.85  # Default confidence
        if hasattr(model, 'predict_proba'):
            # Use probability spread as confidence measure
            max_prob = max(probabilities)
            confidence = max_prob if max_prob > 0.5 else 1 - max_prob
        
        return PredictionResponse(
            riskScore=risk_score,
            riskLevel=risk_level,
            probability=probability,
            confidence=confidence
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction error: {str(e)}")

@app.post("/batch_predict")
async def batch_predict(data_list: List[PredictionInput]):
    """Make predictions for multiple inputs"""
    results = []
    for data in data_list:
        try:
            result = await predict(data)
            results.append(result)
        except Exception as e:
            results.append({"error": str(e)})
    
    return {"predictions": results}


@app.get("/ping", include_in_schema=False)
@app.head("/ping", include_in_schema=False)
def ping():
    return {"message": "pong"}


if __name__ == "__main__":
    # Load model on startup
    load_model()
    
    # Start the server
    uvicorn.run(app, host="0.0.0.0", port=8001, reload=True)
