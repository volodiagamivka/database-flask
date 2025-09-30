from flask_restx import Namespace, Resource, fields
from my_project.auth.controller.patient_controller import get_all_patients, get_patient_by_id, create_patient, update_patient, delete_patient

patient_ns = Namespace('patients', description='Операції з пацієнтами')

# Моделі для Swagger документації
patient_model = patient_ns.model('Patient', {
    'id': fields.Integer(readonly=True, description='ID пацієнта'),
    'name': fields.String(required=True, description='Ім\'я пацієнта'),
    'age': fields.Integer(required=True, description='Вік пацієнта'),
    'diagnosis': fields.String(description='Діагноз'),
    'doctor_id': fields.Integer(description='ID лікаря')
})

patient_input_model = patient_ns.model('PatientInput', {
    'name': fields.String(required=True, description='Ім\'я пацієнта'),
    'age': fields.Integer(required=True, description='Вік пацієнта'),
    'diagnosis': fields.String(description='Діагноз'),
    'doctor_id': fields.Integer(description='ID лікаря')
})

@patient_ns.route('/')
class PatientList(Resource):
    @patient_ns.doc('get_patients')
    @patient_ns.marshal_list_with(patient_model)
    def get(self):
        """Отримати список всіх пацієнтів"""
        return get_all_patients()
    
    @patient_ns.doc('create_patient')
    @patient_ns.expect(patient_input_model)
    @patient_ns.marshal_with(patient_model, code=201)
    def post(self):
        """Створити нового пацієнта"""
        return create_patient()

@patient_ns.route('/<int:patient_id>')
@patient_ns.param('patient_id', 'ID пацієнта')
class Patient(Resource):
    @patient_ns.doc('get_patient')
    @patient_ns.marshal_with(patient_model)
    def get(self, patient_id):
        """Отримати пацієнта за ID"""
        return get_patient_by_id(patient_id)
    
    @patient_ns.doc('update_patient')
    @patient_ns.expect(patient_input_model)
    @patient_ns.marshal_with(patient_model)
    def put(self, patient_id):
        """Оновити пацієнта"""
        return update_patient(patient_id)
    
    @patient_ns.doc('delete_patient')
    def delete(self, patient_id):
        """Видалити пацієнта"""
        return delete_patient(patient_id)
