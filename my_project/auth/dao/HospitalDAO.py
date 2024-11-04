from my_project.db_init import db
from my_project.auth.models.hospitals import Hospital

class HospitalDAO:
    def get_all(self):
        return Hospital.query.all()

    def get_by_id(self, hospital_id):
        return Hospital.query.get(hospital_id)

    def create(self, data):
        new_hospital = Hospital(**data)
        db.session.add(new_hospital)
        db.session.commit()
        return new_hospital

    def update(self, hospital_id, data):
        hospital = Hospital.query.get(hospital_id)
        if hospital:
            for key, value in data.items():
                setattr(hospital, key, value)
            db.session.commit()
            return hospital
        return None

    def delete(self, hospital_id):
        hospital = Hospital.query.get(hospital_id)
        if hospital:
            db.session.delete(hospital)
            db.session.commit()
            return True
        return False
