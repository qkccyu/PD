#!/usr/bin/env python3
"""
Create an initial admin user for testing the login system.
Run this script after setting up the database.
"""

from main import create_app
from models import User
from extensions import db

def create_admin_user():
    app = create_app()
    with app.app_context():
        # Check if admin user already exists
        admin = User.query.filter_by(username='admin').first()
        if admin:
            print("Admin user already exists!")
            return
        
        # Create admin user
        admin = User(
            username='admin',
            email='admin@mycoscan.com'
        )
        admin.set_password('admin123')  # Change this in production!
        
        try:
            db.session.add(admin)
            db.session.commit()
            print("Admin user created successfully!")
            print("Username: admin")
            print("Password: admin123")
            print("Please change the password after first login!")
        except Exception as e:
            db.session.rollback()
            print(f"Error creating admin user: {e}")

if __name__ == "__main__":
    create_admin_user()