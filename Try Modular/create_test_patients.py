#!/usr/bin/env python3
"""
Create Test Patients
This script creates some test patients for the scan functionality.
"""

from main import create_app
from models import Patient
from extensions import db

def create_test_patients():
    app = create_app()
    with app.app_context():
        # Check if patients already exist
        existing_patients = Patient.query.all()
        if existing_patients:
            print(f"Patients already exist: {len(existing_patients)}")
            for p in existing_patients:
                print(f"- {p.name}")
            return
        
        print("Creating test patients...")
        
        # Create test patients
        patients_data = [
            {"name": "John Smith", "age": 45, "sex": "Male", "condition": "Onychomycosis", "severity": "Mild", "last_visit": "Today"},
            {"name": "Mary Johnson", "age": 32, "sex": "Female", "condition": "Healthy", "severity": "N/A", "last_visit": "Yesterday"},
            {"name": "Robert Brown", "age": 58, "sex": "Male", "condition": "Onychomycosis", "severity": "Moderate", "last_visit": "2 days ago"},
            {"name": "Sarah Davis", "age": 41, "sex": "Female", "condition": "Not set", "severity": "Mild", "last_visit": "1 week ago"},
            {"name": "Test Patient", "age": 30, "sex": "Other", "condition": "Not set", "severity": "Mild", "last_visit": "Today"}
        ]
        
        for patient_data in patients_data:
            patient = Patient(**patient_data)
            db.session.add(patient)
        
        try:
            db.session.commit()
            print(f"SUCCESS: Created {len(patients_data)} test patients!")
            
            # Verify creation
            all_patients = Patient.query.all()
            print(f"Total patients now in database: {len(all_patients)}")
            for p in all_patients:
                print(f"- {p.name} (Age: {p.age}, Sex: {p.sex})")
                
        except Exception as e:
            db.session.rollback()
            print(f"ERROR: Could not create test patients: {e}")

if __name__ == "__main__":
    create_test_patients()