# pages/login.py
from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from models import User
from extensions import db

bp = Blueprint("login_page", __name__)

TEMPLATES = {
"login.html": """{% extends "base.html" %}
{% block content %}
<div class="row justify-content-center">
    <div class="col-md-6 col-lg-4">
        <div class="card shadow-sm">
            <div class="card-body">
                <div class="text-center mb-4">
                    <i class="fa-solid fa-heart-pulse fa-3x text-primary mb-3"></i>
                    <h3 class="card-title">MycoScan Login</h3>
                    <p class="text-muted">Access your medical dashboard</p>
                </div>
                
                {% with messages = get_flashed_messages() %}
                    {% if messages %}
                        {% for message in messages %}
                            <div class="alert alert-danger alert-dismissible fade show" role="alert">
                                {{ message }}
                                <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
                            </div>
                        {% endfor %}
                    {% endif %}
                {% endwith %}
                
                <form method="POST" onsubmit="debugForm(event)">
                    <div class="mb-3">
                        <label for="username" class="form-label">
                            <i class="fa-solid fa-user"></i> Username
                        </label>
                        <input type="text" class="form-control" id="username" name="username" required autocomplete="username">
                    </div>
                    
                    <div class="mb-3">
                        <label for="password" class="form-label">
                            <i class="fa-solid fa-lock"></i> Password
                        </label>
                        <div class="input-group">
                            <input type="password" class="form-control" id="password" name="password" required autocomplete="current-password">
                            <button class="btn btn-outline-secondary" type="button" id="togglePassword">
                                <i class="fa-solid fa-eye" id="toggleIcon"></i>
                            </button>
                        </div>
                    </div>
                    
                    <div class="d-grid">
                        <button type="submit" class="btn btn-primary">
                            <i class="fa-solid fa-sign-in-alt"></i> Login
                        </button>
                    </div>
                </form>
                
                <div class="text-center mt-3">
                    <small class="text-muted">
                        Don't have an account? 
                        <a href="/register" class="text-decoration-none">Register here</a>
                    </small>
                </div>
            </div>
        </div>
    </div>
</div>

<script>
document.addEventListener('DOMContentLoaded', function() {
    const togglePassword = document.getElementById('togglePassword');
    const passwordField = document.getElementById('password');
    const toggleIcon = document.getElementById('toggleIcon');
    
    togglePassword.addEventListener('click', function() {
        const type = passwordField.getAttribute('type') === 'password' ? 'text' : 'password';
        passwordField.setAttribute('type', type);
        
        // Toggle the eye icon
        if (type === 'password') {
            toggleIcon.classList.remove('fa-eye-slash');
            toggleIcon.classList.add('fa-eye');
        } else {
            toggleIcon.classList.remove('fa-eye');
            toggleIcon.classList.add('fa-eye-slash');
        }
    });
});

// Debug function to help troubleshoot login issues
function debugForm(event) {
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;
    
    console.log('Login attempt:');
    console.log('Username:', username);
    console.log('Password length:', password.length);
    console.log('Password (first 3 chars):', password.substring(0, 3));
    
    // Check for common issues
    if (username.trim() !== username) {
        console.warn('Username has leading/trailing spaces!');
    }
    if (password.trim() !== password) {
        console.warn('Password has leading/trailing spaces!');
    }
    
    // Allow form to submit normally
    return true;
}
</script>
{% endblock %}""",

"register.html": """{% extends "base.html" %}
{% block content %}
<div class="row justify-content-center">
    <div class="col-md-6 col-lg-4">
        <div class="card shadow-sm">
            <div class="card-body">
                <div class="text-center mb-4">
                    <i class="fa-solid fa-user-plus fa-3x text-primary mb-3"></i>
                    <h3 class="card-title">Create Account</h3>
                    <p class="text-muted">Join MycoScan today</p>
                </div>
                
                {% with messages = get_flashed_messages() %}
                    {% if messages %}
                        {% for message in messages %}
                            <div class="alert alert-danger alert-dismissible fade show" role="alert">
                                {{ message }}
                                <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
                            </div>
                        {% endfor %}
                    {% endif %}
                {% endwith %}
                
                <form method="POST">
                    <div class="mb-3">
                        <label for="username" class="form-label">
                            <i class="fa-solid fa-user"></i> Username
                        </label>
                        <input type="text" class="form-control" id="username" name="username" required>
                    </div>
                    
                    <div class="mb-3">
                        <label for="email" class="form-label">
                            <i class="fa-solid fa-envelope"></i> Email
                        </label>
                        <input type="email" class="form-control" id="email" name="email" required>
                    </div>
                    
                    <div class="mb-3">
                        <label for="password" class="form-label">
                            <i class="fa-solid fa-lock"></i> Password
                        </label>
                        <div class="input-group">
                            <input type="password" class="form-control" id="password" name="password" required>
                            <button class="btn btn-outline-secondary" type="button" id="togglePassword">
                                <i class="fa-solid fa-eye" id="toggleIcon"></i>
                            </button>
                        </div>
                    </div>
                    
                    <div class="mb-3">
                        <label for="confirm_password" class="form-label">
                            <i class="fa-solid fa-lock"></i> Confirm Password
                        </label>
                        <div class="input-group">
                            <input type="password" class="form-control" id="confirm_password" name="confirm_password" required>
                            <button class="btn btn-outline-secondary" type="button" id="toggleConfirmPassword">
                                <i class="fa-solid fa-eye" id="toggleConfirmIcon"></i>
                            </button>
                        </div>
                    </div>
                    
                    <div class="d-grid">
                        <button type="submit" class="btn btn-primary">
                            <i class="fa-solid fa-user-plus"></i> Register
                        </button>
                    </div>
                </form>
                
                <div class="text-center mt-3">
                    <small class="text-muted">
                        Already have an account? 
                        <a href="/login" class="text-decoration-none">Login here</a>
                    </small>
                </div>
            </div>
        </div>
    </div>
</div>

<script>
document.addEventListener('DOMContentLoaded', function() {
    const togglePassword = document.getElementById('togglePassword');
    const passwordField = document.getElementById('password');
    const toggleIcon = document.getElementById('toggleIcon');
    
    const toggleConfirmPassword = document.getElementById('toggleConfirmPassword');
    const confirmPasswordField = document.getElementById('confirm_password');
    const toggleConfirmIcon = document.getElementById('toggleConfirmIcon');
    
    togglePassword.addEventListener('click', function() {
        const type = passwordField.getAttribute('type') === 'password' ? 'text' : 'password';
        passwordField.setAttribute('type', type);
        
        if (type === 'password') {
            toggleIcon.classList.remove('fa-eye-slash');
            toggleIcon.classList.add('fa-eye');
        } else {
            toggleIcon.classList.remove('fa-eye');
            toggleIcon.classList.add('fa-eye-slash');
        }
    });
    
    toggleConfirmPassword.addEventListener('click', function() {
        const type = confirmPasswordField.getAttribute('type') === 'password' ? 'text' : 'password';
        confirmPasswordField.setAttribute('type', type);
        
        if (type === 'password') {
            toggleConfirmIcon.classList.remove('fa-eye-slash');
            toggleConfirmIcon.classList.add('fa-eye');
        } else {
            toggleConfirmIcon.classList.remove('fa-eye');
            toggleConfirmIcon.classList.add('fa-eye-slash');
        }
    });
});
</script>
{% endblock %}"""
}

@bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()
        
        # Debug information
        print(f"DEBUG: Login attempt - Username: '{username}', Password length: {len(password) if password else 0}")
        
        if not username or not password:
            flash("Please fill in all fields.")
            return render_template("login.html")
        
        user = User.query.filter_by(username=username).first()
        print(f"DEBUG: User found: {user is not None}")
        
        if user:
            print(f"DEBUG: User active: {user.is_active}")
            password_valid = user.check_password(password)
            print(f"DEBUG: Password valid: {password_valid}")
        
        if user and user.check_password(password) and user.is_active:
            session["user_id"] = user.id
            session["username"] = user.username
            flash("Login successful!", "success")
            return redirect(url_for("dashboard_page.dashboard"))
        else:
            flash("Invalid username or password.")
            
    return render_template("login.html")

@bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")
        
        if not all([username, email, password, confirm_password]):
            flash("Please fill in all fields.")
            return render_template("register.html")
        
        if password != confirm_password:
            flash("Passwords do not match.")
            return render_template("register.html")
        
        if len(password) < 6:
            flash("Password must be at least 6 characters long.")
            return render_template("register.html")
        
        # Check if user already exists
        existing_user = User.query.filter(
            (User.username == username) | (User.email == email)
        ).first()
        
        if existing_user:
            flash("Username or email already exists.")
            return render_template("register.html")
        
        # Create new user
        new_user = User(username=username, email=email)
        new_user.set_password(password)
        
        try:
            db.session.add(new_user)
            db.session.commit()
            flash("Registration successful! Please login.", "success")
            return redirect(url_for("login_page.login"))
        except Exception as e:
            db.session.rollback()
            flash("An error occurred during registration. Please try again.")
            
    return render_template("register.html")

@bp.route("/logout")
def logout():
    session.clear()
    flash("You have been logged out.", "info")
    return redirect(url_for("login_page.login"))