from fastapi import APIRouter, Response, HTTPException
from models.hdd_modelo import Hdd
from config.db import conexionDB
from schemas.hdd_esquema import hdds
from starlette.status import HTTP_204_NO_CONTENT

hdd = APIRouter()

@hdd.get('/hdd/{idRegistro}', response_model=Hdd, tags=['HDD'])
def get_hdd(idRegistro: str):
    conexion = conexionDB()
    resultado = conexion.execute(hdds.select().where(hdds.c.idRegistro == idRegistro)).first()
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

@hdd.delete('/hdd/{idRegistro}', status_code=HTTP_204_NO_CONTENT, tags=['HDD'])
def delete_hdd(idRegistro: str):
    conexion = conexionDB()
    resultado = conexion.execute(hdds.delete().where(hdds.c.idRegistro == idRegistro))
    conexion.close()
    if resultado:
        return Response(status_code=HTTP_204_NO_CONTENT)

    raise HTTPException(status_code=404, detail='HDD no encontrado')

@hdd.put('/hdd/{idRegistro}', response_model=Hdd, tags=['HDD'])
def update_hdd(hdd_id: str, hddActualizado: Hdd):
    conexion = conexionDB()
    resultado = conexion.execute(hdds.update().values(
        idRegistro = hdd_id,
        marca = hddActualizado.marca,
        modelo = hddActualizado.modelo,
        capacidad = hddActualizado.capacidad,
        interfaz = hddActualizado.interfaz,
        cache = hddActualizado.cache,
        revoluciones = hddActualizado.revoluciones,
        tamanio = hddActualizado.tamanio
    ).where(hdds.c.idRegistro == hdd_id))
    conexion.close()
    if resultado:
        hddActualizado.idRegistro = hdd_id
        return hddActualizado.dict()

    return HTTPException(status_code=404, detail='HDD no encontrado')