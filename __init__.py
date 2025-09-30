from flask import Flask
from flask_restx import Api, Resource, fields
from my_project.db_init import db
from config import config
import os

def create_app():
    app = Flask(__name__)
    
    # Load configuration
    config_name = os.environ.get('FLASK_ENV', 'development')
    app.config.from_object(config[config_name])
    
    # Initialize database
    db.init_app(app)
    
    # Initialize API with Swagger documentation
    api = Api(app, 
              version='1.0', 
              title='Hospital Management API',
              description='API для управління лікарнею, пацієнтами, лікарями та медикаментами',
              doc='/swagger/',
              prefix='/api/v1')
    
    # Import and register namespaces
    from my_project.auth.route.patient_route import patient_ns
    from my_project.auth.route.doctor_route import doctor_ns
    from my_project.auth.route.hospital_route import hospital_ns
    from my_project.auth.route.medication_route import medication_ns
    from my_project.auth.route.patient_medication_route import patient_medication_ns
    
    api.add_namespace(patient_ns, path='/patients')
    api.add_namespace(doctor_ns, path='/doctors')
    api.add_namespace(hospital_ns, path='/hospitals')
    api.add_namespace(medication_ns, path='/medications')
    api.add_namespace(patient_medication_ns, path='/patient-medications')
    
    return app