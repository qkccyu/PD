#!/usr/bin/env python3
"""
Run MycoScan Flask App
This script ensures the Flask app runs from the correct directory with the right database.
"""

import os
import sys

def run_flask_app():
    # Get the script's directory (Try Modular folder)
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Change to the Try Modular directory
    os.chdir(script_dir)
    
    print(f"🏠 Working directory: {os.getcwd()}")
    print(f"📁 Database will be at: {os.path.join(os.getcwd(), 'mycoscan.db')}")
    
    # Import and run the Flask app
    from main import create_app
    from models import User
    from extensions import db
    
    app = create_app()
    
    # Ensure admin user exists in this database
    with app.app_context():
        print(f"🗄️  Database URI: {app.config['SQLALCHEMY_DATABASE_URI']}")
        
        # Check if admin user exists
        admin = User.query.filter_by(username='admin').first()
        if not admin:
            print("👤 Creating admin user...")
            admin = User(username='admin', email='admin@mycoscan.com')
            admin.set_password('admin123')
            db.session.add(admin)
            db.session.commit()
            print("✅ Admin user created!")
        else:
            print(f"👤 Admin user exists: {admin.username}")
    
    # Start the Flask app
    from network_config import DevelopmentConfig
    config_obj = DevelopmentConfig()
    
    print(f"🚀 Starting MycoScan Server...")
    print(f"📡 Local access: http://localhost:{config_obj.PORT}")
    print(f"🌐 Network access: http://0.0.0.0:{config_obj.PORT}")
    print(f"🔐 Login credentials: admin / admin123")
    print(f"⚠️  Debug mode: {config_obj.DEBUG}")
    
    app.run(host=config_obj.HOST, port=config_obj.PORT, debug=config_obj.DEBUG)

if __name__ == "__main__":
    run_flask_app()