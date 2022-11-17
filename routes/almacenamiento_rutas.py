from fastapi import APIRouter, Response, HTTPException
from config.db import conexionDB
from schemas.almacenamiento_esquema import almacenamientos
from models.almacenamiento_modelo import Almacenamiento
from starlette.status import HTTP_204_NO_CONTENT

almacenamiento = APIRouter()


@almacenamiento.get('/almacenamiento/{id_registro}',
                    response_model=Almacenamiento,
                    tags=['Almacenamiento'])
def get_almacenamiento(id_registro: str):
    conexion = conexionDB()
    resultado = conexion.execute(almacenamientos.select().where(
        almacenamientos.c.idRegistro == id_registro)).first()
    conexion.close()
    if resultado:
        return resultado


@almacenamiento.post('/almacenamiento', response_model=Almacenamiento,
                     tags=['Almacenamiento'])
def add_almacenamiento(almacenamiento: Almacenamiento):
    conexion = conexionDB()
    resultado = conexion.execute(almacenamientos.insert().values(
        almacenamiento.dict()))
    conexion.close()
    if resultado:
        return almacenamiento.dict()


@almacenamiento.delete('/almacenamiento/{id_registro}',
                       status_code=HTTP_204_NO_CONTENT,
                       tags=['Almacenamiento'])
def delete_almacenamiento(id_registro: str):
    conexion = conexionDB()
    resultado = conexion.execute(almacenamientos.delete().where(
        almacenamientos.c.idRegistro == id_registro))
    conexion.close()
    if resultado:
        return Response(status_code=HTTP_204_NO_CONTENT)

    raise HTTPException(status_code=404,
                        detail='Almacenamiento no encontrado')


@almacenamiento.put('/almacenamiento/{id_registro}',
                    response_model=Almacenamiento,
                    tags=['Almacenamiento'])
def update_almacenamiento(almacenamiento_id: str,
                          almacenamiento_actualizado: Almacenamiento):
    conexion = conexionDB()
    resultado = conexion.execute(almacenamientos.update().values(
        idRegistro=almacenamiento_id,
        tipoAlmacenamiento=almacenamiento_actualizado.tipoAlmacenamiento
    ).where(almacenamientos.c.idRegistro == almacenamiento_id))
    conexion.close()
    if resultado:
        almacenamiento_actualizado.idRegistro = almacenamiento_id
        return almacenamiento_actualizado.dict()

    raise HTTPException(status_code=404,
                        detail='Almacenamiento no encontrado')
