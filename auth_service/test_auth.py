import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import Base, get_db
from main import app
import os

# Test database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

@pytest.fixture(autoscope="function")
def setup_database():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

def test_signup_success(setup_database):
    """Test successful user signup"""
    response = client.post("/auth/signup", json={
        "email": "test@example.com",
        "password": "password123",
        "full_name": "Test User"
    })
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["email"] == "test@example.com"
    assert data["token_type"] == "bearer"

def test_signup_duplicate_email(setup_database):
    """Test signup with existing email"""
    # First signup
    client.post("/auth/signup", json={
        "email": "test@example.com",
        "password": "password123",
        "full_name": "Test User"
    })
    
    # Second signup with same email
    response = client.post("/auth/signup", json={
        "email": "test@example.com",
        "password": "password456",
        "full_name": "Another User"
    })
    assert response.status_code == 400
    assert "Email already registered" in response.json()["detail"]

def test_login_success(setup_database):
    """Test successful login"""
    # Create user first
    client.post("/auth/signup", json={
        "email": "test@example.com",
        "password": "password123",
        "full_name": "Test User"
    })
    
    # Login
    response = client.post("/auth/login", json={
        "email": "test@example.com",
        "password": "password123"
    })
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["email"] == "test@example.com"

def test_login_invalid_credentials(setup_database):
    """Test login with invalid credentials"""
    response = client.post("/auth/login", json={
        "email": "test@example.com",
        "password": "wrongpassword"
    })
    assert response.status_code == 401
    assert "Incorrect email or password" in response.json()["detail"]

def test_protected_endpoint_with_valid_token(setup_database):
    """Test accessing protected endpoint with valid token"""
    # Create user and get token
    signup_response = client.post("/auth/signup", json={
        "email": "test@example.com",
        "password": "password123",
        "full_name": "Test User"
    })
    token = signup_response.json()["access_token"]
    
    # Access protected endpoint
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/auth/me", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "test@example.com"
    assert data["full_name"] == "Test User"

def test_protected_endpoint_without_token(setup_database):
    """Test accessing protected endpoint without token"""
    response = client.get("/auth/me")
    assert response.status_code == 403

def test_protected_endpoint_with_invalid_token(setup_database):
    """Test accessing protected endpoint with invalid token"""
    headers = {"Authorization": "Bearer invalid_token"}
    response = client.get("/auth/me", headers=headers)
    assert response.status_code == 401

def test_verify_token_endpoint(setup_database):
    """Test token verification endpoint"""
    # Create user and get token
    signup_response = client.post("/auth/signup", json={
        "email": "test@example.com",
        "password": "password123",
        "full_name": "Test User"
    })
    token = signup_response.json()["access_token"]
    
    # Verify token
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/auth/verify", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["valid"] == True
    assert data["user_email"] == "test@example.com"

def test_google_login_initiation(setup_database):
    """Test Google OAuth2 login initiation"""
    response = client.get("/auth/google")
    assert response.status_code == 200
    data = response.json()
    assert "auth_url" in data
    assert "accounts.google.com" in data["auth_url"]

def test_invalid_email_format(setup_database):
    """Test signup with invalid email format"""
    response = client.post("/auth/signup", json={
        "email": "invalid-email",
        "password": "password123",
        "full_name": "Test User"
    })
    assert response.status_code == 422  # Validation error

def test_short_password(setup_database):
    """Test signup with short password"""
    response = client.post("/auth/signup", json={
        "email": "test@example.com",
        "password": "123",
        "full_name": "Test User"
    })
    assert response.status_code == 422  # Validation error

def test_missing_required_fields(setup_database):
    """Test signup with missing required fields"""
    response = client.post("/auth/signup", json={
        "email": "test@example.com"
        # Missing password and full_name
    })
    assert response.status_code == 422  # Validation error

if __name__ == "__main__":
    pytest.main([__file__]) 