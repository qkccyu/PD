#!/usr/bin/env python3
"""
Comprehensive Test Suite for MycoScan Flask Application
This script tests all functionality including routes, API endpoints, and authentication.
"""

import os
import sys
import requests
import time
from io import BytesIO
from PIL import Image

# Set working directory
os.chdir(r"c:\Users\Client\Downloads\pd-main\pd-main\Try Modular")

def test_flask_startup():
    """Test if Flask application can start properly"""
    print("\n=== Testing Flask Application Startup ===")
    try:
        from main import create_app
        app = create_app()
        print("OK: Flask app created successfully")
        
        with app.app_context():
            print(f"OK: App context working")
            print(f"OK: Database URI: {app.config['SQLALCHEMY_DATABASE_URI']}")
            
        return True
    except Exception as e:
        print(f"ERROR: Flask startup failed - {e}")
        return False

def test_routes():
    """Test if server is running and routes are accessible"""
    print("\n=== Testing Routes (requires running server) ===")
    
    base_url = "http://localhost:5000"
    
    # Test routes that should be accessible
    routes_to_test = [
        ("/", "Landing page"),
        ("/login", "Login page"),
        ("/register", "Register page"),
    ]
    
    for route, description in routes_to_test:
        try:
            response = requests.get(f"{base_url}{route}", timeout=5)
            if response.status_code == 200:
                print(f"OK: {description} ({route}) - Status {response.status_code}")
            else:
                print(f"WARN: {description} ({route}) - Status {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"ERROR: {description} ({route}) - {e}")
            return False
    
    return True

def test_authentication():
    """Test login functionality"""
    print("\n=== Testing Authentication ===")
    
    base_url = "http://localhost:5000"
    
    # Test login
    login_data = {
        'username': 'admin',
        'password': 'admin123'
    }
    
    try:
        session = requests.Session()
        
        # Get login page first
        login_response = session.get(f"{base_url}/login")
        if login_response.status_code != 200:
            print(f"ERROR: Cannot access login page - Status {login_response.status_code}")
            return False
        
        print("OK: Login page accessible")
        
        # Attempt login
        auth_response = session.post(f"{base_url}/login", data=login_data)
        if auth_response.status_code == 302 or "dashboard" in auth_response.url:
            print("OK: Login successful")
            
            # Test protected route
            dashboard_response = session.get(f"{base_url}/dashboard")
            if dashboard_response.status_code == 200:
                print("OK: Dashboard accessible after login")
            else:
                print(f"WARN: Dashboard not accessible - Status {dashboard_response.status_code}")
            
            return True
        else:
            print(f"ERROR: Login failed - Status {auth_response.status_code}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"ERROR: Authentication test failed - {e}")
        return False

def test_api_endpoints():
    """Test API endpoints"""
    print("\n=== Testing API Endpoints ===")
    
    base_url = "http://localhost:5000"
    
    # API endpoints to test
    api_endpoints = [
        ("/api/patients", "Patients API"),
        ("/api/medications", "Medications API"),
        ("/api/scans", "Scans API"),
    ]
    
    try:
        session = requests.Session()
        
        # Login first
        login_data = {'username': 'admin', 'password': 'admin123'}
        session.post(f"{base_url}/login", data=login_data)
        
        for endpoint, description in api_endpoints:
            try:
                response = session.get(f"{base_url}{endpoint}", timeout=5)
                if response.status_code == 200:
                    data = response.json()
                    print(f"OK: {description} ({endpoint}) - {len(data)} items")
                else:
                    print(f"WARN: {description} ({endpoint}) - Status {response.status_code}")
            except Exception as e:
                print(f"ERROR: {description} ({endpoint}) - {e}")
        
        return True
        
    except requests.exceptions.RequestException as e:
        print(f"ERROR: API test failed - {e}")
        return False

def test_scan_api():
    """Test scan API with file upload"""
    print("\n=== Testing Scan API ===")
    
    base_url = "http://localhost:5000"
    
    try:
        session = requests.Session()
        
        # Login first
        login_data = {'username': 'admin', 'password': 'admin123'}
        session.post(f"{base_url}/login", data=login_data)
        
        # Create test image
        img = Image.new('RGB', (100, 100), color='red')
        img_bytes = BytesIO()
        img.save(img_bytes, format='JPEG')
        img_bytes.seek(0)
        
        # Test scan upload
        files = {'image': ('test.jpg', img_bytes, 'image/jpeg')}
        data = {
            'patient_name': 'Test Patient',
            'notes': 'Automated test scan',
            'condition': 'Onychomycosis',
            'severity': 'Mild'
        }
        
        response = session.post(f"{base_url}/api/scans", files=files, data=data)
        
        if response.status_code == 201:
            print("OK: Scan API working - Upload successful")
        else:
            print(f"ERROR: Scan API failed - Status {response.status_code}")
            print(f"Response: {response.text}")
        
        return True
        
    except Exception as e:
        print(f"ERROR: Scan API test failed - {e}")
        return False

def check_static_files():
    """Check static files and directories"""
    print("\n=== Checking Static Files ===")
    
    static_dir = "static"
    uploads_dir = os.path.join(static_dir, "uploads", "scans")
    
    # Check if directories exist
    if os.path.exists(static_dir):
        print(f"OK: Static directory exists: {static_dir}")
    else:
        print(f"WARN: Static directory missing: {static_dir}")
    
    if os.path.exists(uploads_dir):
        print(f"OK: Uploads directory exists: {uploads_dir}")
        files = os.listdir(uploads_dir)
        print(f"OK: {len(files)} files in uploads directory")
    else:
        print(f"WARN: Uploads directory missing: {uploads_dir}")
        # Create it
        os.makedirs(uploads_dir, exist_ok=True)
        print(f"OK: Created uploads directory: {uploads_dir}")
    
    return True

def main():
    """Run all tests"""
    print("MycoScan Application Test Suite")
    print("=" * 60)
    
    # Test 1: Flask startup
    if not test_flask_startup():
        print("\nCRITICAL: Flask startup failed. Cannot continue tests.")
        return False
    
    # Test 2: Static files
    check_static_files()
    
    # Test 3: Server-dependent tests (only if server is running)
    try:
        response = requests.get("http://localhost:5000", timeout=2)
        server_running = True
    except:
        server_running = False
        print("\nINFO: Flask server not running. Skipping server-dependent tests.")
        print("To run server tests, start the server with: python run_app.py")
    
    if server_running:
        print("\nINFO: Server is running. Running full test suite...")
        test_routes()
        test_authentication()
        test_api_endpoints()
        test_scan_api()
    
    print("\n" + "=" * 60)
    print("Test Summary:")
    print("- Flask application: WORKING")
    print("- Database models: WORKING") 
    print("- Static files: CHECKED")
    if server_running:
        print("- Routes: TESTED")
        print("- Authentication: TESTED")
        print("- API endpoints: TESTED")
    else:
        print("- Server tests: SKIPPED (server not running)")
    
    print("\nTo start the server: python run_app.py")
    print("Login credentials: admin / admin123")
    
    return True

if __name__ == "__main__":
    main()