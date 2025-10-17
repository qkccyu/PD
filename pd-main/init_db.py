from app import app, db

with app.app_context():
    db.drop_all()
    db.create_all()
    print("Database tables dropped and recreated successfully!")

    # Create a default admin user
    from app import User
    admin = User(username='admin', email='admin@example.com')
    admin.set_password('admin123')
    db.session.add(admin)
    db.session.commit()
    print("Default admin user created!")
    print("Username: admin")
    print("Password: admin123")