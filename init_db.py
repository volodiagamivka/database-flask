#!/usr/bin/env python3
"""
Database initialization script
"""
import os
import sys
from app import app
from my_project.db_init import db

# Import all models to ensure they are registered
from my_project.auth.models.patient import Patient
from my_project.auth.models.doctors import Doctor
from my_project.auth.models.hospitals import Hospital
from my_project.auth.models.medication import Medication
from my_project.auth.models.patient_medications_model import PatientMedications

def init_db():
    """Initialize the database"""
    with app.app_context():
        try:
            # Create all tables
            db.create_all()
            print("Database tables created successfully!")
            
            # You can add initial data here if needed
            # Example:
            # if not Patient.query.first():
            #     initial_patient = Patient(
            #         first_name="Test", 
            #         last_name="Patient", 
            #         date_of_birthday="1990-01-01",
            #         gender="Male",
            #         address="Test Address",
            #         phone="1234567890"
            #     )
            #     db.session.add(initial_patient)
            #     db.session.commit()
            #     print("Initial data added!")
                
        except Exception as e:
            print(f"Error initializing database: {e}")
            sys.exit(1)

if __name__ == "__main__":
    init_db()
