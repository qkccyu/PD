#!/usr/bin/env python3
"""
Test Login Credentials
This script tests if the login credentials work correctly outside of the web interface.
"""

from main import create_app
from models import User
from extensions import db

def test_login():
    app = create_app()
    with app.app_context():
        print("🔍 Testing Login Credentials")
        print("=" * 40)
        
        # Test credentials
        test_username = "admin"
        test_password = "admin123"
        
        print(f"Testing username: '{test_username}'")
        print(f"Testing password: '{test_password}'")
        print()
        
        # Find user
        user = User.query.filter_by(username=test_username).first()
        
        if not user:
            print("❌ User not found!")
            return False
        
        print(f"✅ User found: {user.username}")
        print(f"   Email: {user.email}")
        print(f"   Active: {user.is_active}")
        print(f"   ID: {user.id}")
        print()
        
        # Test password
        is_valid = user.check_password(test_password)
        
        if is_valid:
            print("✅ Password is CORRECT!")
            print("🎉 Login should work!")
            return True
        else:
            print("❌ Password is INCORRECT!")
            print("🔧 Try recreating the admin user")
            return False

def recreate_admin():
    app = create_app()
    with app.app_context():
        print("\n🔧 Recreating Admin User")
        print("=" * 30)
        
        # Delete existing admin user
        existing_admin = User.query.filter_by(username='admin').first()
        if existing_admin:
            db.session.delete(existing_admin)
            print("🗑️  Deleted existing admin user")
        
        # Create new admin user
        new_admin = User(
            username='admin',
            email='admin@mycoscan.com'
        )
        new_admin.set_password('admin123')
        
        try:
            db.session.add(new_admin)
            db.session.commit()
            print("✅ New admin user created!")
            print("Username: admin")
            print("Password: admin123")
            return True
        except Exception as e:
            db.session.rollback()
            print(f"❌ Error creating admin user: {e}")
            return False

if __name__ == "__main__":
    # Test current credentials
    if not test_login():
        print("\n" + "="*50)
        response = input("Would you like to recreate the admin user? (y/n): ")
        if response.lower() in ['y', 'yes']:
            if recreate_admin():
                print("\n" + "="*50)
                test_login()
    
    print("\n🌐 Try logging in at: http://localhost:5000/login")
    print("📱 Or network access: http://192.168.1.11:5000/login")