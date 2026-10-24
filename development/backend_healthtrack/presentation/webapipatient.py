from fastapi import FastAPI

from domain.patient import PatientInput
from application.patientservice import PatientService

app = FastAPI(
    title="HealthTrack API",
    description="API para la gestión de pacientes de HealthTrack",
    version="1.0.0"
)

service = PatientService()

@app.get(
    "/",
    summary="Estado de HealthTrack",
    description="Comprueba que la API de HealthTrack está funcionando",
    tags=["HealthTrack"]
)
async def inicio():
    return {
        "mensaje": "API HealthTrack funcionando"
    }


# --------------------------------
# GET - Consulta
# --------------------------------

@app.get(
    "/api/patients",
    summary="Consultar pacientes",
    description="Consultar pacientes activos",
    tags=["Patients"]
)
async def consultar():
    return service.consultar()


# --------------------------------
# GET ONE - Consulta por ID
# --------------------------------

@app.get(
    "/api/patients/{patient_id}",
    summary="Consultar paciente por ID",
    description="Consultar un paciente activo por su ID",
    tags=["Patients"]
)
async def consultar_por_id(patient_id: str):
    return service.consultar_por_id(patient_id)


# --------------------------------
# POST - Ingreso
# --------------------------------

@app.post(
    "/api/patients",
    summary="Registrar paciente",
    description="Registrar un paciente",
    tags=["Patients"]
)
async def ingresar(patient: PatientInput):
    return service.ingresar(patient)


# --------------------------------
# PUT - Modificación
# --------------------------------

@app.put(
    "/api/patients/{patient_id}",
    summary="Actualizar paciente",
    description="Actualizar los datos de un paciente activo",
    tags=["Patients"]
)
async def modificar(patient_id: str, patient: PatientInput):
    return service.modificar(patient_id, patient)


# --------------------------------
# DELETE - Eliminación
# --------------------------------

@app.delete(
    "/api/patients/{patient_id}",
    summary="Desactivar paciente",
    description="Desactivar un paciente",
    tags=["Patients"]
)
async def eliminar(patient_id: str):
    return service.eliminar(patient_id)
