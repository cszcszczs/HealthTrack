from datetime import datetime, timezone
from uuid import uuid4

from fastapi import HTTPException, status

from domain.patient import Patient, PatientInput
from infraestructure.patientrepository import MemoryRepository


class PatientService:
    def __init__(self):
        self.repository = MemoryRepository()

    def consultar(self):
        return {
            "operacion": "Consulta realizada",
            "payload": self.repository.get_all(),
        }

    def consultar_por_id(self, patient_id: str):
        patient = self.repository.get_one(patient_id)
        if patient is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Paciente no encontrado",
            )
        return {
            "operacion": "Consulta realizada",
            "payload": patient,
        }

    def ingresar(self, patient_input: PatientInput):
        now = datetime.now(timezone.utc)
        patient = Patient(
            **patient_input.model_dump(),
            id=str(uuid4()),
            isActive=True,
            createdAt=now,
            updatedAt=now,
        )
        return {
            "operacion": "Ingreso realizado",
            "payload": self.repository.create(patient),
        }

    def modificar(self, patient_id: str, patient_input: PatientInput):
        stored_patient = self.repository.get_one(patient_id)
        if stored_patient is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Paciente no encontrado",
            )

        patient = Patient(
            **patient_input.model_dump(),
            id=stored_patient.id,
            isActive=True,
            createdAt=stored_patient.createdAt,
            updatedAt=datetime.now(timezone.utc),
        )
        return {
            "operacion": "Modificación realizada",
            "payload": self.repository.update(patient_id, patient),
        }

    def eliminar(self, patient_id: str):
        patient = self.repository.deactivate(
            patient_id,
            datetime.now(timezone.utc),
        )
        if patient is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Paciente no encontrado",
            )
        return {
            "operacion": "Eliminación realizada",
            "mensaje": "Paciente desactivado",
            "payload": None,
        }
