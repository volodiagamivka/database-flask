from flask_restx import Namespace, Resource, fields
from my_project.auth.controller.patient_medication_controller import (
    get_all_patient_medications,
    get_patient_medication_by_id,
    create_patient_medication,
    update_patient_medication,
    delete_patient_medication,
    get_medications_for_patient,
    get_patients_for_medication
)

patient_medication_ns = Namespace('patient-medications', description='Операції з призначеннями медикаментів пацієнтам')

# Моделі для Swagger документації
patient_medication_model = patient_medication_ns.model('PatientMedication', {
    'id': fields.Integer(readonly=True, description='ID призначення'),
    'patient_id': fields.Integer(required=True, description='ID пацієнта'),
    'medication_id': fields.Integer(required=True, description='ID медикаменту'),
    'dosage': fields.String(description='Дозування'),
    'start_date': fields.String(description='Дата початку прийому'),
    'end_date': fields.String(description='Дата закінчення прийому')
})

patient_medication_input_model = patient_medication_ns.model('PatientMedicationInput', {
    'patient_id': fields.Integer(required=True, description='ID пацієнта'),
    'medication_id': fields.Integer(required=True, description='ID медикаменту'),
    'dosage': fields.String(description='Дозування'),
    'start_date': fields.String(description='Дата початку прийому'),
    'end_date': fields.String(description='Дата закінчення прийому')
})

@patient_medication_ns.route('/')
class PatientMedicationList(Resource):
    @patient_medication_ns.doc('get_patient_medications')
    @patient_medication_ns.marshal_list_with(patient_medication_model)
    def get(self):
        """Отримати список всіх призначень медикаментів"""
        return get_all_patient_medications()
    
    @patient_medication_ns.doc('create_patient_medication')
    @patient_medication_ns.expect(patient_medication_input_model)
    @patient_medication_ns.marshal_with(patient_medication_model, code=201)
    def post(self):
        """Створити нове призначення медикаменту"""
        return create_patient_medication()

@patient_medication_ns.route('/<int:patient_medication_id>')
@patient_medication_ns.param('patient_medication_id', 'ID призначення')
class PatientMedication(Resource):
    @patient_medication_ns.doc('get_patient_medication')
    @patient_medication_ns.marshal_with(patient_medication_model)
    def get(self, patient_medication_id):
        """Отримати призначення за ID"""
        return get_patient_medication_by_id(patient_medication_id)
    
    @patient_medication_ns.doc('update_patient_medication')
    @patient_medication_ns.expect(patient_medication_input_model)
    @patient_medication_ns.marshal_with(patient_medication_model)
    def put(self, patient_medication_id):
        """Оновити призначення"""
        return update_patient_medication(patient_medication_id)
    
    @patient_medication_ns.doc('delete_patient_medication')
    def delete(self, patient_medication_id):
        """Видалити призначення"""
        return delete_patient_medication(patient_medication_id)

@patient_medication_ns.route('/patients/<int:patient_id>/medications')
@patient_medication_ns.param('patient_id', 'ID пацієнта')
class MedicationsForPatient(Resource):
    @patient_medication_ns.doc('get_medications_for_patient')
    def get(self, patient_id):
        """Отримати медикаменти для пацієнта"""
        return get_medications_for_patient(patient_id)

@patient_medication_ns.route('/medications/<int:medication_id>/patients')
@patient_medication_ns.param('medication_id', 'ID медикаменту')
class PatientsForMedication(Resource):
    @patient_medication_ns.doc('get_patients_for_medication')
    def get(self, medication_id):
        """Отримати пацієнтів для медикаменту"""
        return get_patients_for_medication(medication_id)
