#!/usr/bin/env python3
"""
Test script to verify ML service integration
"""

import json
import time
import subprocess
import requests
import sys
import os

def test_ml_service():
    """Test the ML service functionality"""
    
    print("🔬 Testing ML Service Integration")
    print("=" * 50)
    
    # Test sample data
    test_data = {
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
    }
    
    try:
        # Start the ML service
        print("1. Starting ML service...")
        
        # Import the model server module
        sys.path.append('ml_service')
        from model_server import app, load_model, preprocess_input, PredictionInput
        
        # Load model and scaler
        print("2. Loading model and scaler...")
        files_loaded = load_model()
        
        if not files_loaded:
            print("⚠️  Model or scaler files not found")
            print("   Place your files in:")
            print("   - ml_service/liver_disease_model.pkl")  
            print("   - ml_service/standard_scaler.pkl")
        else:
            print("✅ Model and scaler loaded successfully")
        
        if files_loaded:
            # Test preprocessing only if files are loaded
            print("3. Testing data preprocessing...")
            input_data = PredictionInput(**test_data)
            try:
                features = preprocess_input(input_data)
                print(f"✅ Preprocessed features shape: {features.shape}")
                print(f"   Features: {features.flatten()}")
                
                print("\n4. Testing prediction...")
                # Direct prediction test (without HTTP)
                from model_server import predict
                import asyncio
                
                result = asyncio.run(predict(input_data))
                print(f"✅ Prediction result:")
                print(f"   Risk Score: {result.riskScore}")
                print(f"   Risk Level: {result.riskLevel}")
                print(f"   Probability: {result.probability}")
                print(f"   Confidence: {result.confidence}")
                
                print("\n🎉 ML Service integration test completed successfully!")
                
            except Exception as e:
                print(f"❌ Preprocessing/prediction failed: {e}")
                return False
        
        return files_loaded
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("   Make sure all Python dependencies are installed")
        return False
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

def test_http_service():
    """Test the HTTP service endpoint"""
    
    print("\n🌐 Testing HTTP Service")
    print("=" * 30)
    
    service_url = "http://localhost:8001"
    test_data = {
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
    }
    
    try:
        # Check if service is running
        response = requests.get(f"{service_url}/health", timeout=5)
        print(f"✅ Health check: {response.json()}")
        
        # Test prediction endpoint
        response = requests.post(f"{service_url}/predict", 
                               json=test_data, 
                               timeout=10)
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ HTTP Prediction successful:")
            print(f"   Risk Score: {result['riskScore']}")
            print(f"   Risk Level: {result['riskLevel']}")
            return True
        else:
            print(f"❌ HTTP request failed: {response.status_code}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to ML service. Is it running on port 8001?")
        return False
    except Exception as e:
        print(f"❌ HTTP test failed: {e}")
        return False

def main():
    """Main test function"""
    
    print("🧪 Liver Disease Prediction ML Integration Test")
    print("=" * 60)
    
    # Test 1: Direct Python module test
    python_test_passed = test_ml_service()
    
    # Test 2: HTTP service test (if service is running)
    http_test_passed = test_http_service()
    
    print("\n📊 Test Summary:")
    print("=" * 20)
    print(f"Python module test: {'✅ PASSED' if python_test_passed else '❌ FAILED'}")
    print(f"HTTP service test:  {'✅ PASSED' if http_test_passed else '❌ FAILED'}")
    
    if python_test_passed:
        print("\n💡 Next Steps:")
        print("1. Place your .pkl model file in ml_service/liver_disease_model.pkl")
        print("2. Adjust feature preprocessing in model_server.py if needed")
        print("3. Start both services with: python3 start_ml_service.py & npm run dev")
        print("4. Test the full application at http://localhost:5000")

if __name__ == "__main__":
    main()