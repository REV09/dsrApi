from fastapi import APIRouter, Response, HTTPException
from models.procesador_model import Procesador
from config.db import conexionDB
from schemas.procesador_schema import procesadores
from starlette.status import HTTP_204_NO_CONTENT

procesador = APIRouter()

@procesador.get('/procesador/{idRegistro}', response_model=Procesador, tags=['Procesador'])
def get_procesador(idRegistro: str):
    conexion = conexionDB()
    resultado = conexion.execute(procesadores.select().where(procesadores.c.idRegistro == idRegistro)).first()
    conexion.close()
    if resultado:
        return resultado

@procesador.post('/procesador', response_model=Procesador, tags=['Procesador'])
def add_procesador(procesador: Procesador):
    conexion = conexionDB()
    resultado = conexion.execute(procesadores.insert().values(procesador.dict()))
    conexion.close()
    if resultado: 
        return procesador.dict()

@procesador.delete('/procesador/{idRegistro}', status_code=HTTP_204_NO_CONTENT, tags=['Procesador'])
def delete_procesador(idRegistro: str):
    conexion = conexionDB()
    resultado = conexion.execute(procesadores.delete().where(procesadores.c.idRegistro == idRegistro))
    conexion.close()
    if resultado:
        return Response(status_code=HTTP_204_NO_CONTENT)

    raise HTTPException(status_code= 404, detail='procesador no encontrado')

@procesador.put('/procesador/{idRegistro}', response_model=Procesador, tags=['Procesador'])
def update_procesador(procesador_id: str, procesadorActualizado: Procesador):
    conexion = conexionDB()
    resultado = conexion.execute(procesadores.update().values(
        idRegistro = procesador_id,
        modelo = procesadorActualizado.modelo,
        marca = procesadorActualizado.marca,
        numeroNucleos = procesadorActualizado.numeroNucleos,
        numeroHilos = procesadorActualizado.numeroHilos,
        velocidadMaxima = procesadorActualizado.velocidadMaxima,
        velocidadMinima = procesadorActualizado.velocidadMinima,
        litografia = procesadorActualizado.litografia
    ).where(procesadores.c.idRegistro == procesador_id))
    conexion.close()
    if resultado:
        procesadorActualizado.idRegistro = procesador_id
        return procesadorActualizado.dict()

    return HTTPException(status_code=404, detail='Procesador no encontrado')