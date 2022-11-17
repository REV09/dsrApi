from fastapi import APIRouter, Response, HTTPException
from models.hdd_modelo import Hdd
from config.db import conexionDB
from schemas.hdd_esquema import hdds
from starlette.status import HTTP_204_NO_CONTENT

hdd = APIRouter()


@hdd.get('/hdd/{id_registro}', response_model=Hdd, tags=['HDD'])
def get_hdd(id_registro: str):
    conexion = conexionDB()
    resultado = conexion.execute(hdds.select().where(
        hdds.c.idRegistro == id_registro)).first()
    conexion.close()
    if resultado:
        return resultado


@hdd.post('/hdd', response_model=Hdd, tags=['HDD'])
def add_hdd(hdd: Hdd):
    conexion = conexionDB()
    resultado = conexion.execute(hdds.insert().values(hdd.dict()))
    conexion.close()
    if resultado:
        return hdd.dict()


@hdd.delete('/hdd/{id_registro}', status_code=HTTP_204_NO_CONTENT,
            tags=['HDD'])
def delete_hdd(id_registro: str):
    conexion = conexionDB()
    resultado = conexion.execute(hdds.delete().where(
        hdds.c.idRegistro == id_registro))
    conexion.close()
    if resultado:
        return Response(status_code=HTTP_204_NO_CONTENT)

    raise HTTPException(status_code=404, detail='HDD no encontrado')


@hdd.put('/hdd/{id_registro}', response_model=Hdd, tags=['HDD'])
def update_hdd(hdd_id: str, hdd_actualizado: Hdd):
    conexion = conexionDB()
    resultado = conexion.execute(hdds.update().values(
        idRegistro=hdd_id,
        marca=hdd_actualizado.marca,
        modelo=hdd_actualizado.modelo,
        capacidad=hdd_actualizado.capacidad,
        interfaz=hdd_actualizado.interfaz,
        cache=hdd_actualizado.cache,
        revoluciones=hdd_actualizado.revoluciones,
        tamanio=hdd_actualizado.tamanio
    ).where(hdds.c.idRegistro == hdd_id))
    conexion.close()
    if resultado:
        hdd_actualizado.idRegistro = hdd_id
        return hdd_actualizado.dict()

    return HTTPException(status_code=404, detail='HDD no encontrado')
