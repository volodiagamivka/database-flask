from my_project.auth.dao.HospitalDAO import HospitalDAO

class HospitalService:
    def __init__(self):
        self.hospital_dao = HospitalDAO()

    def get_all_hospitals(self):
        return self.hospital_dao.get_all()

    def get_hospital_by_id(self, hospital_id):
        return self.hospital_dao.get_by_id(hospital_id)

    def create_hospital(self, data):
        return self.hospital_dao.create(data)

    def update_hospital(self, hospital_id, data):
        return self.hospital_dao.update(hospital_id, data)

    def delete_hospital(self, hospital_id):
        return self.hospital_dao.delete(hospital_id)

