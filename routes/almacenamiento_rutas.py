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

    '''
    Realiza la conexion con la base de datos para obtener los
    detalles del almacenamiento de una laptop mediante el id
    de registro, recibe el id de registro para realizar su 
    tarea de busqueda y retorno de informacion

    En el caso de no encontrar lo solicitado retorna un codigo
    de error HTTP 404 que significa que no encontro el
    almacenamiento solicitado
    '''

    conexion = conexionDB()
    resultado = conexion.execute(almacenamientos.select().where(
        almacenamientos.c.idRegistro == id_registro)).first()
    conexion.close()
    if resultado:
        return resultado

    raise HTTPException(status_code=404,
                        detail='Almacenamiento no encontrado')


@almacenamiento.post('/almacenamiento', response_model=Almacenamiento,
                     tags=['Almacenamiento'])
def add_almacenamiento(almacenamiento: Almacenamiento):

    '''
    Realiza la conexion con la base de datos para agregar los
    detalles del almacenamiento de una laptop asociandolos 
    mediante el id de registro de la laptop ya existente, 
    recibe un objeto de tipo Almacenamiento el cual contiene
    el id de registro con el que se asociara

    En el caso de no completar lo solicitado retorna un codigo
    de error HTTP 500 que significa que ocurrio un error en el
    servidor y no pudo completar la tarea

    En el caso contrario retornara un codigo HTTP 200 que
    significa tarea completada con extio y retornara los datos
    del almacenamiento registrado en la base de datos
    '''

    conexion = conexionDB()
    resultado = conexion.execute(almacenamientos.insert().values(
        almacenamiento.dict()))
    conexion.close()
    if resultado:
        return almacenamiento.dict()
    
    raise HTTPException(status_code=500,
                        detail='Error del servidor')


@almacenamiento.delete('/almacenamiento/{id_registro}',
                       status_code=HTTP_204_NO_CONTENT,
                       tags=['Almacenamiento'])
def delete_almacenamiento(id_registro: str):

    '''
    Realiza la conexion con la base de datos con la peticion de
    eliminar de esta misma el almacenamiento especificado mediante
    el id de registro

    Si el almacenamiento es eliminado correctamente este metodo
    retornara un HTTP 204 especificando que la tarea se completo
    de manera exitosa y no hay contenido que mostrar

    En caso de no completarse con exito se retornara un HTTP 404
    especificando que no se encontro el almacenamiento a eliminar
    '''

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

    '''
    Realiza la actualizacion de datos del almacenamiento especificado
    mediante el id de registro de la base de datos.
    Recibe primero el id de registro del almacenamiento que a su vez
    es el id de registro de la laptop con la que guarda relacion
    seguido de eso recibe un objeto de tipo Almacenamiento el cual es
    el almacenamiento con los datos actualizados

    Si el almacenamiento es actualizado correctamente este metodo
    retornara un HTTP 200 especificando que la tarea se completo
    de manera exitosa y retorna la nueva informacion del almacenamiento

    En caso de no completarse con exito se retornara un HTTP 404
    especificando que no se encontro el almacenamiento a actualizar
    '''

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
