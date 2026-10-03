#webliberria.py

from fastapi import FastAPI, responses

from domain.entitylibreria import EntityLiberira

librerias = []

app = FastAPI(
    title="API Libreria",
    description="API para la libreria",
    version="1.0.0"
)

## GET
@app.get(
    "/consultarlibreriatodo",
    summary="Consultar Libreria Todo",
    description="Consultar Liberia Todo",
    tags=["Libreria"]
)
async def constultar_libreria_todo():
    return librerias

@app.get(
    "/consultarlibreria/{IdLibreria}",
    summary="Consultar Libreria Uno",
    description="Consultar Liberia Uno",
    tags=["Libreria"]
)
async def constultar_libreria_uno(IdLibreria: int):
    return list(filter(lambda libreria: IdLibreria == libreria.Idlibreria, librerias))

## POST
@app.post("/librerias")
async def crear_libro(libreria: EntityLiberira):
    librerias.append(libreria)
    return { "message": "Item created"}
