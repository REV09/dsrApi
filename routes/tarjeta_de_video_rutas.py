from fastapi import APIRouter, Response, HTTPException
from models.tarjeta_de_video_modelo import TarjetaVideo
from config.db import conexionDB
from schemas.tarjeta_de_video_esquema import tarjetas_video
from starlette.status import HTTP_204_NO_CONTENT

tarjeta_video = APIRouter()


@tarjeta_video.get('/tarjetaDeVideo/{id_registro}',
                   response_model=TarjetaVideo,
                   tags=['Tarjeta de video'])
def get_tarjetaVideo(id_registro: str):
    conexion = conexionDB()
    resultado = conexion.execute(tarjetas_video.select().where(
        tarjetas_video.c.idRegistro == id_registro)).first()
    conexion.close()
    if resultado:
        return resultado


@tarjeta_video.post('/tarjetaDeVideo/', response_model=TarjetaVideo,
                    tags=['Tarjeta de video'])
def add_tarjetaVideo(tarjeta_Video: TarjetaVideo):
    conexion = conexionDB()
    resultado = conexion.execute(tarjetas_video.insert().values(
        tarjeta_Video.dict()))
    conexion.close()
    if resultado:
        return tarjeta_Video.dict()


@tarjeta_video.delete('/tarjetaDeVideo/{id_registro}',
                      status_code=HTTP_204_NO_CONTENT,
                      tags=['Tarjeta de video'])
def delete_tarjetaVideo(id_registro: str):
    conexion = conexionDB()
    resultado = conexion.execute(tarjetas_video.delete().where(
        tarjetas_video.c.idRegistro == id_registro))
    conexion.close()
    if resultado:
        return Response(status_code=HTTP_204_NO_CONTENT)

    raise HTTPException(status_code=404,
                        detail='Tarjetade video no encontrada')


@tarjeta_video.put('/tarjetaDeVideo/{id_registro}',
                   response_model=TarjetaVideo,
                   tags=['Tarjeta de video'])
def update_tarjetaVideo(tarjeta_id: str, tarjetaActualizada: TarjetaVideo):
    conexion = conexionDB()
    resultado = conexion.execute(tarjetas_video.update().values(
        idRegistro=tarjeta_id,
        modelo=tarjetaActualizada.modelo,
        marca=tarjetaActualizada.marca,
        cantidadVram=tarjetaActualizada.cantidadVram,
        tipoMemoria=tarjetaActualizada.tipoMemoria,
        bits=tarjetaActualizada.bits,
        velocidadReloj=tarjetaActualizada.velocidadReloj,
        tipo=tarjetaActualizada.tipo
    ).where(tarjetas_video.c.idRegistro == tarjeta_id))
    conexion.close()
    if resultado:
        tarjetaActualizada.idRegistro = tarjeta_id
        return tarjetaActualizada.dict()

    return HTTPException(status_code=404,
                         detail='Tarjeta de video no encontrado')
