#!/bin/bash

# Liver Disease Prediction App - Dependency Installation Script
# This script installs all required dependencies for both Node.js and Python services

set -e  # Exit on any error

echo "🚀 Installing Liver Disease Prediction App Dependencies"
echo "===================================================="

# Check if we're in a Replit environment
if [ -n "$REPL_ID" ]; then
    echo "✓ Detected Replit environment"
else
    echo "ℹ️  Running in local environment"
fi

echo ""
echo "📦 Installing Node.js Dependencies..."
echo "-----------------------------------"

# Install Node.js dependencies
if command -v npm &> /dev/null; then
    echo "Installing frontend and backend packages..."
    npm install
    echo "✓ Node.js dependencies installed successfully"
else
    echo "❌ npm not found. Please install Node.js first."
    exit 1
fi

echo ""
echo "🐍 Installing Python Dependencies..."
echo "----------------------------------"

# Check if Python is available
if command -v python3 &> /dev/null; then
    echo "Python 3 found: $(python3 --version)"
    
    # Install Python dependencies using pip
    echo "Installing ML service dependencies..."
    
    # Core dependencies for ML service
    python3 -m pip install --user fastapi==0.104.1
    python3 -m pip install --user "uvicorn[standard]==0.24.0"
    python3 -m pip install --user numpy==1.24.3
    python3 -m pip install --user pandas==2.0.3
    python3 -m pip install --user scikit-learn==1.3.0
    python3 -m pip install --user joblib==1.3.2
    python3 -m pip install --user requests==2.31.0
    
    echo "✓ Python dependencies installed successfully"
else
    echo "❌ Python 3 not found. Please install Python 3 first."
    exit 1
fi

echo ""
echo "🔧 Verifying Installation..."
echo "-------------------------"

# Test Node.js dependencies
echo "Testing Node.js setup..."
if npm list express &> /dev/null; then
    echo "✓ Express.js is available"
else
    echo "⚠️  Express.js may not be properly installed"
fi

# Test Python dependencies  
echo "Testing Python ML dependencies..."
python3 -c "
try:
    import fastapi, uvicorn, numpy, pandas, sklearn, joblib, requests
    print('✓ All Python ML dependencies are available')
except ImportError as e:
    print(f'⚠️  Missing Python dependency: {e}')
"

echo ""
echo "📋 Installation Summary"
echo "====================="
echo "Required files for ML service:"
echo "  • ml_service/liver_disease_model.pkl (your trained model)"
echo "  • ml_service/standard_scaler.pkl (your scaler)"
echo ""
echo "To start the application:"
echo "  1. Place your model files in ml_service/ directory"
echo "  2. Start ML service: python3 start_ml_service.py"
echo "  3. Start main app: npm run dev"
echo ""
echo "To test the integration:"
echo "  • Run: python3 test_ml_integration.py"
echo ""
echo "🎉 Dependency installation complete!"