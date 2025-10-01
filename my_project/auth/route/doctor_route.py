from flask_restx import Namespace, Resource, fields
from my_project.auth.controller.doctor_controller import (
    get_all_doctors, get_doctor_by_id, create_doctor, update_doctor, delete_doctor, get_doctors_with_hospital
)

doctor_ns = Namespace('doctors', description='Операції з лікарями')

# Моделі для Swagger документації
doctor_model = doctor_ns.model('Doctor', {
    'id': fields.Integer(readonly=True, description='ID лікаря'),
    'name': fields.String(required=True, description='Ім\'я лікаря'),
    'specialization': fields.String(description='Спеціалізація'),
    'hospital_id': fields.Integer(description='ID лікарні')
})

doctor_input_model = doctor_ns.model('DoctorInput', {
    'name': fields.String(required=True, description='Ім\'я лікаря'),
    'specialization': fields.String(description='Спеціалізація'),
    'hospital_id': fields.Integer(description='ID лікарні')
})

@doctor_ns.route('/')
class DoctorList(Resource):
    @doctor_ns.doc('get_doctors')
    @doctor_ns.marshal_list_with(doctor_model)
    def get(self):
        """Отримати список всіх лікарів"""
        return get_all_doctors()
    
    @doctor_ns.doc('create_doctor')
    @doctor_ns.expect(doctor_input_model)
    @doctor_ns.marshal_with(doctor_model, code=201)
    def post(self):
        """Створити нового лікаря"""
        return create_doctor()

@doctor_ns.route('/<int:doctor_id>')
@doctor_ns.param('doctor_id', 'ID лікаря')
class Doctor(Resource):
    @doctor_ns.doc('get_doctor')
    @doctor_ns.marshal_with(doctor_model)
    def get(self, doctor_id):
        """Отримати лікаря за ID"""
        return get_doctor_by_id(doctor_id)
    
    @doctor_ns.doc('update_doctor')
    @doctor_ns.expect(doctor_input_model)
    @doctor_ns.marshal_with(doctor_model)
    def put(self, doctor_id):
        """Оновити лікаря"""
        return update_doctor(doctor_id)
    
    @doctor_ns.doc('delete_doctor')
    def delete(self, doctor_id):
        """Видалити лікаря"""
        return delete_doctor(doctor_id)

@doctor_ns.route('/hospitals/<int:hospital_id>')
@doctor_ns.param('hospital_id', 'ID лікарні')
class DoctorsByHospital(Resource):
    @doctor_ns.doc('get_doctors_by_hospital')
    @doctor_ns.marshal_list_with(doctor_model)
    def get(self, hospital_id):
        """Отримати лікарів за лікарнею"""
        return get_doctors_with_hospital(hospital_id)