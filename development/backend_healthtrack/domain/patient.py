from datetime import datetime
from enum import Enum

from pydantic import BaseModel


class DocumentType(str, Enum):
    CEDULA = "CEDULA"
    TARJETA_IDENTIDAD = "TARJETA_IDENTIDAD"
    PASAPORTE = "PASAPORTE"
    CEDULA_EXTRANJERIA = "CEDULA_EXTRANJERIA"


class Gender(str, Enum):
    MASCULINO = "MASCULINO"
    FEMENINO = "FEMENINO"
    OTRO = "OTRO"


class PatientInput(BaseModel):
    firstName: str
    lastName: str
    documentType: DocumentType
    documentNumber: str
    birthDate: datetime
    gender: Gender
    email: str
    phone: str
    city: str
    address: str


class Patient(PatientInput):
    id: str
    isActive: bool
    createdAt: datetime
    updatedAt: datetime
