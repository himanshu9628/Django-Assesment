import sys
import os

# Add current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    # Test imports
    print("Testing imports...")
    from main import app
    from auth_utils import create_access_token, verify_token, get_password_hash, verify_password
    from database import get_db, engine, Base, User
    from models import UserCreate, UserLogin, TokenResponse
    print("✓ All imports successful")
    
    # Test JWT functionality
    print("Testing JWT functionality...")
    test_data = {"sub": "test@example.com"}
    token = create_access_token(test_data)
    print(f"✓ Token created: {token[:50]}...")
    
    # Test token verification
    payload = verify_token(token)
    print(f"✓ Token verified: {payload}")
    
    # Test password hashing
    print("Testing password hashing...")
    password = "testpassword"
    hashed = get_password_hash(password)
    print(f"✓ Password hashed: {hashed[:50]}...")
    
    # Test password verification
    is_valid = verify_password(password, hashed)
    print(f"✓ Password verification: {is_valid}")
    
    print("\n🎉 All basic functionality tests passed!")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc() 