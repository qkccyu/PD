# api/scans_api.py
import os
from datetime import datetime
from flask import Blueprint, request, jsonify, current_app
from werkzeug.utils import secure_filename
from models import Scan
from extensions import db

bp = Blueprint("scans_api", __name__)

def _image_url(filename):
    if not filename:
        return None
    return f"/static/uploads/scans/{filename}"

@bp.route("/api/scans", methods=["GET"])
def list_scans():
    # newest first
    scans = Scan.query.order_by(Scan.created_at.desc()).all()
    return jsonify([
        {
            "id": s.id,
            "patient_name": s.patient_name,
            "notes": s.notes,
            "condition": s.condition,
            "severity": s.severity,
            "created_at": s.created_at.isoformat(),
            "image_url": _image_url(s.image_filename),
            "analyzed": s.analyzed,
        }
        for s in scans
    ])

@bp.route("/api/scans", methods=["POST"])
def save_scan():
    # Accepts multipart/form-data
    patient_name = request.form.get("patient_name")
    notes = request.form.get("notes")
    condition = request.form.get("condition") or "Onychomycosis"
    severity = request.form.get("severity") or ("N/A" if condition == "Healthy" else "Mild")
    image = request.files.get("image")

    # Debug information
    print(f"DEBUG SCAN API: patient_name='{patient_name}', image={image is not None}")
    print(f"DEBUG SCAN API: form data keys: {list(request.form.keys())}")
    print(f"DEBUG SCAN API: files keys: {list(request.files.keys())}")

    if not patient_name or not image:
        error_msg = "Missing patient name or image"
        if not patient_name:
            error_msg += " (patient_name is missing)"
        if not image:
            error_msg += " (image is missing)"
        print(f"DEBUG SCAN API: Error - {error_msg}")
        return jsonify({"error": error_msg}), 400

    filename = secure_filename(image.filename)
    upload_dir = os.path.join(current_app.static_folder, "uploads", "scans")
    os.makedirs(upload_dir, exist_ok=True)
    image.save(os.path.join(upload_dir, filename))

    new_scan = Scan(
        patient_name=patient_name,
        notes=notes,
        image_filename=filename,
        condition=condition,
        severity=severity,
        analyzed=True,
        created_at=datetime.utcnow(),
    )
    db.session.add(new_scan)
    db.session.commit()

    return jsonify({
        "id": new_scan.id,
        "patient_name": new_scan.patient_name,
        "notes": new_scan.notes,
        "condition": new_scan.condition,
        "severity": new_scan.severity,
        "created_at": new_scan.created_at.isoformat(),
        "image_url": _image_url(new_scan.image_filename),
        "message": f"Scan saved for {patient_name}"
    }), 201
