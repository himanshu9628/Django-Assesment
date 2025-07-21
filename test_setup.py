#!/usr/bin/env python3
"""
Test script to verify the project setup and basic functionality.
"""

import os
import sys
import subprocess

def test_imports():
    """Test if all required modules can be imported."""
    print("Testing imports...")
    
    try:
        import django
        print("✅ Django imported successfully")
    except ImportError as e:
        print(f"❌ Django import failed: {e}")
        return False
    
    try:
        import fastapi
        print("✅ FastAPI imported successfully")
    except ImportError as e:
        print(f"❌ FastAPI import failed: {e}")
        return False
    
    try:
        import redis
        print("✅ Redis imported successfully")
    except ImportError as e:
        print(f"❌ Redis import failed: {e}")
        return False
    
    try:
        import sqlalchemy
        print("✅ SQLAlchemy imported successfully")
    except ImportError as e:
        print(f"❌ SQLAlchemy import failed: {e}")
        return False
    
    return True

def test_django_setup():
    """Test Django project setup."""
    print("\nTesting Django setup...")
    
    # Change to Django project directory
    os.chdir('django_project')
    
    try:
        # Test Django settings
        result = subprocess.run([
            sys.executable, 'manage.py', 'check', '--deploy'
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Django project setup is valid")
            return True
        else:
            print(f"❌ Django project setup failed: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Django test failed: {e}")
        return False
    finally:
        os.chdir('..')

def test_fastapi_setup():
    """Test FastAPI project setup."""
    print("\nTesting FastAPI setup...")
    
    try:
        # Test if FastAPI app can be imported
        sys.path.append('auth_service')
        from main import app
        print("✅ FastAPI app imported successfully")
        
        # Test if models can be imported
        from models import UserCreate, UserLogin, TokenResponse
        print("✅ FastAPI models imported successfully")
        
        return True
    except Exception as e:
        print(f"❌ FastAPI test failed: {e}")
        return False

def main():
    """Run all tests."""
    print("🚀 Backend Developer Technical Assessment - Setup Test")
    print("=" * 60)
    
    # Test imports
    if not test_imports():
        print("\n❌ Import tests failed. Please install dependencies:")
        print("pip install -r requirements.txt")
        return
    
    # Test Django setup
    if not test_django_setup():
        print("\n❌ Django setup failed.")
        return
    
    # Test FastAPI setup
    if not test_fastapi_setup():
        print("\n❌ FastAPI setup failed.")
        return
    
    print("\n" + "=" * 60)
    print("✅ All tests passed! Your project is ready to run.")
    print("\nNext steps:")
    print("1. cd django_project && python manage.py migrate")
    print("2. cd auth_service && python main.py")
    print("3. Visit http://localhost:8000 for Django app")
    print("4. Visit http://localhost:8001 for FastAPI auth service")

if __name__ == "__main__":
    main() 