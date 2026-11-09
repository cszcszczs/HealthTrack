import sys
from pathlib import Path

from fastapi.testclient import TestClient

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "development" / "backend_healthtrack"))

from presentation.webapipatient import app

client = TestClient(app)


def test_get_patient_by_id_not_found_returns_404():
    response = client.get("/api/patients/no-existe")

    assert response.status_code == 404
    assert response.json()["detail"] == "Paciente no encontrado"


def test_delete_patient_not_found_returns_404():
    response = client.delete("/api/patients/no-existe")

    assert response.status_code == 404
    assert response.json()["detail"] == "Paciente no encontrado"


def test_deactivated_patient_is_available_when_including_inactive():
    created = client.post(
        "/api/patients",
        json={
            "firstName": "Paciente",
            "lastName": "Inactivo",
            "documentType": "CEDULA",
            "documentNumber": "123456789",
            "birthDate": "2000-01-01T00:00:00Z",
            "gender": "MASCULINO",
            "email": "inactivo@example.com",
            "phone": "3001234567",
            "city": "Bogotá",
            "address": "Calle 1",
        },
    )
    assert created.status_code == 200
    patient_id = created.json()["payload"]["id"]

    deactivated = client.delete(f"/api/patients/{patient_id}")
    assert deactivated.status_code == 200

    active_patients = client.get("/api/patients").json()["payload"]
    all_patients = client.get("/api/patients?include_inactive=true").json()["payload"]

    assert all(patient["id"] != patient_id for patient in active_patients)
    inactive_patient = next(patient for patient in all_patients if patient["id"] == patient_id)
    assert inactive_patient["isActive"] is False
