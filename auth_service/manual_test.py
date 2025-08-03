import requests
import json
import time

# Base URL for the authentication service
BASE_URL = "http://localhost:8000"

def test_signup():
    """Test user signup"""
    print("Testing user signup...")
    
    signup_data = {
        "email": "test@example.com",
        "password": "password123",
        "full_name": "Test User"
    }
    
    response = requests.post(f"{BASE_URL}/auth/signup", json=signup_data)
    print(f"Signup Status Code: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"Signup successful! User ID: {data['user_id']}")
        print(f"Token: {data['access_token'][:50]}...")
        return data['access_token']
    else:
        print(f"Signup failed: {response.text}")
        return None

def test_login():
    """Test user login"""
    print("\nTesting user login...")
    
    login_data = {
        "email": "test@example.com",
        "password": "password123"
    }
    
    response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
    print(f"Login Status Code: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"Login successful! User ID: {data['user_id']}")
        print(f"Token: {data['access_token'][:50]}...")
        return data['access_token']
    else:
        print(f"Login failed: {response.text}")
        return None

def test_protected_endpoint(token):
    """Test accessing protected endpoint"""
    print("\nTesting protected endpoint...")
    
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/auth/me", headers=headers)
    print(f"Protected Endpoint Status Code: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"User info: {data}")
    else:
        print(f"Protected endpoint failed: {response.text}")

def test_token_verification(token):
    """Test token verification"""
    print("\nTesting token verification...")
    
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/auth/verify", headers=headers)
    print(f"Token Verification Status Code: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"Token verification: {data}")
    else:
        print(f"Token verification failed: {response.text}")

def test_google_oauth_initiation():
    """Test Google OAuth initiation"""
    print("\nTesting Google OAuth initiation...")
    
    response = requests.get(f"{BASE_URL}/auth/google")
    print(f"Google OAuth Status Code: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"Google OAuth URL: {data['auth_url']}")
    else:
        print(f"Google OAuth failed: {response.text}")

def test_invalid_token():
    """Test with invalid token"""
    print("\nTesting with invalid token...")
    
    headers = {"Authorization": "Bearer invalid_token"}
    response = requests.get(f"{BASE_URL}/auth/me", headers=headers)
    print(f"Invalid Token Status Code: {response.status_code}")
    
    if response.status_code == 401:
        print("Correctly rejected invalid token")
    else:
        print(f"Unexpected response: {response.text}")

def main():
    print("=== Authentication Service Test ===")
    
    # Test signup
    token = test_signup()
    
    if token:
        # Test protected endpoint
        test_protected_endpoint(token)
        
        # Test token verification
        test_token_verification(token)
        
        # Test login
        login_token = test_login()
        if login_token:
            test_protected_endpoint(login_token)
    
    # Test Google OAuth initiation
    test_google_oauth_initiation()
    
    # Test invalid token
    test_invalid_token()
    
    print("\n=== Test Complete ===")

if __name__ == "__main__":
    main() 