# pages/scan.py
from flask import Blueprint, render_template
from models import Patient

bp = Blueprint("scan_page", __name__)

TEMPLATES = {
"scan.html": """{% extends "base.html" %}{% block content %}
<div class="mb-4">
  <a href="/dashboard" class="text-dark text-decoration-none">
    <i class="fa-solid fa-arrow-left"></i> Back
  </a>
  <h2 class="d-inline ms-3">New Toenail Scan</h2>
</div>

<div class="row g-4">
  <div class="col-md-7">
    <div class="card p-4 shadow-sm">
      <div class="d-flex justify-content-center gap-3 mb-3">
        <button id="cameraBtn" class="btn btn-primary">
          <i class="fa-solid fa-camera"></i> Use Camera
        </button>
        <button id="uploadBtn" class="btn btn-secondary">
          <i class="fa-solid fa-upload"></i> Upload Image
        </button>
        <input type="file" id="imageInput" accept="image/*" class="d-none">
      </div>

      <div id="imageContainer" class="border rounded d-flex align-items-center justify-content-center bg-dark bg-opacity-75" style="height:320px;">
        <img id="imagePreview" class="img-fluid d-none rounded shadow-sm" style="max-height:300px; object-fit:contain;" alt="Preview">
        <div id="placeholderText" class="text-light text-center">
          <i class="fa-solid fa-image fa-2x mb-2 d-block"></i>
          <span>No image uploaded yet</span>
        </div>
      </div>

      <div id="loadingSection" class="text-center my-4 d-none">
        <div class="spinner-border text-primary" role="status" style="width:3rem;height:3rem;"><span class="visually-hidden">Analyzing...</span></div>
        <p class="mt-3 mb-1 fw-semibold">Analyzing Image...</p>
        <div class="progress mx-auto" style="height:10px;width:80%;">
          <div id="progressBar" class="progress-bar progress-bar-striped progress-bar-animated" style="width:0%"></div>
        </div>
      </div>

      <!-- RESULTS: choose condition/severity BEFORE saving -->
      <div class="card mt-3 border-0">
        <div class="card-body">
          <h5 class="mb-3">Results</h5>
          <div class="row g-3">
            <div class="col-md-6">
              <label class="form-label">Condition</label>
              <select id="resultCondition" class="form-select">
                <option value="Onychomycosis" selected>Onychomycosis</option>
                <option value="Healthy">Healthy</option>
              </select>
            </div>
            <div class="col-md-6">
              <label class="form-label">Severity Level</label>
              <select id="resultSeverity" class="form-select">
                <option value="Mild" selected>Mild</option>
                <option value="Moderate">Moderate</option>
                <option value="Severe">Severe</option>
                <option value="N/A">N/A</option>
              </select>
            </div>
          </div>
          <small class="text-muted d-block mt-2">Tip: Selecting <strong>Healthy</strong> will set severity to <strong>N/A</strong>.</small>
        </div>
      </div>

      <div class="text-center mt-3">
        <button id="saveScanBtn" class="btn btn-success px-5 py-2">
          <i class="fa-solid fa-floppy-disk"></i> Save Scan
        </button>
      </div>
    </div>
  </div>

  <div class="col-md-5">
    <div class="card p-4 shadow-sm">
      <h5>Patient Information</h5>
      <div class="mb-3">
        <label class="form-label">Select Patient</label>
        <select id="patientSelect" class="form-select">
          {% for p in patients %}<option>{{ p }}</option>{% endfor %}
        </select>
      </div>
      <div class="mb-3">
        <label class="form-label">Notes</label>
        <textarea id="scanNotes" class="form-control" rows="3" placeholder="Any observations or notes about this scan..."></textarea>
      </div>
    </div>
  </div>
</div>

<script>
let selectedFile = null;

const cameraBtn = document.getElementById('cameraBtn');
const uploadBtn = document.getElementById('uploadBtn');
const imageInput = document.getElementById('imageInput');
const preview = document.getElementById('imagePreview');
const placeholderText = document.getElementById('placeholderText');
const loadingSection = document.getElementById('loadingSection');
const progressBar = document.getElementById('progressBar');
const saveBtn = document.getElementById('saveScanBtn');
const resultCondition = document.getElementById('resultCondition');
const resultSeverity = document.getElementById('resultSeverity');

// Adjust severity when condition=Healthy
resultCondition.addEventListener('change', () => {
  if (resultCondition.value === "Healthy") {
    resultSeverity.value = "N/A";
    resultSeverity.disabled = true;
  } else {
    if (resultSeverity.value === "N/A") resultSeverity.value = "Mild";
    resultSeverity.disabled = false;
  }
});

// Camera placeholder
cameraBtn.addEventListener('click', () => showToast("📷 Camera capture will be connected to Raspberry Pi soon!"));

// Upload
uploadBtn.addEventListener('click', () => imageInput.click());
imageInput.addEventListener('change', () => {
  const file = imageInput.files[0];
  if (!file) return;
  selectedFile = file;
  simulateProgress(() => {
    const reader = new FileReader();
    reader.onload = e => {
      preview.src = e.target.result;
      preview.classList.remove('d-none');
      placeholderText.classList.add('d-none');
    };
    reader.readAsDataURL(file);
  });
});

// Progress animation
function simulateProgress(callback) {
  loadingSection.classList.remove('d-none');
  let progress = 0;
  const interval = setInterval(() => {
    progress += Math.random() * 15;
    if (progress >= 100) {
      progress = 100;
      clearInterval(interval);
      setTimeout(() => {
        loadingSection.classList.add('d-none');
        progressBar.style.width = '0%';
        if (callback) callback();
      }, 500);
    }
    progressBar.style.width = progress + '%';
  }, 300);
}

// Save (POST) then go to /reports
saveBtn.addEventListener('click', async () => {
  const patient = document.getElementById('patientSelect').value;
  const notes = document.getElementById('scanNotes').value.trim();
  const condition = resultCondition.value;
  const severity = resultSeverity.value;

  if (!selectedFile) {
    showToast("Please upload or capture an image first.", "danger", "fa-triangle-exclamation");
    return;
  }

  saveBtn.disabled = true;
  const formData = new FormData();
  formData.append('patient_name', patient);
  formData.append('notes', notes);
  formData.append('condition', condition);
  formData.append('severity', severity);
  formData.append('image', selectedFile, selectedFile.name);

  try {
    const res = await fetch('/api/scans', { method: 'POST', body: formData });
    const data = await res.json();
    if (!res.ok || data.error) throw new Error(data.error || ('HTTP ' + res.status));
    showToast('Scan saved! Redirecting to Recent Reports…');
    setTimeout(() => { window.location.href = '/reports'; }, 900);
  } catch (err) {
    console.error(err);
    showToast('Failed to save scan', 'danger', 'fa-triangle-exclamation');
  } finally {
    saveBtn.disabled = false;
  }
});

// toast
function showToast(message, color="success", icon="fa-check") {
  const toast = document.createElement("div");
  toast.className = `soft-toast alert alert-${color} shadow text-center`;
  toast.innerHTML = `<i class="fa-solid ${icon} me-2"></i>${message}`;
  document.body.appendChild(toast);
  requestAnimationFrame(() => toast.classList.add('show'));
  setTimeout(() => { toast.classList.remove('show'); setTimeout(() => toast.remove(), 250); }, 2000);
}
</script>

<style>
#imageContainer { transition: all 0.3s ease; }
.progress{ background-color:#e9ecef; border-radius:5px; }
.spinner-border{ animation-duration: .8s; }
.soft-toast{ position:fixed; top:18px; left:50%; transform:translate(-50%,-8px); min-width:280px;
  border-radius:14px; padding:.75rem 1rem; z-index:3000; opacity:0; transition:all .2s; box-shadow:0 12px 30px rgba(0,0,0,.12); }
.soft-toast.show{ transform:translate(-50%,0); opacity:1; }
</style>
{% endblock %}"""
}

@bp.route("/scan")
def scan():
    patients = [p.name for p in Patient.query.all()]
    return render_template("scan.html", patients=patients)