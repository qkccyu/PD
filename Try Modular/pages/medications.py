# pages/medications.py
from flask import Blueprint, render_template

bp = Blueprint("medications_page", __name__)

TEMPLATES = {
"medications.html": """{% extends "base.html" %}{% block content %}
<h2>Clinic Inventory</h2>

<!-- Refresh Button -->
<div class="d-flex justify-content-end mb-3">
  <button class="btn btn-light" id="refreshBtn">
    <i class="fa-solid fa-rotate"></i> Refresh
  </button>
</div>

<!-- Container for medications -->
<div class="row g-4" id="medicationsContainer"></div>

<!-- Add Medication Modal -->
<div class="modal fade" id="addMedicationModal" tabindex="-1" aria-hidden="true">
  <div class="modal-dialog">
    <div class="modal-content">
      <div class="modal-header">
        <h5 class="modal-title">Add New Medication</h5>
        <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
      </div>
      <div class="modal-body">
        <form id="addMedicationForm">
          <div class="mb-3">
            <label class="form-label">Medicine Name</label>
            <input type="text" class="form-control" id="medName" required>
          </div>
          <div class="mb-3">
            <label class="form-label">Type</label>
            <input type="text" class="form-control" id="medType" required>
          </div>
          <div class="mb-3">
            <label class="form-label">Stock Quantity</label>
            <input type="number" class="form-control" id="medStock" required min="0" value="0">
          </div>
          <button type="submit" class="btn btn-primary w-100">Add Medication</button>
        </form>
      </div>
    </div>
  </div>
</div>

<script>
// ---------- Toast helper ----------
function showToast(message, color="success", icon="fa-check") {
  const toast = document.createElement("div");
  toast.className = `soft-toast alert alert-${color} shadow text-center`;
  toast.innerHTML = `<i class="fa-solid ${icon} me-2"></i>${message}`;
  document.body.appendChild(toast);
  requestAnimationFrame(() => toast.classList.add('show'));
  setTimeout(() => {
    toast.classList.remove('show');
    setTimeout(() => toast.remove(), 250);
  }, 2200);
}

// ---------- Floating confirm (replaces window.confirm) ----------
function showConfirm({ title="Confirm", message="", confirmText="Delete", cancelText="Cancel", onConfirm }) {
  // Remove existing one if any
  document.querySelectorAll('.confirm-toast').forEach(e => e.remove());

  const wrap = document.createElement('div');
  wrap.className = 'confirm-toast shadow-lg';
  wrap.innerHTML = `
    <div class="d-flex align-items-start gap-3">
      <div class="icon-wrap">
        <i class="fa-solid fa-triangle-exclamation"></i>
      </div>
      <div class="flex-grow-1">
        <div class="fw-semibold mb-1">${title}</div>
        <div class="small text-muted">${message}</div>
        <div class="d-flex gap-2 mt-3">
          <button class="btn btn-sm btn-secondary" data-role="cancel">${cancelText}</button>
          <button class="btn btn-sm btn-danger" data-role="confirm"><i class="fa-solid fa-trash me-1"></i>${confirmText}</button>
        </div>
      </div>
      <button class="btn-close" data-role="close" aria-label="Close"></button>
    </div>
  `;
  document.body.appendChild(wrap);
  requestAnimationFrame(() => wrap.classList.add('show'));

  const close = () => { wrap.classList.remove('show'); setTimeout(()=>wrap.remove(), 200); };
  wrap.querySelector('[data-role="cancel"]').onclick = close;
  wrap.querySelector('[data-role="close"]').onclick = close;
  wrap.querySelector('[data-role="confirm"]').onclick = async () => {
    try { await onConfirm?.(); }
    finally { close(); }
  };
}

// ---------- UI builders ----------
function buildAddCard() {
  const addCard = document.createElement('div');
  addCard.className = 'col-md-6';
  addCard.innerHTML = `
    <div class="card h-100 d-flex align-items-center justify-content-center p-4 border-0 shadow-sm">
      <div class="text-center">
        <div class="bg-light rounded-circle p-3 mb-2 mx-auto" style="width:48px;height:48px;">
          <i class="fa-solid fa-plus fa-2x"></i>
        </div>
        <button class="btn btn-link text-decoration-none" id="openAddBtn">Add New Medication</button>
      </div>
    </div>`;
  return addCard;
}

function buildMedCard(med) {
  const imageSrc = med.image_url || '';
  const imageArea = imageSrc
    ? `<div class="image-box"><img src="${imageSrc}" class="rounded border med-image" alt="${med.name}"></div>`
    : `<div class="image-box upload-hover d-flex flex-column align-items-center justify-content-center border rounded"
         onclick="triggerImageUpload(this)">
         <i class="fa-solid fa-plus fa-2x text-muted"></i>
         <small class="text-muted">Add Image</small>
         <input type="file" class="d-none" accept="image/*" onchange="uploadImage(${med.id}, this)">
       </div>`;

  const card = document.createElement('div');
  card.className = 'col-md-6';
  card.innerHTML = `
    <div class="card shadow-sm border-0 p-3 d-flex flex-row align-items-center justify-content-between">
      <div class="flex-grow-1 me-3">
        <h5 class="card-title mb-1">${med.name}</h5>
        <p class="text-muted mb-1">${med.type}</p>
        <p><strong>In Stock:</strong> ${med.stock}</p>
        <button class="btn btn-outline-danger btn-sm" onclick="deleteMedication(${med.id}, '${med.name.replace(/'/g,"\\'")}')">
          <i class="fa-solid fa-trash"></i> Delete
        </button>
      </div>
      ${imageArea}
    </div>`;
  return card;
}

// ---------- Data load ----------
async function loadMedications() {
  const container = document.getElementById('medicationsContainer');
  container.innerHTML = '';

  let meds = [];
  try {
    const res = await fetch('/api/medications', { headers: { 'Accept': 'application/json' }});
    if (!res.ok) throw new Error('HTTP ' + res.status);
    meds = await res.json();
  } catch (err) {
    console.error('Failed to load medications:', err);
    showToast('Could not load inventory. You can still add new items.', 'warning', 'fa-triangle-exclamation');
  }

  if (Array.isArray(meds) && meds.length) {
    meds.forEach(med => container.appendChild(buildMedCard(med)));
  } else {
    const empty = document.createElement('div');
    empty.className = 'col-12';
    empty.innerHTML = `
      <div class="text-muted text-center py-4">
        <i class="fa-regular fa-box-open fa-2x d-block mb-2"></i>
        <div>No medications yet.</div>
      </div>`;
    container.appendChild(empty);
  }

  const addCard = buildAddCard();
  container.appendChild(addCard);
  addCard.querySelector('#openAddBtn').addEventListener('click', openAddModal);
}

// ---------- Modal / CRUD ----------
function openAddModal() {
  new bootstrap.Modal(document.getElementById('addMedicationModal')).show();
}

document.addEventListener('DOMContentLoaded', () => {
  loadMedications();

  document.getElementById('refreshBtn').addEventListener('click', () => {
    loadMedications();
    showToast("Inventory Refreshed","secondary","fa-rotate");
  });

  document.getElementById('addMedicationForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    const name = document.getElementById('medName').value.trim();
    const type = document.getElementById('medType').value.trim();
    const stock = parseInt(document.getElementById('medStock').value || '0', 10);

    try {
      const res = await fetch('/api/medications', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({ name, type, stock })
      });
      if (!res.ok) throw new Error('HTTP ' + res.status);
      bootstrap.Modal.getInstance(document.getElementById('addMedicationModal')).hide();
      showToast("New Medication Added!");
      loadMedications();
      e.target.reset();
    } catch (err) {
      console.error('Add failed:', err);
      showToast("Add failed", "danger", "fa-triangle-exclamation");
    }
  });
});

// ---------- Image upload ----------
function triggerImageUpload(div) {
  const input = div.querySelector('input[type=file]');
  if (input) input.click();
}

async function uploadImage(id, input) {
  const file = input.files[0];
  if (!file) return;
  const formData = new FormData();
  formData.append('image', file);
  try {
    const r = await fetch(`/api/medications/${id}/image`, { method: 'POST', body: formData });
    const res = await r.json();
    if (res.error) throw new Error(res.error);
    showToast('Image uploaded successfully!');
    loadMedications();
  } catch (e) {
    console.error('Upload failed:', e);
    showToast('Upload failed', 'danger', 'fa-triangle-exclamation');
  }
}

// ---------- Delete (with floating confirm) ----------
async function deleteMedication(id, name) {
  showConfirm({
    title: "Delete Medication",
    message: `Are you sure you want to delete "<strong>${name}</strong>"? This cannot be undone.`,
    confirmText: "Delete",
    cancelText: "Cancel",
    onConfirm: async () => {
      try {
        const r = await fetch(`/api/medications/${id}`, { method: 'DELETE' });
        if (!r.ok) throw new Error('HTTP ' + r.status);
        showToast(`"${name}" deleted`, "danger", "fa-trash");
        loadMedications();
      } catch (e) {
        console.error('Delete failed:', e);
        showToast('Delete failed', 'danger', 'fa-triangle-exclamation');
      }
    }
  });
}
</script>

<style>
/* --- Images --- */
.image-box { width: 120px; height: 120px; position: relative; overflow: hidden; }
.med-image  { width: 120px; height: 120px; object-fit: cover; }

/* --- Soft toast (top-center) --- */
.soft-toast {
  position: fixed;
  top: 18px; left: 50%;
  transform: translate(-50%, -8px);
  min-width: 280px;
  border-radius: 14px;
  padding: .75rem 1rem;
  z-index: 3000;
  opacity: 0;
  transition: all .2s ease;
  box-shadow: 0 12px 30px rgba(0,0,0,.12);
}
.soft-toast.show {
  transform: translate(-50%, 0);
  opacity: 1;
}

/* --- Floating confirm card --- */
.confirm-toast {
  position: fixed;
  top: 18px; left: 50%;
  transform: translate(-50%, -8px);
  width: min(520px, 92vw);
  background: #fff;
  border-radius: 18px;
  padding: 16px 18px;
  z-index: 3100;
  opacity: 0;
  transition: all .2s ease;
  box-shadow: 0 16px 40px rgba(0,0,0,.16);
  border: 1px solid rgba(0,0,0,.04);
}
.confirm-toast.show {
  transform: translate(-50%, 0);
  opacity: 1;
}
.confirm-toast .icon-wrap {
  width: 36px; height: 36px;
  display: grid; place-items: center;
  border-radius: 50%;
  background: #fff3f3;
  color: #dc3545;
  flex: 0 0 36px;
}
.confirm-toast .btn-danger { box-shadow: 0 4px 10px rgba(220,53,69,.25); }
</style>
{% endblock %}"""
}

@bp.route("/medications")
def medications():
    return render_template("medications.html")