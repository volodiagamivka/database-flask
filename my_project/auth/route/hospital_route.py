from flask import Blueprint
from my_project.auth.controller.hospitals_controller import (
    get_all_hospitals, get_hospital_by_id, create_hospital, update_hospital, delete_hospital
)

hospital_bp = Blueprint('hospital', __name__)

hospital_bp.route('/hospitals', methods=['GET'])(get_all_hospitals)
hospital_bp.route('/hospitals/<int:hospital_id>', methods=['GET'])(get_hospital_by_id)
hospital_bp.route('/hospitals', methods=['POST'])(create_hospital)
hospital_bp.route('/hospitals/<int:hospital_id>', methods=['PUT'])(update_hospital)
hospital_bp.route('/hospitals/<int:hospital_id>', methods=['DELETE'])(delete_hospital)
