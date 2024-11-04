from my_project.auth.dao.GeneralDAO import GeneralDAO
from my_project.auth.models.patient import Patient
from my_project.db_init import db

class PatientDAO(GeneralDAO):
    def __init__(self):
        super().__init__(Patient)


    def get_by_id(self, id):
        return Patient.query.get(id)


    def get_all(self):
        return Patient.query.all()


    def create(self, data):
        new_patient = Patient(**data)
        db.session.add(new_patient)
        db.session.commit()
        return new_patient


    def update(self, id, data):
        patient = Patient.query.get(id)
        if patient:
            for key, value in data.items():
                setattr(patient, key, value)
            db.session.commit()
            return patient
        return None


    def delete(self, id):
        patient = Patient.query.get(id)
        if patient:
            db.session.delete(patient)
            db.session.commit()
            return True
        return False
