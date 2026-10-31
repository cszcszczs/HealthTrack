# HealthTrack — Frontend React para CRUD de pacientes

Frontend modular para practicar la integración de React + Axios con una API REST construida en FastAPI. Incluye listado/filtrado, registro, actualización, consulta por UUID, desactivación lógica y un inspector de tráfico HTTP que muestra método, URL, request body, response body, estado HTTP y duración.

## Requisitos
- Node.js 20 o superior (recomendado) y npm.
- Backend FastAPI iniciado y accesible en `http://127.0.0.1:7000`.

## Ejecutar

```bash
# 1. Descomprime el ZIP y entra a la carpeta
cd pacientes-frontend

# 2. Instala dependencias
npm install

# 3. (Opcional) configura la URL del backend
cp .env.example .env
# Edita VITE_API_BASE_URL si el backend usa otra dirección/puerto.

# 4. Inicia Vite
npm run dev
```

Abre la URL local que imprime Vite (normalmente `http://localhost:5173`). Para generar una compilación de producción: `npm run build`; para previsualizarla: `npm run preview`.

## Conexión con FastAPI
- Base URL predeterminada: `http://127.0.0.1:7000`.
- `GET /api/patients`: carga el directorio.
- `POST /api/patients`: crea un paciente.
- `GET /api/patients/{patient_id}`: consulta por UUID.
- `PUT /api/patients/{patient_id}`: actualiza el paciente.
- `DELETE /api/patients/{patient_id}`: solicita desactivación lógica.
- Se espera el formato descrito en el contrato compartido: `{ "operacion": "...", "payload": ... }` para operaciones que devuelven datos. El listado espera que `payload` sea un array y las consultas individuales que sea un objeto.

### CORS
Si Vite corre en `http://localhost:5173`, configura CORS en FastAPI para permitir ese origen. Ejemplo orientativo en tu aplicación FastAPI:

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

Añade el middleware después de crear `app = FastAPI(...)`. Ajusta los orígenes a los que realmente utilices; no uses `allow_origins=["*"]` junto con credenciales.

## Inspector HTTP
Los interceptores de `src/services/http.js` registran automáticamente cada solicitud y su respuesta o error. El panel conserva las últimas 40 entradas de la sesión y permite seleccionar una entrada, copiar los payloads y borrar el historial. Las respuestas HTTP fallidas muestran el cuerpo de error que devuelva FastAPI, si existe. Un error de red/CORS se representa con estado `0` porque el navegador no expone un código HTTP.

## Estructura
```text
src/
├── components/
│   ├── HttpInspector.jsx
│   ├── PatientDetail.jsx
│   ├── PatientForm.jsx
│   └── PatientTable.jsx
├── services/
│   ├── http.js             # Axios, interceptores y captura HTTP
│   └── patientsApi.js      # Métodos CRUD
├── utils/
│   └── patient.js          # Normalización de formulario/payload
├── App.jsx                 # Composición de módulos y estado de pantalla
├── main.jsx
└── styles.css
```

## Notas de integración
- El frontend usa `VITE_API_BASE_URL`; las variables `VITE_` se leen durante el arranque/build de Vite.
- La fecha se envía en ISO 8601 UTC (`YYYY-MM-DDT00:00:00.000Z`).
- El botón “Desactivar” ejecuta el `DELETE` descrito en el contrato; el frontend no elimina localmente el registro hasta volver a consultar la API.
- Si tu backend utiliza nombres de campos, enums o respuestas distintos, ajusta `src/utils/patient.js` y `src/services/patientsApi.js`.
- Los archivos Python que se mencionan en la solicitud no aparecieron adjuntos en esta conversación. Por eso, el cliente se implementó contra el contrato REST incluido en el prompt; valida las rutas y los modelos reales del backend antes de entregar.
