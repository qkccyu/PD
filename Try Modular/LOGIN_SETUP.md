# Login System Setup

This document explains how to use the new login and logout functionality added to the Try Modular application.

## Features Added

1. **User Authentication**: Complete login/logout system with secure password hashing
2. **User Registration**: New users can register with username, email, and password
3. **Password Visibility Toggle**: Users can show/hide passwords during login and registration
4. **Session Management**: User sessions are maintained across page visits
5. **Route Protection**: Dashboard and other protected routes require authentication
6. **Consistent Design**: Login pages match the existing MycoScan dashboard design

## Files Modified/Added

### New Files:
- `pages/login.py` - Login/logout/registration logic and templates
- `create_admin.py` - Script to create initial admin user

### Modified Files:
- `models.py` - Added User model with password hashing
- `main.py` - Added login blueprint and authentication middleware
- `pages/base_tpl.py` - Added login/logout buttons and flash messages
- `requirements.txt` - Added Werkzeug dependency

## Setup Instructions

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Initialize Database** (if not already done):
   ```bash
   python main.py
   ```
   This will create the database tables including the new User table.

3. **Create Admin User**:
   ```bash
   python create_admin.py
   ```
   This creates an initial admin user:
   - Username: `admin`
   - Password: `admin123`
   - Email: `admin@mycoscan.com`

4. **Run the Application**:
   ```bash
   python main.py
   ```

## Usage

1. **Accessing the Application**: 
   - Visit any protected route (like `/dashboard`) and you'll be redirected to login
   - Or visit `/login` directly

2. **Login**:
   - Use the admin credentials or register a new account
   - Password field has a toggle button to show/hide the password
   - Successful login redirects to the dashboard

3. **Registration**:
   - Click "Register here" on the login page
   - Fill out username, email, password, and confirm password
   - Password fields have toggle buttons for visibility
   - Successful registration redirects to login page

4. **Logout**:
   - Click the "Logout" button in the top navigation
   - This clears the session and redirects to login

## Security Features

- Passwords are hashed using Werkzeug's secure password hashing
- Protected routes require authentication
- Session-based authentication
- Password confirmation during registration
- Input validation and error handling

## Customization

- Modify the `TEMPLATES` dictionary in `pages/login.py` to customize the UI
- Update the authentication middleware in `main.py` to change which routes require login
- Add more user fields to the User model in `models.py` if needed

## Troubleshooting

- If you get import errors, make sure all dependencies are installed
- If the database is locked, stop the application and restart it
- Check the console for any error messages during login/registration