# pages/aboutus.py
import os
from flask import Blueprint, render_template, url_for, current_app

bp = Blueprint("aboutus_page", __name__)

TEMPLATES = {
"aboutus.html": """{% extends "base.html" %}{% block content %}
<h2 class="mb-4 text-center">About Us</h2>
<div class="d-flex flex-wrap justify-content-center gap-4">
    {% for m in members %}
    <div class="profile-card text-center flex-grow-1" style="min-width:220px;max-width:260px;">
        <div class="mx-auto mb-3" style="width:120px;height:120px;">
            <img src="{{ photos[loop.index0 % photos|length] }}" alt="{{ m.name }}"
                 class="profile-img"
                 style="width:100%;height:100%;object-fit:cover;border-radius:50%;
                        box-shadow:0 4px 16px rgba(0,0,0,0.12);border:4px solid #fff;">
        </div>
        <h5 class="mb-1">{{ m.name }}</h5>
        <div class="text-muted mb-2">{{ m.role }}</div>
        <div class="small text-secondary">Team 31</div>
    </div>
    {% endfor %}
</div>
<style>
.profile-card {
    background:#fff;border-radius:24px;box-shadow:0 2px 12px rgba(0,0,0,0.07);
    padding:32px 16px 24px;margin-bottom:16px;display:flex;flex-direction:column;
    align-items:center;transition:box-shadow .2s;
}
.profile-card:hover { box-shadow:0 6px 24px rgba(0,0,0,0.13); }
.profile-img { display:block;margin:0 auto; }
@media (max-width:600px){ .profile-card{ min-width:100%; max-width:100%; } }
</style>
{% endblock %}"""
}

def _collect_photos():
    """Return URLs for images found in preferred static folders."""
    allowed = {".jpg", ".jpeg", ".png", ".webp", ".avif"}
    # Search these (first match with files wins)
    search_dirs = [
        os.path.join(current_app.static_folder, "images", "team"),   # recommended
        os.path.join(current_app.static_folder, "uploads", "scans"), # your current folder
    ]

    for folder in search_dirs:
        if os.path.isdir(folder):
            files = [f for f in os.listdir(folder)
                     if os.path.splitext(f)[1].lower() in allowed]
            files.sort()
            if files:
                # Build url_for paths that match where we found them
                if folder.endswith(os.path.join("images", "team")):
                    return [url_for("static", filename=f"images/team/{f}") for f in files]
                else:
                    return [url_for("static", filename=f"uploads/scans/{f}") for f in files]

    # Final fallback – show nothing (or you can add a placeholder here)
    return []

@bp.route("/aboutus")
def aboutus():
    members = [
        {"name": "Regine Apit",  "role": "Cyber-Physical Systems"},
        {"name": "Liam Calamba", "role": "Data Science"},
        {"name": "Ed Fernandez", "role": "Frontend Developer"},
        {"name": "Jc Paloca",    "role": "System Administration"},
        {"name": "Cherwin Yu",   "role": "System Administration"},
    ]
    photos = _collect_photos()
    # If still empty, you can optionally hardcode a placeholder list here.
    return render_template("aboutus.html", members=members, photos=photos)
