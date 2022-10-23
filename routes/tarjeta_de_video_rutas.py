from fastapi import APIRouter, Response, HTTPException
from models.tarjeta_de_video_modelo import TarjetaVideo
from config.db import conexionDB
from schemas.tarjeta_de_video_esquema import tarjetasVideo
from starlette.status import HTTP_204_NO_CONTENT

tarjetaVideo = APIRouter()

@tarjetaVideo.get('/tarjetaDeVideo/{idRegistro}', response_model=TarjetaVideo, tags=['Tarjeta de video'])
def get_tarjetaVideo(idRegistro: str):
    conexion = conexionDB()
    resultado = conexion.execute(tarjetasVideo.select().where(tarjetasVideo.c.idRegistro == idRegistro)).first()
    conexion.close()
    if resultado:
        return resultado

@tarjetaVideo.post('/tarjetaDeVideo/', response_model=TarjetaVideo, tags=['Tarjeta de video'])
def add_tarjetaVideo(tarjetaVideo: TarjetaVideo):
    conexion = conexionDB()
    resultado = conexion.execute(tarjetasVideo.insert().values(tarjetaVideo.dict()))
    conexion.close()
    if resultado:
        return tarjetaVideo.dict()

@tarjetaVideo.delete('/tarjetaDeVideo/{idRegistro}', status_code=HTTP_204_NO_CONTENT, tags=['Tarjeta de video'])
def delete_tarjetaVideo(idRegistro: str):
    conexion = conexionDB()
    resultado = conexion.execute(tarjetasVideo.delete().where(tarjetasVideo.c.idRegistro == idRegistro))
    conexion.close()
    if resultado:
        return Response(status_code=HTTP_204_NO_CONTENT)

    raise HTTPException(status_code=404, detail='Tarjeta de video no encontrada')

@tarjetaVideo.put('/tarjetaDeVideo/{idRegistro}', response_model=TarjetaVideo, tags=['Tarjeta de video'])
def update_tarjetaVideo(tarjeta_id: str, tarjetaActualizada: TarjetaVideo):
    conexion = conexionDB()
    resultado = conexion.execute(tarjetasVideo.update().values(
        idRegistro = tarjeta_id,
        modelo = tarjetaActualizada.modelo,
        marca = tarjetaActualizada.marca,
        cantidadVram = tarjetaActualizada.cantidadVram,
        tipoMemoria = tarjetaActualizada.tipoMemoria,
        bits = tarjetaActualizada.bits,
        velocidadReloj = tarjetaActualizada.velocidadReloj,
        tipo = tarjetaActualizada.tipo
    ).where(tarjetasVideo.c.idRegistro == tarjeta_id))
    conexion.close()
    if resultado:
        tarjetaActualizada.idRegistro = tarjeta_id
        return tarjetaActualizada.dict()

    return HTTPException(status_code=404, detail='Tarjeta de video no encontrado')