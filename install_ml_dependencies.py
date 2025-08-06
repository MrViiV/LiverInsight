#!/usr/bin/env python3
"""
ML Dependencies Installer for Liver Disease Prediction App
This script installs all required Python packages for the ML service.
"""

import subprocess
import sys
import importlib.util

def check_package(package_name):
    """Check if a package is already installed"""
    spec = importlib.util.find_spec(package_name)
    return spec is not None

def install_package(package):
    """Install a package using pip"""
    try:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '--user', package])
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install {package}: {e}")
        return False

def main():
    print("🐍 ML Service Dependencies Installer")
    print("===================================")
    
    # Required packages for ML service
    ml_packages = [
        ('fastapi', 'fastapi==0.104.1'),
        ('uvicorn', 'uvicorn[standard]==0.24.0'),
        ('numpy', 'numpy==1.24.3'),
        ('pandas', 'pandas==2.0.3'),
        ('sklearn', 'scikit-learn==1.3.0'),
        ('joblib', 'joblib==1.3.2'),
        ('requests', 'requests==2.31.0')
    ]
    
    print(f"Python version: {sys.version}")
    print(f"Installing {len(ml_packages)} packages...\n")
    
    installed_count = 0
    failed_packages = []
    
    for package_name, package_spec in ml_packages:
        print(f"📦 Processing {package_name}...")
        
        if check_package(package_name):
            print(f"✓ {package_name} is already installed")
            installed_count += 1
        else:
            print(f"Installing {package_spec}...")
            if install_package(package_spec):
                print(f"✓ {package_name} installed successfully")
                installed_count += 1
            else:
                failed_packages.append(package_name)
        print()
    
    # Summary
    print("📊 Installation Summary")
    print("=====================")
    print(f"✓ Successfully installed/verified: {installed_count}/{len(ml_packages)}")
    
    if failed_packages:
        print(f"❌ Failed to install: {', '.join(failed_packages)}")
        print("\nTry installing manually:")
        for pkg in failed_packages:
            matching_spec = next(spec for name, spec in ml_packages if name == pkg)
            print(f"  pip install {matching_spec}")
    
    # Test imports
    print("\n🧪 Testing imports...")
    try:
        import fastapi
        import uvicorn
        import numpy
        import pandas
        import sklearn
        import joblib
        import requests
        print("✅ All ML dependencies are working correctly!")
    except ImportError as e:
        print(f"⚠️  Import test failed: {e}")
        return False
    
    print("\n🎉 ML service dependencies are ready!")
    print("\nNext steps:")
    print("1. Place your model files:")
    print("   • ml_service/liver_disease_model.pkl")
    print("   • ml_service/standard_scaler.pkl")
    print("2. Test the setup: python3 test_ml_integration.py")
    print("3. Start ML service: python3 start_ml_service.py")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)