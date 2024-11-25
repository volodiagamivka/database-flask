from flask import Flask
from __init__ import create_app
from my_project.auth.route.patient_route import patient_bp  # Імпортуємо маршрут для пацієнтів
from my_project.auth.route.medication_route import medication_bp  # Імпортуємо маршрут для медикаментів
from my_project.auth.route.patient_medication_route import patient_medications_bp
from  my_project.auth.route.doctor_route import doctor_bp
from my_project.auth.route.hospital_route import hospital_bp
from my_project.auth.route.department_route import department_bp
from my_project.auth.route.aggregate_route import aggregate_bp
from my_project.auth.route.historylog_route import history_log_bp
from my_project.auth.route.patient_tracker_route import patient_tracker_bp
app = create_app()

app.register_blueprint(patient_bp)
app.register_blueprint(medication_bp)
app.register_blueprint(patient_medications_bp)
app.register_blueprint(doctor_bp)
app.register_blueprint(hospital_bp)
app.register_blueprint(department_bp)
app.register_blueprint(aggregate_bp)
app.register_blueprint(history_log_bp)
app.register_blueprint(patient_tracker_bp)

if __name__ == '__main__':
    app.run(debug=True)
