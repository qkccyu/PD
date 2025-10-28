# pages/reports.py
from flask import Blueprint, render_template

bp = Blueprint("reports_page", __name__)

TEMPLATES = {
"reports.html": """{% extends "base.html" %}{% block content %}
<h2 class="mb-3">Recent Reports</h2>

<div class="d-flex justify-content-between align-items-center mb-3">
  <div class="text-muted small">Latest saved scans</div>
  <button class="btn btn-light btn-sm" id="refreshBtn"><i class="fa-solid fa-rotate"></i> Refresh</button>
</div>

<div id="reportsContainer" class="row g-3"></div>

<script>
function badgeFor(cond, sev){
  if(cond === 'Healthy') return '<span class="badge bg-success">Healthy</span>';
  const map = { Mild:'bg-success bg-opacity-25 text-success',
                Moderate:'bg-warning text-dark',
                Severe:'bg-danger' };
  return '<span class="badge '+(map[sev]||'bg-secondary')+'">'+cond+' - '+sev+'</span>';
}

async function loadReports(){
  const container = document.getElementById('reportsContainer');
  container.innerHTML = '';
  try{
    const r = await fetch('/api/scans');
    const data = await r.json();
    if(!Array.isArray(data) || !data.length){
      container.innerHTML = '<div class="col-12 text-center text-muted py-4">No reports yet.</div>';
      return;
    }
    data.forEach(s=>{
      const card = document.createElement('div');
      card.className = 'col-md-6';
      card.innerHTML = `
        <div class="card h-100 shadow-sm border-0">
          <div class="card-body d-flex gap-3">
            <div class="flex-shrink-0">
              ${s.image_url ? `<img src="${s.image_url}" class="rounded border" style="width:120px;height:120px;object-fit:cover;">`
                            : `<div class="bg-light rounded d-flex align-items-center justify-content-center" style="width:120px;height:120px;">N/A</div>`}
            </div>
            <div class="flex-grow-1">
              <div class="d-flex justify-content-between">
                <h5 class="mb-1">${s.patient_name}</h5>
                <small class="text-muted">${new Date(s.created_at).toLocaleString()}</small>
              </div>
              <div class="mb-2">${badgeFor(s.condition, s.severity)}</div>
              ${s.notes ? `<div class="small text-muted"><i class="fa-regular fa-note-sticky me-1"></i>${s.notes}</div>`:''}
            </div>
          </div>
        </div>`;
      container.appendChild(card);
    });
  }catch(e){
    console.error(e);
    container.innerHTML = '<div class="col-12 text-center text-danger py-4">Failed to load reports.</div>';
  }
}
document.getElementById('refreshBtn').onclick = loadReports;
window.addEventListener('DOMContentLoaded', loadReports);
</script>
{% endblock %}"""
}

@bp.route("/reports")
def reports():
    return render_template("reports.html")
