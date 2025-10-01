from flask_restx import Namespace, Resource, fields
from my_project.auth.controller.hospitals_controller import (
    get_all_hospitals, get_hospital_by_id, create_hospital, update_hospital, delete_hospital
)

hospital_ns = Namespace('hospitals', description='Операції з лікарнями')

# Моделі для Swagger документації
hospital_model = hospital_ns.model('Hospital', {
    'id': fields.Integer(readonly=True, description='ID лікарні'),
    'name': fields.String(required=True, description='Назва лікарні'),
    'address': fields.String(description='Адреса лікарні'),
    'phone': fields.String(description='Телефон лікарні')
})

hospital_input_model = hospital_ns.model('HospitalInput', {
    'name': fields.String(required=True, description='Назва лікарні'),
    'address': fields.String(description='Адреса лікарні'),
    'phone': fields.String(description='Телефон лікарні')
})

@hospital_ns.route('/')
class HospitalList(Resource):
    @hospital_ns.doc('get_hospitals')
    @hospital_ns.marshal_list_with(hospital_model)
    def get(self):
        """Отримати список всіх лікарень"""
        return get_all_hospitals()
    
    @hospital_ns.doc('create_hospital')
    @hospital_ns.expect(hospital_input_model)
    @hospital_ns.marshal_with(hospital_model, code=201)
    def post(self):
        """Створити нову лікарню"""
        return create_hospital()

@hospital_ns.route('/<int:hospital_id>')
@hospital_ns.param('hospital_id', 'ID лікарні')
class Hospital(Resource):
    @hospital_ns.doc('get_hospital')
    @hospital_ns.marshal_with(hospital_model)
    def get(self, hospital_id):
        """Отримати лікарню за ID"""
        return get_hospital_by_id(hospital_id)
    
    @hospital_ns.doc('update_hospital')
    @hospital_ns.expect(hospital_input_model)
    @hospital_ns.marshal_with(hospital_model)
    def put(self, hospital_id):
        """Оновити лікарню"""
        return update_hospital(hospital_id)
    
    @hospital_ns.doc('delete_hospital')
    def delete(self, hospital_id):
        """Видалити лікарню"""
        return delete_hospital(hospital_id)
