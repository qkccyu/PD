from flask import Blueprint, jsonify, request
from extensions import db
from models import Patient

bp = Blueprint("patients_api", __name__, url_prefix="/api")

@bp.get("/patients")
def get_patients():
    pts = Patient.query.all()
    return jsonify([{
        "id": p.id, "name": p.name, "age": p.age, "sex": p.sex,
        "condition": p.condition, "severity": p.severity, "last_visit": p.last_visit
    } for p in pts])

@bp.post("/patients")
def add_patient():
    data = request.get_json()
    p = Patient(name=data["name"], age=data["age"], sex=data["sex"],
                last_visit="Today", condition="Not set", severity="Mild")
    db.session.add(p)
    db.session.commit()
    return jsonify({
        "id": p.id, "name": p.name, "age": p.age, "sex": p.sex,
        "condition": p.condition, "severity": p.severity, "last_visit": p.last_visit
    })

@bp.put("/patients/<int:pid>")
def update_patient(pid):
    p = Patient.query.get_or_404(pid)
    data = request.get_json()
    p.last_visit = data.get("last_visit", p.last_visit)
    p.condition  = data.get("condition",  p.condition)
    p.severity   = data.get("severity",   p.severity)
    db.session.commit()
    return jsonify({
        "id": p.id, "name": p.name, "age": p.age, "sex": p.sex,
        "condition": p.condition, "severity": p.severity, "last_visit": p.last_visit
    })

@bp.delete("/patients/<int:pid>")
def delete_patient(pid):
    p = Patient.query.get_or_404(pid)
    db.session.delete(p)
    db.session.commit()
    return jsonify({"message": "Patient deleted successfully"})
