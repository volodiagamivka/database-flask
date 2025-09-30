#!/usr/bin/env python3
"""
Database initialization script
"""
import os
import sys
from app import app, db

def init_db():
    """Initialize the database"""
    with app.app_context():
        try:
            # Create all tables
            db.create_all()
            print("Database tables created successfully!")
            
            # You can add initial data here if needed
            # Example:
            # from my_project.auth.models.patient import Patient
            # if not Patient.query.first():
            #     initial_patient = Patient(name="Test Patient", age=30, diagnosis="Test")
            #     db.session.add(initial_patient)
            #     db.session.commit()
            #     print("Initial data added!")
                
        except Exception as e:
            print(f"Error initializing database: {e}")
            sys.exit(1)

if __name__ == "__main__":
    init_db()
