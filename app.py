from flask import Flask
from __init__ import create_app
from my_project.auth.route.patient_route import patient_bp  # Імпортуємо маршрут для пацієнтів
from my_project.auth.route.medication_route import medication_bp  # Імпортуємо маршрут для медикаментів
from my_project.auth.route.patient_medication_route import patient_medications_bp
from  my_project.auth.route.doctor_route import doctor_bp
from my_project.auth.route.hospital_route import hospital_bp

app = create_app()

app.register_blueprint(patient_bp)
app.register_blueprint(medication_bp)
app.register_blueprint(patient_medications_bp)
app.register_blueprint(doctor_bp)
app.register_blueprint(hospital_bp)

if __name__ == '__main__':
    app.run(debug=True)
