from fastapi import APIRouter, Response, HTTPException
from models.hdd_modelo import Hdd
from config.db import conexionDB
from schemas.hdd_esquema import hdds
from starlette.status import HTTP_204_NO_CONTENT

hdd = APIRouter()


@hdd.get('/hdd/{id_registro}', response_model=Hdd, tags=['HDD'])
def get_hdd(id_registro: str):

    '''
    Realiza la conexion con la base de datos para obtener los
    detalles del disco duro de una laptop mediante el id
    de registro, recibe el id de registro para realizar su 
    tarea de busqueda y retorno de informacion

    En el caso de no encontrar lo solicitado retorna un codigo
    de error HTTP 404 que significa que no encontro el
    disco duro solicitado
    '''

    conexion = conexionDB()
    resultado = conexion.execute(hdds.select().where(
        hdds.c.idRegistro == id_registro)).first()
    conexion.close()
    if resultado:
        return resultado

    raise HTTPException(status_code=404, detail='HDD no encontrado')


@hdd.post('/hdd', response_model=Hdd, tags=['HDD'])
def add_hdd(hdd: Hdd):

    '''
    Realiza la conexion con la base de datos para agregar los
    detalles del disco duro de una laptop asociandolos 
    mediante el id de registro de la laptop ya existente, 
    recibe un objeto de tipo Almacenamiento el cual contiene
    el id de registro con el que se asociara

    En el caso de no completar lo solicitado retorna un codigo
    de error HTTP 500 que significa que ocurrio un error en el
    servidor y no pudo completar la tarea

    En el caso contrario retornara un codigo HTTP 200 que
    significa tarea completada con extio y retornara los datos
    del disco duro registrado en la base de datos
    '''

    conexion = conexionDB()
    resultado = conexion.execute(hdds.insert().values(hdd.dict()))
    conexion.close()
    if resultado:
        return hdd.dict()

    raise HTTPException(status_code=500, detail='Error del servidor')


@hdd.delete('/hdd/{id_registro}', status_code=HTTP_204_NO_CONTENT,
            tags=['HDD'])
def delete_hdd(id_registro: str):

    '''
    Realiza la conexion con la base de datos con la peticion de
    eliminar de esta misma el disco duro especificado mediante
    el id de registro

    Si el disco duro es eliminado correctamente este metodo
    retornara un HTTP 204 especificando que la tarea se completo
    de manera exitosa y no hay contenido que mostrar

    En caso de no completarse con exito se retornara un HTTP 404
    especificando que no se encontro el disco duro a eliminar
    '''

    conexion = conexionDB()
    resultado = conexion.execute(hdds.delete().where(
        hdds.c.idRegistro == id_registro))
    conexion.close()
    if resultado:
        return Response(status_code=HTTP_204_NO_CONTENT)

    raise HTTPException(status_code=404, detail='HDD no encontrado')


@hdd.put('/hdd/{id_registro}', response_model=Hdd, tags=['HDD'])
def update_hdd(hdd_id: str, hdd_actualizado: Hdd):

    '''
    Realiza la actualizacion de datos del disco duro especificado
    mediante el id de registro de la base de datos.
    Recibe primero el id de registro del disco duro que a su vez
    es el id de registro de la laptop con la que guarda relacion
    seguido de eso recibe un objeto de tipo disco duro el cual es
    el disco duro con los datos actualizados

    Si el disco duro es actualizado correctamente este metodo
    retornara un HTTP 200 especificando que la tarea se completo
    de manera exitosa y retorna la nueva informacion del disco duro

    En caso de no completarse con exito se retornara un HTTP 404
    especificando que no se encontro el disco duro a actualizar
    '''

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

    raise HTTPException(status_code=404, detail='HDD no encontrado')
