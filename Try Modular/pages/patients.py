from flask import Blueprint, render_template
from models import Patient

bp = Blueprint("patients_page", __name__)

TEMPLATES = {
"patients.html": """{% extends "base.html" %}{% block content %}
<h2>Patient Records</h2>
<div class="card mb-4">
  <div class="card-body">
    <div class="d-flex justify-content-between align-items-center mb-3">
      <input type="text" class="form-control w-50" placeholder="Search patients...">
      <div>
        <button class="btn btn-light" id="refreshBtn"><i class="fa-solid fa-rotate"></i> Refresh</button>
      </div>
    </div>

    <table class="table" id="patientsTable">
      <thead>
        <tr>
          <th>PATIENT</th>
          <th>LAST VISIT</th>
          <th>CONDITION</th>
          <th>SEVERITY</th>
          <th>ACTIONS</th>
        </tr>
      </thead>
      <tbody id="patientsBody"></tbody>
    </table>

    <button class="btn btn-primary" id="addPatientBtn">
      <i class="fa-solid fa-plus"></i> Add Patient
    </button>
  </div>
</div>

<!-- Add Patient Modal -->
<div class="modal fade" id="addPatientModal" tabindex="-1" aria-hidden="true">
  <div class="modal-dialog">
    <div class="modal-content">
      <div class="modal-header">
        <h5 class="modal-title">Add New Patient</h5>
        <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
      </div>
      <div class="modal-body">
        <form id="addPatientForm">
          <div class="mb-3">
            <label for="patientName" class="form-label">Name</label>
            <input type="text" class="form-control" id="patientName" required>
          </div>
          <div class="mb-3">
            <label for="patientAge" class="form-label">Age</label>
            <input type="number" class="form-control" id="patientAge" required min="0">
          </div>
          <div class="mb-3">
            <label for="patientSex" class="form-label">Sex</label>
            <select class="form-select" id="patientSex" required>
              <option value="">Select...</option>
              <option value="Male">Male</option>
              <option value="Female">Female</option>
            </select>
          </div>
          <button type="submit" class="btn btn-primary w-100">Add Patient</button>
        </form>
      </div>
    </div>
  </div>
</div>

<!-- Edit Patient Modal -->
<div class="modal fade" id="editPatientModal" tabindex="-1" aria-hidden="true">
  <div class="modal-dialog">
    <div class="modal-content">
      <div class="modal-header">
        <h5 class="modal-title">Edit Patient Info</h5>
        <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
      </div>
      <div class="modal-body">
        <form id="editPatientForm">
          <input type="hidden" id="editPatientId">
          <div class="mb-3">
            <label for="editLastVisit" class="form-label">Last Visit</label>
            <input type="date" class="form-control" id="editLastVisit" required>
          </div>
          <div class="mb-3">
            <label for="editCondition" class="form-label">Condition</label>
            <select class="form-select" id="editCondition" required>
              <option value="Onychomycosis">Onychomycosis</option>
              <option value="Healthy">Healthy</option>
            </select>
          </div>
          <div class="mb-3">
            <label for="editSeverity" class="form-label">Severity</label>
            <select class="form-select" id="editSeverity" required>
              <option value="Mild">Mild</option>
              <option value="Moderate">Moderate</option>
              <option value="Severe">Severe</option>
              <option value="N/A">N/A</option>
            </select>
          </div>
          <button type="submit" class="btn btn-primary w-100">Save Changes</button>
        </form>
      </div>
    </div>
  </div>
</div>

<!-- Delete Confirmation Modal -->
<div class="modal fade" id="deleteConfirmModal" tabindex="-1" aria-hidden="true">
  <div class="modal-dialog modal-sm modal-dialog-centered">
    <div class="modal-content text-center">
      <div class="modal-body">
        <p class="fw-bold">Are you sure you want to delete this patient?</p>
        <div class="d-flex justify-content-center gap-2 mt-3">
          <button class="btn btn-secondary" data-bs-dismiss="modal">Cancel</button>
          <button class="btn btn-danger" id="confirmDeleteBtn">Delete</button>
        </div>
      </div>
    </div>
  </div>
</div>

<script>
let deletePatientId = null;
let allPatients = [];
let hiddenDetails = new Set();

function renderPatientRow(p) {
  const hidden = hiddenDetails.has(p.id);
  return `
  <tr data-id="${p.id}">
    <td>
      <div class="d-flex align-items-center">
        <div class="bg-light rounded-circle p-2 me-2"><i class="fa-solid fa-user"></i></div>
        <div>
          <strong>${p.name}</strong><br>
          <small class="patient-details" style="display:${hidden ? 'none' : 'inline'}">${p.age}yo, ${p.sex}</small>
        </div>
      </div>
    </td>
    <td>${p.last_visit || 'Not set'}</td>
    <td>${p.condition || 'Not set'}</td>
    <td>
      ${p.severity ? `<span class='badge ${
        p.severity == "Moderate" ? "bg-warning text-dark" :
        p.severity == "Mild" ? "bg-success bg-opacity-25 text-success" :
        p.severity == "Severe" ? "bg-danger bg-opacity-25 text-danger" : "bg-secondary"
      }'>${p.severity}</span>` : ''}
    </td>
    <td>
      <a href="#" class="toggle-info me-2"><i class="fa-regular fa-eye"></i></a>
      <a href="#" class="edit-patient me-2"><i class="fa-regular fa-pen-to-square"></i></a>
      <a href="#" class="delete-patient text-danger"><i class="fa-solid fa-trash"></i></a>
    </td>
  </tr>`;
}

function loadPatients() {
  fetch('/api/patients')
    .then(r => r.json())
    .then(data => { allPatients = data; displayPatients(data); });
}

function displayPatients(patients) {
  const body = document.getElementById('patientsBody');
  body.innerHTML = '';
  patients.forEach(p => body.innerHTML += renderPatientRow(p));
}

document.querySelector('input[placeholder="Search patients..."]').addEventListener('input', e => {
  const term = e.target.value.toLowerCase();
  const filtered = allPatients.filter(p =>
    p.name.toLowerCase().includes(term) ||
    p.condition.toLowerCase().includes(term) ||
    p.severity.toLowerCase().includes(term)
  );
  displayPatients(filtered);
});

document.getElementById('addPatientBtn').onclick = () => {
  new bootstrap.Modal(document.getElementById('addPatientModal')).show();
};

document.getElementById('addPatientForm').onsubmit = e => {
  e.preventDefault();
  const name = patientName.value.trim();
  const age = parseInt(patientAge.value);
  const sex = patientSex.value;

  fetch('/api/patients', {
    method: 'POST',
    headers: {'Content-Type':'application/json'},
    body: JSON.stringify({name, age, sex})
  })
  .then(r => r.json())
  .then(newPatient => {
    if (newPatient && newPatient.id) {
      allPatients.push(newPatient);
      displayPatients(allPatients);
      bootstrap.Modal.getInstance(document.getElementById('addPatientModal')).hide();
      e.target.reset();
      showAlert('✅ New Patient Added!');
    }
  });
};

document.addEventListener('click', e => {
  const icon = e.target.closest('.toggle-info');
  if (icon) {
    const row = icon.closest('tr');
    const id = parseInt(row.dataset.id);
    const details = row.querySelector('.patient-details');
    const currentlyHidden = details.style.display === 'none';
    details.style.display = currentlyHidden ? 'inline' : 'none';
    if (currentlyHidden) hiddenDetails.delete(id); else hiddenDetails.add(id);
  }
});

document.addEventListener('click', e => {
  if (e.target.closest('.edit-patient')) {
    const row = e.target.closest('tr');
    const id = row.dataset.id;
    document.getElementById('editPatientId').value = id;
    new bootstrap.Modal(document.getElementById('editPatientModal')).show();
  }
});

document.getElementById('editCondition').addEventListener('change', () => {
  const disabled = document.getElementById('editCondition').value === "Healthy";
  const sel = document.getElementById('editSeverity');
  sel.disabled = disabled;
  if (disabled) sel.value = "N/A";
});

document.getElementById('editPatientForm').onsubmit = e => {
  e.preventDefault();
  const id = document.getElementById('editPatientId').value;
  const last_visit = document.getElementById('editLastVisit').value;
  const condition = document.getElementById('editCondition').value;
  const severity = condition === "Healthy" ? "N/A" : document.getElementById('editSeverity').value;

  fetch(`/api/patients/${id}`, {
    method: 'PUT',
    headers: {'Content-Type':'application/json'},
    body: JSON.stringify({ last_visit, condition, severity })
  })
  .then(r => r.json())
  .then(updated => {
    allPatients = allPatients.map(p => p.id === updated.id ? updated : p);
    displayPatients(allPatients);
    bootstrap.Modal.getInstance(document.getElementById('editPatientModal')).hide();
    showAlert('✅ Patient Updated Successfully!');
  });
};

document.addEventListener('click', e => {
  if (e.target.closest('.delete-patient')) {
    const id = e.target.closest('tr').dataset.id;
    window.deletePatientId = id;
    new bootstrap.Modal(document.getElementById('deleteConfirmModal')).show();
  }
});

document.getElementById('confirmDeleteBtn').onclick = () => {
  fetch(`/api/patients/${window.deletePatientId}`, { method: 'DELETE' })
    .then(() => {
      allPatients = allPatients.filter(p => p.id != window.deletePatientId);
      displayPatients(allPatients);
      bootstrap.Modal.getInstance(document.getElementById('deleteConfirmModal')).hide();
      showAlert('🗑️ Patient deleted successfully!');
    });
};

document.getElementById('refreshBtn').onclick = () => {
  loadPatients();
  showAlert('🔄 Records refreshed!');
};

function showAlert(message) {
  const alertDiv = document.createElement('div');
  alertDiv.className = 'alert alert-success position-fixed top-50 start-50 translate-middle text-center shadow-lg fade show';
  alertDiv.style.zIndex = '2000';
  alertDiv.style.minWidth = '300px';
  alertDiv.innerHTML = `<strong>${message}</strong>`;
  document.body.appendChild(alertDiv);
  setTimeout(() => alertDiv.remove(), 2500);
}

window.addEventListener('DOMContentLoaded', loadPatients);
</script>
{% endblock %}"""
}

@bp.route("/patients")
def patients():
    # (not used by the JS list, but kept for parity)
    _ = Patient.query.all()
    return render_template("patients.html")
