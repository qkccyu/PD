import os
from flask import Blueprint, jsonify, request, current_app
from werkzeug.utils import secure_filename
from extensions import db
from models import Medication

bp = Blueprint("meds_api", __name__, url_prefix="/api")

def _allowed(filename: str) -> bool:
    return "." in filename and filename.rsplit(".",1)[-1].lower() in current_app.config["ALLOWED_IMAGE_EXTENSIONS"]

@bp.get("/medications")
def get_meds():
    meds = Medication.query.all()
    return jsonify([{
        "id": m.id, "name": m.name, "type": m.type, "stock": m.stock,
        "image_url": f"/static/uploads/scans/{m.image_filename}" if m.image_filename else None
    } for m in meds])

@bp.post("/medications")
def add_med():
    data = request.get_json()
    m = Medication(name=data["name"], type=data["type"], stock=data["stock"])
    db.session.add(m); db.session.commit()
    return jsonify({"id": m.id, "name": m.name, "type": m.type, "stock": m.stock, "image_url": None})

@bp.put("/medications/<int:mid>")
def update_med(mid):
    m = Medication.query.get_or_404(mid)
    data = request.get_json()
    m.name, m.type, m.stock = data["name"], data["type"], data["stock"]
    db.session.commit()
    return jsonify({"id": m.id, "name": m.name, "type": m.type, "stock": m.stock})

@bp.delete("/medications/<int:mid>")
def delete_med(mid):
    m = Medication.query.get_or_404(mid)
    db.session.delete(m); db.session.commit()
    return jsonify({"message": "Medication deleted successfully"})

@bp.post("/medications/<int:mid>/image")
def upload_med_image(mid):
    m = Medication.query.get_or_404(mid)
    file = request.files.get("image")
    if not file or not _allowed(file.filename):
        return jsonify({"error": "No/invalid image"}), 400
    filename = secure_filename(file.filename)
    dest = os.path.join(current_app.config["UPLOAD_FOLDER"], filename)
    os.makedirs(current_app.config["UPLOAD_FOLDER"], exist_ok=True)
    file.save(dest)
    m.image_filename = filename
    db.session.commit()
    return jsonify({"message": "Image uploaded successfully"})
