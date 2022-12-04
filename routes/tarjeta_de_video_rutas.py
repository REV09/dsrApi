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

    '''
    Realiza la conexion con la base de datos para obtener los
    detalles de la tarjeta de video de una laptop mediante el id
    de registro, recibe el id de registro para realizar su 
    tarea de busqueda y retorno de informacion

    En el caso de no encontrar lo solicitado retorna un codigo
    de error HTTP 404 que significa que no encontro la
    tarjeta de video solicitada
    '''

    conexion = conexionDB()
    resultado = conexion.execute(tarjetas_video.select().where(
        tarjetas_video.c.idRegistro == id_registro)).first()
    conexion.close()
    if resultado:
        return resultado

    raise HTTPException(status_code=404,
                        detail='Tarjeta de video no encontrada')


@tarjeta_video.post('/tarjetaDeVideo/', response_model=TarjetaVideo,
                    tags=['Tarjeta de video'])
def add_tarjetaVideo(tarjeta_video: TarjetaVideo):

    '''
    Realiza la conexion con la base de datos para agregar los
    detalles de la tarjeta de video de una laptop asociandolos
    mediante el id de registro de la laptop ya existente, 
    recibe un objeto de tipo TarjetaVideo el cual contiene
    el id de registro con el que se asociara

    En el caso de no completar lo solicitado retorna un codigo
    de error HTTP 500 que significa que ocurrio un error en el
    servidor y no pudo completar la tarea

    En el caso contrario retornara un codigo HTTP 200 que
    significa tarea completada con extio y retornara los datos
    de la tarjeta de video registrado en la base de datos
    '''

    conexion = conexionDB()
    resultado = conexion.execute(tarjetas_video.insert().values(
        tarjeta_video.dict()))
    conexion.close()
    if resultado:
        return tarjeta_video.dict()

    raise HTTPException(status_code=500, detail='Error del servidor')


@tarjeta_video.delete('/tarjetaDeVideo/{id_registro}',
                      status_code=HTTP_204_NO_CONTENT,
                      tags=['Tarjeta de video'])
def delete_tarjetaVideo(id_registro: str):

    '''
    Realiza la conexion con la base de datos con la peticion de
    eliminar de esta misma la tarjeta de video especificada mediante
    el id de registro

    Si la tarjeta de video es eliminado correctamente este metodo
    retornara un HTTP 204 especificando que la tarea se completo
    de manera exitosa y no hay contenido que mostrar

    En caso de no completarse con exito se retornara un HTTP 404
    especificando que no se encontro la tarjeta de video a eliminar
    '''

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

    '''
    Realiza la actualizacion de datos de la tarjeta de video 
    especificada mediante el id de registro de la base de datos.
    Recibe primero el id de registro de la tarjeta de video que a su 
    vez es el id de registro de la laptop con la que guarda relacion
    seguido de eso recibe un objeto de tipo TarjetaVideo el cual es
    la tarjeta de video con los datos actualizados

    Si la tarjeta de video es actualizada correctamente este metodo
    retornara un HTTP 200 especificando que la tarea se completo
    de manera exitosa y retorna la nueva informacion de la 
    tarjeta de video

    En caso de no completarse con exito se retornara un HTTP 404
    especificando que no se encontro la tarjeta de video a actualizar
    '''

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

    raise HTTPException(status_code=404,
                         detail='Tarjeta de video no encontrado')
