from fastapi import APIRouter, Response, HTTPException
from config.db import conexionDB
from schemas.almacenamiento_esquema import almacenamientos
from models.almacenamiento_model import Almacenamiento
from starlette.status import HTTP_204_NO_CONTENT

almacenamiento = APIRouter()

#Test
@almacenamiento.get('/almacenamiento/{idRegistro}', response_model=Almacenamiento, tags=['Almacenamiento'])
def get_almacenamiento(idRegistro: str):
    conexion = conexionDB()
    resultado = conexion.execute(almacenamientos.select().where(almacenamientos.c.idRegistro == idRegistro)).first()
    conexion.close()
    if resultado:
        return resultado

#Test
@almacenamiento.post('/almacenamiento', response_model=Almacenamiento, tags=['Almacenamiento'])
def add_almacenamiento(almacenamiento: Almacenamiento):
    conexion = conexionDB()
    resultado = conexion.execute(almacenamientos.insert().values(almacenamiento.dict()))
    conexion.close()
    if resultado:
        return almacenamiento.dict()

#Test
@almacenamiento.delete('/almacenamiento/{idRegistro}', status_code=HTTP_204_NO_CONTENT, tags=['Almacenamiento'])
def delete_almacenamiento(idRegistro: str):
    conexion = conexionDB()
    resultado = conexion.execute(almacenamientos.delete().where(almacenamientos.c.idRegistro == idRegistro))
    conexion.close()
    if resultado:
        return Response(status_code=HTTP_204_NO_CONTENT)

    raise HTTPException(status_code=404, detail='Almacenamiento no encontrado')

#Test
@almacenamiento.put('/almacenamiento/{idRegistro}', response_model=Almacenamiento, tags=['Almacenamiento'])
def update_almacenamiento(almacenamiento_id: str, almacenamientoActualizado: Almacenamiento):
    conexion = conexionDB()
    resultado = conexion.execute(almacenamientos.update().values(
        idRegistro = almacenamiento_id,
        tipoAlmacenamiento = almacenamientoActualizado.tipoAlmacenamiento
    ).where(almacenamientos.c.idRegistro == almacenamiento_id))
    conexion.close()
    if resultado:
        almacenamientoActualizado.idRegistro = almacenamiento_id
        return almacenamientoActualizado.dict()

    raise HTTPException(status_code=404, detail='Almacenamiento no encontrado')