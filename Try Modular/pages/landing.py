# pages/landing.py
import os
from flask import Blueprint, render_template, current_app, url_for

bp = Blueprint("landing", __name__)

TEMPLATES = {
"landing.html": """{% extends "base.html" %}{% block content %}

<!-- Hero Section -->
<div class="row g-4 align-items-center mb-4">
  <div class="col-md-6">
    <div class="p-5 rounded-4 text-white"
         style="background: linear-gradient(135deg, #2563eb 80%, #1e293b 100%); min-height:320px;">
      <div class="mb-4"><i class="fa-solid fa-heart-pulse fa-2x"></i></div>
      <h2 class="fw-bold">MycoSCAN</h2>
      <p class="mb-4">
        Deep Learning-based Severity Level Classification System for Onychomycosis
        with Automated Preemptive Medication Device
      </p>
    </div>
  </div>

  <div class="col-md-6">
    <div class="row g-3">
      <div class="col-6">
        <div class="card h-100 text-center p-3">
          <div class="mb-2"><i class="fa-solid fa-brain fa-2x text-primary"></i></div>
          <h5>Deep Learning</h5>
          <small>Advanced AI-based severity classification</small>
        </div>
      </div>
      <div class="col-6">
        <div class="card h-100 text-center p-3">
          <div class="mb-2"><i class="fa-solid fa-bolt fa-2x text-success"></i></div>
          <h5>Quick Scan</h5>
          <small>Instant nail analysis with photo capture</small>
        </div>
      </div>
      <div class="col-6">
        <div class="card h-100 text-center p-3">
          <div class="mb-2"><i class="fa-solid fa-robot fa-2x text-purple"></i></div>
          <h5>Automated Device</h5>
          <small>Smart medication dispensing system</small>
        </div>
      </div>
      <div class="col-6">
        <div class="card h-100 text-center p-3">
          <div class="mb-2"><i class="fa-solid fa-shield-heart fa-2x text-warning"></i></div>
          <h5>Preemptive Care</h5>
          <small>Early detection and treatment guidance</small>
        </div>
      </div>
    </div>
  </div>
</div>

<!-- About Section -->
<div class="row g-4 mb-4">
  <div class="col-md-8">
    <div class="card p-4 bg-primary text-white">
      <h5>About Onychomycosis</h5>
      <p>
        Onychomycosis is a fungal infection affecting nails, causing discoloration, thickening, and brittleness.
        Early detection is crucial for effective treatment.
      </p>

      <!-- Images (auto-picks correct static path) -->
      <div class="d-flex flex-wrap gap-3 justify-content-start mt-3">
        <div class="bg-white rounded shadow-sm p-2">
          <img src="{{ landing1_url }}" alt="Toenail sample 1"
               class="rounded" style="width:140px; height:140px; object-fit:cover;">
        </div>
        <div class="bg-white rounded shadow-sm p-2">
          <img src="{{ landing2_url }}" alt="Toenail sample 2"
               class="rounded" style="width:140px; height:140px; object-fit:cover;">
        </div>
      </div>
    </div>
  </div>

  <div class="col-md-4 d-flex align-items-center">
    <a href="/dashboard" class="btn btn-lg btn-primary w-100">
      <i class="fa-solid fa-arrow-right"></i> Get Started with MycoSCAN
    </a>
  </div>
</div>

<!-- Footer -->
<div class="text-center mt-5">
  <div class="d-flex justify-content-center gap-4 mb-2">
    <a href="https://www.facebook.com/YourPage" target="_blank" class="text-decoration-none text-primary">
      <i class="fa-brands fa-facebook fa-2x"></i>
    </a>
    <a href="https://www.instagram.com/YourPage" target="_blank" class="text-decoration-none text-danger">
      <i class="fa-brands fa-instagram fa-2x"></i>
    </a>
  </div>
  <h4 class="fw-bold text-muted footer-text mb-2">MycoScan ©2025</h4>
  <div class="text-center text-muted" style="margin-top: -5px;">
    Advanced deep learning-based severity classification
  </div>
</div>

<style>
  .footer-text { font-size: 22px; font-weight: 600; }
  body { overflow-y: auto !important; } /* just in case some global css blocked scrolling */
</style>
{% endblock %}"""
}

def _first_existing(rel_candidates):
    """
    Return a url_for('static', filename=relpath) for the first candidate that exists
    under app.static_folder. rel_candidates are like 'images/landing1.jpg'.
    """
    for rel in rel_candidates:
        full = os.path.join(current_app.static_folder, *rel.split("/"))
        if os.path.isfile(full):
            return url_for("static", filename=rel)
    # fallback to the first path so the HTML compiles even if file is missing
    return url_for("static", filename=rel_candidates[0])

@bp.route("/")
def landing():
    # Try images/ first; if not present, use uploads/scans/ (your current location)
    img1 = _first_existing(["images/landing1.jpg", "uploads/scans/landing1.jpg"])
    img2 = _first_existing(["images/landing2.png", "uploads/scans/landing2.png"])
    return render_template("landing.html", landing1_url=img1, landing2_url=img2)
