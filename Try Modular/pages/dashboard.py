# pages/dashboard.py
from flask import Blueprint, render_template

bp = Blueprint("dashboard_page", __name__)

TEMPLATES = {
"dashboard.html": """{% extends "base.html" %}{% block content %}
<h2>Quick Actions</h2>
<div class="row mb-4">
  <div class="col-md-4">
    <a href="/scan" style="text-decoration:none;color:inherit;">
      <div class="card text-center"><div class="card-body">
        <i class="fa-solid fa-camera fa-2x mb-2"></i>
        <h5 class="card-title">Scan</h5><p class="card-text">Capture and analyze a toenail sample</p>
      </div></div>
    </a>
  </div>
  <div class="col-md-4">
    <a href="/patients" style="text-decoration:none;color:inherit;">
      <div class="card text-center"><div class="card-body">
        <i class="fa-solid fa-user-plus fa-2x mb-2"></i>
        <h5 class="card-title">New Patient</h5><p class="card-text">Add patient to your records</p>
      </div></div>
    </a>
  </div>
  <div class="col-md-4">
    <a href="/reports" style="text-decoration:none;color:inherit;">
      <div class="card text-center"><div class="card-body">
        <i class="fa-solid fa-file-lines fa-2x mb-2"></i>
        <h5 class="card-title">Recent Reports</h5><p class="card-text">View past diagnoses</p>
      </div></div>
    </a>
  </div>
</div>
{% endblock %}"""
}

@bp.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")
