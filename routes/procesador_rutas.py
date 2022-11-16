from fastapi import APIRouter, Response, HTTPException
from models.procesador_model import Procesador
from config.db import conexionDB
from schemas.procesador_schema import procesadores
from starlette.status import HTTP_204_NO_CONTENT

procesador = APIRouter()

@procesador.get('/procesador/{id_registro}', response_model=Procesador, tags=['Procesador'])
def get_procesador(id_registro: str):
    conexion = conexionDB()
    resultado = conexion.execute(procesadores.select().where(procesadores.c.idRegistro == id_registro)).first()
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

@procesador.delete('/procesador/{id_registro}', status_code=HTTP_204_NO_CONTENT, tags=['Procesador'])
def delete_procesador(id_registro: str):
    conexion = conexionDB()
    resultado = conexion.execute(procesadores.delete().where(procesadores.c.idRegistro == id_registro))
    conexion.close()
    if resultado:
        return Response(status_code=HTTP_204_NO_CONTENT)

    raise HTTPException(status_code= 404, detail='procesador no encontrado')

@procesador.put('/procesador/{id_registro}', response_model=Procesador, tags=['Procesador'])
def update_procesador(procesador_id: str, procesador_actualizado: Procesador):
    conexion = conexionDB()
    resultado = conexion.execute(procesadores.update().values(
        idRegistro = procesador_id,
        modelo = procesador_actualizado.modelo,
        marca = procesador_actualizado.marca,
        numeroNucleos = procesador_actualizado.numeroNucleos,
        numeroHilos = procesador_actualizado.numeroHilos,
        velocidadMaxima = procesador_actualizado.velocidadMaxima,
        velocidadMinima = procesador_actualizado.velocidadMinima,
        litografia = procesador_actualizado.litografia
    ).where(procesadores.c.idRegistro == procesador_id))
    conexion.close()
    if resultado:
        procesador_actualizado.idRegistro = procesador_id
        return procesador_actualizado.dict()

    return HTTPException(status_code=404, detail='Procesador no encontrado')