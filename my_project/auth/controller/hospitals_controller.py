from flask import request, jsonify
from my_project.auth.service.HospitalService import HospitalService

hospital_service = HospitalService()


def get_all_hospitals():
    hospitals = hospital_service.get_all_hospitals()
    return jsonify([hospital.to_dict() for hospital in hospitals]), 200


def get_hospital_by_id(hospital_id):
    hospital = hospital_service.get_hospital_by_id(hospital_id)
    if hospital:
        return jsonify(hospital.to_dict()), 200
    return jsonify({'message': 'Hospital not found'}), 404


def create_hospital():
    data = request.json
    new_hospital = hospital_service.create_hospital(data)
    return jsonify(new_hospital.to_dict()), 201


def update_hospital(hospital_id):
    data = request.json
    updated_hospital = hospital_service.update_hospital(hospital_id, data)
    if updated_hospital:
        return jsonify(updated_hospital.to_dict()), 200
    return jsonify({'message': 'Hospital not found'}), 404


def delete_hospital(hospital_id):
    success = hospital_service.delete_hospital(hospital_id)
    if success:
        return jsonify({'message': 'Hospital deleted successfully'}), 200
    return jsonify({'message': 'Hospital not found'}), 404

