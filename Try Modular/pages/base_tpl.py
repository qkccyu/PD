# pages/base_tpl.py

TEMPLATES = {
"base.html": """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <!-- Keep page responsive and ensure scrolling works everywhere -->
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>MycoScan</title>

    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css">
    <link rel="stylesheet" href="{{ url_for('static', filename='css/style.css') }}">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">

    <style>
        /* Hard override any accidental global styles */
        html { min-height: 100%; height: auto; overflow-y: auto !important; }
        body { min-height: 100%; height: auto; overflow-y: auto !important; position: static !important; }

        /* Sticky navbar (like original), with page content offset */
        .navbar {
            position: fixed;
            top: 0; left: 0; right: 0;
            z-index: 1050;
            background-color: #fff !important;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }
        body { padding-top: 70px; }
        .navbar.bg-white {
            backdrop-filter: blur(8px);
            background-color: rgba(255, 255, 255, 0.95) !important;
        }
        .btn-light { border-radius: 50%; }
    </style>
</head>

<body>
    <nav class="navbar navbar-light bg-white shadow-sm">
        <div class="container-fluid">
            <a href="/" class="navbar-brand mb-0 h1" style="text-decoration:none;color:inherit;">
                <i class="fa-solid fa-heart-pulse"></i> MycoScan
            </a>

            <!-- Hide the mid-nav links only on '/' (bar itself remains sticky) -->
            {% if request.path != '/' %}
            <ul class="nav">
                <li class="nav-item">
                    <a class="nav-link {% if request.path.startswith('/dashboard') %}active{% endif %}" href="/dashboard">
                        <i class="fa-solid fa-house"></i> Dashboard
                    </a>
                </li>
                <li class="nav-item">
                    <a class="nav-link {% if request.path.startswith('/patients') %}active{% endif %}" href="/patients">
                        <i class="fa-solid fa-user"></i> Patients
                    </a>
                </li>
                <li class="nav-item">
                    <a class="nav-link {% if request.path.startswith('/medications') %}active{% endif %}" href="/medications">
                        <i class="fa-solid fa-cube"></i> Medications
                    </a>
                </li>
            </ul>
            {% endif %}

            <div class="d-flex align-items-center ms-auto" style="gap:12px;">
                {% if session.get('user_id') %}
                    <span class="text-muted me-2">
                        <i class="fa-solid fa-user"></i> {{ session.get('username') }}
                    </span>
                    <a href="/logout" class="btn btn-outline-danger btn-sm" title="Logout">
                        <i class="fa-solid fa-sign-out-alt"></i> Logout
                    </a>
                {% else %}
                    <a href="/login" class="btn btn-primary btn-sm" title="Login">
                        <i class="fa-solid fa-sign-in-alt"></i> Login
                    </a>
                {% endif %}
                <a href="/aboutus" class="btn btn-light p-2" title="About Us">
                    <i class="fa-solid fa-users"></i>
                </a>
            </div>
        </div>
    </nav>

    <div class="container mt-4">
        {% with messages = get_flashed_messages(with_categories=true) %}
            {% if messages %}
                {% for category, message in messages %}
                    <div class="alert alert-{{ 'success' if category == 'success' else 'info' if category == 'info' else 'danger' }} alert-dismissible fade show" role="alert">
                        {{ message }}
                        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
                    </div>
                {% endfor %}
            {% endif %}
        {% endwith %}
        
        {% block content %}{% endblock %}
    </div>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>"""
}
