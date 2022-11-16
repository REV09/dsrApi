from fastapi import APIRouter, Response, HTTPException
from models.ssd_modelo import Ssd
from config.db import  conexionDB
from schemas.ssd_esquema import ssds
from starlette.status import HTTP_204_NO_CONTENT

ssd = APIRouter()

@ssd.get('/ssd/{id_registro}', response_model=Ssd, tags=['SSD'])
def get_ssd(id_registro: str):
    conexion = conexionDB()
    resultado = conexion.execute(ssds.select().where(ssds.c.idRegistro == id_registro)).first()
    conexion.close()
    if resultado:
        return resultado

@ssd.post('/ssd', response_model=Ssd, tags=['SSD'])
def add_ssd(ssd: Ssd):
    conexion = conexionDB()
    resultado = conexion.execute(ssds.insert().values(ssd.dict()))
    conexion.close()
    if resultado:
        return ssd.dict()

@ssd.delete('/ssd/{id_registro}', status_code=HTTP_204_NO_CONTENT, tags=['SSD'])
def delete_ssd(id_registro: str):
    conexion = conexionDB()
    resultado = conexion.execute(ssds.delete().where(ssds.c.idRegistro == id_registro))
    conexion.close()
    if resultado:
        return Response(status_code=HTTP_204_NO_CONTENT)

    raise HTTPException(status_code=404, detail='SSD no encontrado')

@ssd.put('/ssd/{id_registro}', response_model=Ssd, tags=['SSD'])
def update_ssd(ssd_id: str, ssd_actualizado: Ssd):
    conexion = conexionDB()
    resultado = conexion.execute(ssds.update().values(
        idRegistro = ssd_id,
        marca = ssd_actualizado.marca,
        modelo = ssd_actualizado.modelo,
        capacidad = ssd_actualizado.capacidad,
        factorForma = ssd_actualizado.factorForma,
        durabilidad = ssd_actualizado.durabilidad,
        tipoMemorias = ssd_actualizado.tipoMemorias,
        generacionMemorias = ssd_actualizado.generacionMemorias,
        velocidadLectura = ssd_actualizado.velocidadLectura,
        velocidadEscritura = ssd_actualizado.velocidadEscritura,
        protocolo = ssd_actualizado.protocolo
    ).where(ssds.c.idRegistro == ssd_id))
    conexion.close()
    if resultado:
        ssd_actualizado.idRegistro = ssd_id
        return ssd_actualizado.dict()

    return HTTPException(status_code=404, detail='SSD no encontrado')