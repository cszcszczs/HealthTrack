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
