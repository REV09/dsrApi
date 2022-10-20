from fastapi import APIRouter, HTTPException, Response
from config.db import conexionDB
from schemas.memoriaRam_schema import memoriasRam
from models.memoriaRam_model import MemoriaRam
from starlette.status import HTTP_204_NO_CONTENT

memoriaRam = APIRouter()

@memoriaRam.post("/memoria", response_model=MemoriaRam, tags=["Memoria Ram"])
def add_memoriaRam(memoria: MemoriaRam):
    conexion = conexionDB()
    result = conexion.execute(memoriasRam.insert().values(memoria.dict()))
    conexion.close()
    if result:
        return memoria.dict()

@memoriaRam.get('/memoria/{idRegistro}', response_model=MemoriaRam, tags=['Memoria Ram'])
def get_memoriaRam(idRegistro: str):
    conexion = conexionDB()
    result = conexion.execute(memoriasRam.select().where(memoriasRam.c.idRegistro == idRegistro)).first()
    conexion.close()
    if result:
        return result

@memoriaRam.delete('/memoria/{idRegistro}', status_code=HTTP_204_NO_CONTENT,tags=['Memoria Ram'])
def delete_memoria(idRegistro: str):
     conexion = conexionDB()
     result = conexion.execute(memoriasRam.delete().where(memoriasRam.c.idRegistro == idRegistro))
     conexion.close()
     if result:
        return Response(status_code=HTTP_204_NO_CONTENT)

@memoriaRam.put('/memoria/{idRegistro}', response_model=MemoriaRam, tags=['Memoria Ram'])
def update_memoriaRam(ram_id: str,newMemoriaRam: MemoriaRam):
    conexion = conexionDB()
    result = conexion.execute(memoriasRam.update().values(
    idRegistro = ram_id,
    modelo = newMemoriaRam.modelo,
    marca = newMemoriaRam.marca,
    tipoMemoria = newMemoriaRam.tipoMemoria,
    cantidadMemoria = newMemoriaRam.cantidadMemoria,
    cantidadMemorias = newMemoriaRam.cantidadMemorias,
    velocidad = newMemoriaRam.velocidad,
    ecc = newMemoriaRam.ecc).where(memoriasRam.c.idRegistro == ram_id))
    conexion.close()
    if result:
        newMemoriaRam.idRegistro = ram_id
        return newMemoriaRam.dict()

    raise HTTPException(status_code=404, detail="Memoria Ram not found")