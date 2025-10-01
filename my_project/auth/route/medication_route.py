from flask_restx import Namespace, Resource, fields
from my_project.auth.controller.medication_controller import get_all_medications, get_medication_by_id, create_medication, update_medication, delete_medication

medication_ns = Namespace('medications', description='Операції з медикаментами')

# Моделі для Swagger документації
medication_model = medication_ns.model('Medication', {
    'id': fields.Integer(readonly=True, description='ID медикаменту'),
    'name': fields.String(required=True, description='Назва медикаменту'),
    'dosage': fields.String(description='Дозування'),
    'description': fields.String(description='Опис медикаменту')
})

medication_input_model = medication_ns.model('MedicationInput', {
    'name': fields.String(required=True, description='Назва медикаменту'),
    'dosage': fields.String(description='Дозування'),
    'description': fields.String(description='Опис медикаменту')
})

@medication_ns.route('/')
class MedicationList(Resource):
    @medication_ns.doc('get_medications')
    @medication_ns.marshal_list_with(medication_model)
    def get(self):
        """Отримати список всіх медикаментів"""
        return get_all_medications()
    
    @medication_ns.doc('create_medication')
    @medication_ns.expect(medication_input_model)
    @medication_ns.marshal_with(medication_model, code=201)
    def post(self):
        """Створити новий медикамент"""
        return create_medication()

@medication_ns.route('/<int:medication_id>')
@medication_ns.param('medication_id', 'ID медикаменту')
class Medication(Resource):
    @medication_ns.doc('get_medication')
    @medication_ns.marshal_with(medication_model)
    def get(self, medication_id):
        """Отримати медикамент за ID"""
        return get_medication_by_id(medication_id)
    
    @medication_ns.doc('update_medication')
    @medication_ns.expect(medication_input_model)
    @medication_ns.marshal_with(medication_model)
    def put(self, medication_id):
        """Оновити медикамент"""
        return update_medication(medication_id)
    
    @medication_ns.doc('delete_medication')
    def delete(self, medication_id):
        """Видалити медикамент"""
        return delete_medication(medication_id)
