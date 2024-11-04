from flask import request, jsonify
from my_project.auth.service.PatientService import PatientService

patient_service = PatientService()


def get_all_patients():
    patients = patient_service.get_all_patients()
    return jsonify([patient.to_dict() for patient in patients]), 200

def get_patient_by_id(patient_id):
    patient = patient_service.get_patient_by_id(patient_id)
    if patient:
        return jsonify(patient.to_dict()), 200
    return jsonify({'message': 'Patient not found'}), 404


def create_patient():
    data = request.json
    new_patient = patient_service.create_patient(data)
    return jsonify(new_patient.to_dict()), 201


def update_patient(patient_id):
    data = request.json
    updated_patient = patient_service.update_patient(patient_id, data)
    if updated_patient:
        return jsonify(updated_patient.to_dict()), 200
    return jsonify({'message': 'Patient not found'}), 404


def delete_patient(patient_id):
    success = patient_service.delete_patient(patient_id)
    if success:
        return jsonify({'message': 'Patient deleted successfully'}), 200
    return jsonify({'message': 'Patient not found'}), 404

def get_patients_with_medications():
    patients_with_medications = patient_service.get_patients_with_medications()
    return jsonify(patients_with_medications), 200