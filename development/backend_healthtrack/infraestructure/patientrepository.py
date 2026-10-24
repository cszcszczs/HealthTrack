from datetime import datetime

from domain.patient import Patient


class MemoryRepository:
    def __init__(self):
        self.patients: list[Patient] = []

    def get_all(self):
        return [patient for patient in self.patients if patient.isActive]

    def get_one(self, patient_id: str):
        return next(
            (
                patient
                for patient in self.patients
                if patient.id == patient_id and patient.isActive
            ),
            None,
        )

    def create(self, patient: Patient):
        self.patients.append(patient)
        return patient

    def update(self, patient_id: str, patient: Patient):
        for index, stored_patient in enumerate(self.patients):
            if stored_patient.id == patient_id and stored_patient.isActive:
                self.patients[index] = patient
                return patient
        return None

    def deactivate(self, patient_id: str, updated_at: datetime):
        for index, patient in enumerate(self.patients):
            if patient.id == patient_id and patient.isActive:
                deactivated = patient.model_copy(
                    update={"isActive": False, "updatedAt": updated_at}
                )
                self.patients[index] = deactivated
                return deactivated
        return None
