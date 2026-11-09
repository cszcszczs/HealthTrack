# Backend de HealthTrack

API REST para registrar, consultar, actualizar y desactivar pacientes. Está construida con FastAPI y valida los datos mediante modelos de Pydantic.

## Requisitos

- Python 3.10 o superior.
- `pip`.

## Instalación y ejecución

Desde la raíz del repositorio:

```bash
cd development/backend_healthtrack
python -m venv .venv
```

Activa el entorno virtual:

```bash
# Linux o macOS
source .venv/bin/activate

# Windows PowerShell
.venv\Scripts\Activate.ps1
```

Instala las dependencias e inicia el servidor:

```bash
python -m pip install fastapi uvicorn
python main.py
```

La API queda disponible en `http://localhost:7000`. La documentación interactiva de FastAPI está en <http://localhost:7000/docs> y el esquema OpenAPI en <http://localhost:7000/openapi.json>.

Para ejecutar las pruebas desde la raíz del repositorio, instala además `pytest` y `httpx` en el mismo entorno:

```bash
python -m pip install pytest httpx
cd ../..
python -m pytest -q tests/test_patient_api.py
```

## Cómo funciona

El backend separa responsabilidades en cuatro módulos:

- `domain/patient.py`: define los datos requeridos para un paciente (`PatientInput`), los campos del registro completo (`Patient`) y los valores válidos de tipo de documento y género.
- `application/patientservice.py`: aplica las operaciones de negocio, crea UUID y fechas, y traduce registros inexistentes a errores HTTP 404.
- `infraestructure/patientrepository.py`: almacena y consulta los pacientes en memoria. La desactivación es lógica: cambia `isActive` a `false` y conserva el registro.
- `presentation/webapipatient.py`: expone las rutas FastAPI y configura CORS para el frontend local en los puertos 5173.
- `main.py`: inicia Uvicorn en `localhost:7000` con recarga automática.

**Importante:** el repositorio actual es en memoria, no una base de datos. Los pacientes se pierden cuando se detiene o reinicia el proceso del servidor.

## Endpoints

| Método | Ruta | Descripción |
|---|---|---|
| `GET` | `/` | Comprueba que la API está activa. |
| `GET` | `/api/patients` | Lista los pacientes activos. |
| `GET` | `/api/patients?include_inactive=true` | Lista todos los pacientes, incluidos los inactivos. |
| `GET` | `/api/patients/{patient_id}` | Consulta un paciente activo por UUID. |
| `POST` | `/api/patients` | Crea un paciente activo. |
| `PUT` | `/api/patients/{patient_id}` | Actualiza un paciente activo. |
| `DELETE` | `/api/patients/{patient_id}` | Desactiva un paciente sin eliminarlo del almacenamiento. |

Las operaciones de listado y creación devuelven un objeto con `operacion` y `payload`. La desactivación devuelve `operacion`, `mensaje` y un `payload` nulo. Las rutas por UUID responden con HTTP 404 cuando el paciente no está disponible.

## Ejemplo de creación

```bash
curl -X POST http://localhost:7000/api/patients \
  -H "Content-Type: application/json" \
  -d '{
    "firstName": "Ana",
    "lastName": "Ejemplo",
    "documentType": "CEDULA",
    "documentNumber": "123456789",
    "birthDate": "2000-01-01T00:00:00Z",
    "gender": "FEMENINO",
    "email": "ana@example.com",
    "phone": "3001234567",
    "city": "Bogota",
    "address": "Calle 1"
  }'
```

La respuesta contiene el UUID generado en `payload.id`. Usa ese valor para consultar, actualizar o desactivar el registro.
