from fastapi import APIRouter, Response, HTTPException
from models.ssd_modelo import Ssd
from config.db import conexionDB
from schemas.ssd_esquema import ssds
from starlette.status import HTTP_204_NO_CONTENT

ssd = APIRouter()


@ssd.get('/ssd/{id_registro}', response_model=Ssd, tags=['SSD'])
def get_ssd(id_registro: str):

    '''
    Realiza la conexion con la base de datos para obtener los
    detalles del ssd de una laptop mediante el id
    de registro, recibe el id de registro para realizar su 
    tarea de busqueda y retorno de informacion

    En el caso de no encontrar lo solicitado retorna un codigo
    de error HTTP 404 que significa que no encontro el
    ssd solicitado
    '''

    conexion = conexionDB()
    resultado = conexion.execute(ssds.select().where(
        ssds.c.idRegistro == id_registro)).first()
    conexion.close()
    if resultado:
        return resultado

    raise HTTPException(status_code=404, detail='SSD no encontrado')


@ssd.post('/ssd', response_model=Ssd, tags=['SSD'])
def add_ssd(ssd: Ssd):

    '''
    Realiza la conexion con la base de datos para agregar los
    detalles del ssd de una laptop asociandolos 
    mediante el id de registro de la laptop ya existente, 
    recibe un objeto de tipo Ssd el cual contiene
    el id de registro con el que se asociara

    En el caso de no completar lo solicitado retorna un codigo
    de error HTTP 500 que significa que ocurrio un error en el
    servidor y no pudo completar la tarea

    En el caso contrario retornara un codigo HTTP 200 que
    significa tarea completada con extio y retornara los datos
    del ssd registrado en la base de datos
    '''

    conexion = conexionDB()
    resultado = conexion.execute(ssds.insert().values(ssd.dict()))
    conexion.close()
    if resultado:
        return ssd.dict()

    raise HTTPException(status_code=500, detail='Error del servidor')


@ssd.delete('/ssd/{id_registro}',
            status_code=HTTP_204_NO_CONTENT, tags=['SSD'])
def delete_ssd(id_registro: str):

    '''
    Realiza la conexion con la base de datos con la peticion de
    eliminar de esta misma el ssd especificado mediante
    el id de registro

    Si el ssd es eliminado correctamente este metodo
    retornara un HTTP 204 especificando que la tarea se completo
    de manera exitosa y no hay contenido que mostrar

    En caso de no completarse con exito se retornara un HTTP 404
    especificando que no se encontro el ssd a eliminar
    '''

    conexion = conexionDB()
    resultado = conexion.execute(ssds.delete().where(
        ssds.c.idRegistro == id_registro))
    conexion.close()
    if resultado:
        return Response(status_code=HTTP_204_NO_CONTENT)

    raise HTTPException(status_code=404, detail='SSD no encontrado')


@ssd.put('/ssd/{id_registro}', response_model=Ssd, tags=['SSD'])
def update_ssd(ssd_id: str, ssd_actualizado: Ssd):

    '''
    Realiza la actualizacion de datos del ssd especificado
    mediante el id de registro de la base de datos.
    Recibe primero el id de registro del ssd que a su vez
    es el id de registro de la laptop con la que guarda relacion
    seguido de eso recibe un objeto de tipo Ssd el cual es
    el ssd con los datos actualizados

    Si el ssd es actualizado correctamente este metodo
    retornara un HTTP 200 especificando que la tarea se completo
    de manera exitosa y retorna la nueva informacion del ssd

    En caso de no completarse con exito se retornara un HTTP 404
    especificando que no se encontro el ssd a actualizar
    '''

    conexion = conexionDB()
    resultado = conexion.execute(ssds.update().values(
        idRegistro=ssd_id,
        marca=ssd_actualizado.marca,
        modelo=ssd_actualizado.modelo,
        capacidad=ssd_actualizado.capacidad,
        factorForma=ssd_actualizado.factorForma,
        durabilidad=ssd_actualizado.durabilidad,
        tipoMemorias=ssd_actualizado.tipoMemorias,
        generacionMemorias=ssd_actualizado.generacionMemorias,
        velocidadLectura=ssd_actualizado.velocidadLectura,
        velocidadEscritura=ssd_actualizado.velocidadEscritura,
        protocolo=ssd_actualizado.protocolo
    ).where(ssds.c.idRegistro == ssd_id))
    conexion.close()
    if resultado:
        ssd_actualizado.idRegistro = ssd_id
        return ssd_actualizado.dict()

    raise HTTPException(status_code=404, detail='SSD no encontrado')
