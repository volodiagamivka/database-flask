from my_project.auth.dao.DoctorDAO import DoctorDAO

class DoctorService:
    def __init__(self):
        self.doctor_dao = DoctorDAO()

    def get_all_doctors(self):
        return self.doctor_dao.get_all()

    def get_doctor_by_id(self, doctor_id):
        return self.doctor_dao.get_by_id(doctor_id)

    def create_doctor(self, data):
        return self.doctor_dao.create(data)

    def update_doctor(self, doctor_id, data):
        return self.doctor_dao.update(doctor_id, data)

    def delete_doctor(self, doctor_id):
        return self.doctor_dao.delete(doctor_id)

    def get_doctors_with_hospital(self):

        doctors = self.doctor_dao.get_all()
        result = []
        for doctor in doctors:
            result.append({
                'doctors_id': doctor.doctors_id,
                'first_name': doctor.first_name,
                'last_name': doctor.last_name,
                'specialization': doctor.specialization,
                'hospital': {
                    'hospital_id': doctor.hospital.hospital_id,
                    'name': doctor.hospital.name,
                    'address': doctor.hospital.address
                }
            })
        return result