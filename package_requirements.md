# Dependency Requirements

## Node.js Dependencies (Automatically Installed)

The following packages are already configured in `package.json` and installed via `npm install`:

### Frontend Dependencies
- **React & TypeScript**: `react`, `react-dom`, `typescript`
- **Build Tools**: `vite`, `@vitejs/plugin-react`
- **UI Components**: `@radix-ui/*` (various components), `lucide-react`
- **Form Handling**: `react-hook-form`, `@hookform/resolvers`
- **State Management**: `@tanstack/react-query`
- **Styling**: `tailwindcss`, `class-variance-authority`, `clsx`
- **Routing**: `wouter`
- **Validation**: `zod`, `drizzle-zod`

### Backend Dependencies
- **Server**: `express`, `@types/express`
- **Database**: `drizzle-orm`, `@neondatabase/serverless`
- **Session Management**: `express-session`, `passport`, `passport-local`
- **Development**: `tsx`, `@types/node`

## Python Dependencies (ML Service)

### Required for ML Service
```bash
# Install using the provided scripts or manually:
pip install fastapi==0.104.1
pip install "uvicorn[standard]==0.24.0"
pip install numpy==1.24.3
pip install pandas==2.0.3
pip install scikit-learn==1.3.0
pip install joblib==1.3.2
pip install requests==2.31.0
```

### Package Descriptions
- **FastAPI**: Web framework for the ML API service
- **Uvicorn**: ASGI server for running FastAPI
- **NumPy**: Numerical computing for data processing
- **Pandas**: Data manipulation and analysis
- **Scikit-learn**: Machine learning utilities and standard scaler
- **Joblib**: Loading and saving ML models (pickle files)
- **Requests**: HTTP library for testing and integration

## Installation Options

### Option 1: Automated Installation (Recommended)
```bash
# Make script executable and run
chmod +x install_dependencies.sh
./install_dependencies.sh
```

### Option 2: Python-only ML Dependencies
```bash
python3 install_ml_dependencies.py
```

### Option 3: Manual Installation
```bash
# Node.js dependencies
npm install

# Python dependencies
python3 -m pip install --user fastapi uvicorn numpy pandas scikit-learn joblib requests
```

## Required Model Files

After installing dependencies, you need to provide:

1. **Trained Model**: `ml_service/liver_disease_model.pkl`
2. **Standard Scaler**: `ml_service/standard_scaler.pkl`

## Verification

Test your installation:
```bash
# Test ML integration
python3 test_ml_integration.py

# Start services
python3 start_ml_service.py  # Terminal 1
npm run dev                  # Terminal 2
```

## Environment Requirements

- **Node.js**: 18+ (already configured in Replit)
- **Python**: 3.8+ (already available in Replit)
- **Memory**: 512MB+ for ML model loading
- **Storage**: ~100MB for all dependencies