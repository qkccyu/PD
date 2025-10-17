from app import app, db, User

with app.app_context():
    # Check if admin user exists
    admin = User.query.filter_by(username='admin').first()
    if admin:
        print("Admin user exists:")
        print(f"Username: {admin.username}")
        print(f"Email: {admin.email}")
        print("Testing password 'admin123':", admin.check_password('admin123'))
    else:
        print("No admin user found in database!")