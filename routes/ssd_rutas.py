from fastapi import APIRouter, Response, HTTPException
from models.ssd_modelo import Ssd
from config.db import  conexionDB
from schemas.ssd_esquema import ssds
from starlette.status import HTTP_204_NO_CONTENT

ssd = APIRouter()

#Test
@ssd.get('/ssd/{idRegistro}', response_model=Ssd, tags=['SSD'])
def get_ssd(idRegistro: str):
    conexion = conexionDB()
    resultado = conexion.execute(ssds.select().where(ssds.c.idRegistro == idRegistro)).first()
    conexion.close()
    if resultado:
        return resultado

#Test
@ssd.post('/ssd', response_model=Ssd, tags=['SSD'])
def add_ssd(ssd: Ssd):
    conexion = conexionDB()
    resultado = conexion.execute(ssds.insert().values(ssd.dict()))
    conexion.close()
    if resultado:
        return ssd.dict()

#Test
@ssd.delete('/ssd/{idRegistro}', status_code=HTTP_204_NO_CONTENT, tags=['SSD'])
def delete_ssd(idRegistro: str):
    conexion = conexionDB()
    resultado = conexion.execute(ssds.delete().where(ssds.c.idRegistro == idRegistro))
    conexion.close()
    if resultado:
        return Response(status_code=HTTP_204_NO_CONTENT)

    raise HTTPException(status_code=404, detail='SSD no encontrado')

#Test
@ssd.put('/ssd/{idRegistro}', response_model=Ssd, tags=['SSD'])
def update_ssd(ssd_id: str, ssdActualizado: Ssd):
    conexion = conexionDB()
    resultado = conexion.execute(ssds.update().values(
        idRegistro = ssd_id,
        marca = ssdActualizado.marca,
        modelo = ssdActualizado.modelo,
        capacidad = ssdActualizado.capacidad,
        factorForma = ssdActualizado.factorForma,
        durabilidad = ssdActualizado.durabilidad,
        tipoMemorias = ssdActualizado.tipoMemorias,
        generacionMemorias = ssdActualizado.generacionMemorias,
        velocidadLectura = ssdActualizado.velocidadLectura,
        velocidadEscritura = ssdActualizado.velocidadEscritura,
        protocolo = ssdActualizado.protocolo
    ).where(ssds.c.idRegistro == ssd_id))
    conexion.close()
    if resultado:
        ssdActualizado.idRegistro = ssd_id
        return ssdActualizado.dict()

    return HTTPException(status_code=404, detail='SSD no encontrado')