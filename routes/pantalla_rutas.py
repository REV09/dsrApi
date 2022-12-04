from fastapi import APIRouter, HTTPException, Response
from config.db import conexionDB
from schemas.pantalla_esquema import pantallas
from models.pantalla_modelo import Pantalla
from starlette.status import HTTP_204_NO_CONTENT

pantalla = APIRouter()


@pantalla.post('/pantalla', response_model=Pantalla, tags=['Pantalla'])
def add_pantalla(pantalla: Pantalla):

    '''
    Realiza la conexion con la base de datos para agregar los
    detalles de la pantalla de una laptop asociandolos 
    mediante el id de registro de la laptop ya existente, 
    recibe un objeto de tipo Pantalla el cual contiene
    el id de registro con el que se asociara

    En el caso de no completar lo solicitado retorna un codigo
    de error HTTP 500 que significa que ocurrio un error en el
    servidor y no pudo completar la tarea

    En el caso contrario retornara un codigo HTTP 200 que
    significa tarea completada con extio y retornara los datos
    de la pantalla registrado en la base de datos
    '''

    conexion = conexionDB()
    resultado = conexion.execute(pantallas.insert().values(
        pantalla.dict()))
    conexion.close()
    if resultado:
        return pantalla.dict()
    
    raise HTTPException(status_code=500, detail='Error del servidor')


@pantalla.get('/pantalla/{id_registro}', response_model=Pantalla,
              tags=['Pantalla'])
def get_pantalla(id_registro: str):

    '''
    Realiza la conexion con la base de datos para obtener los
    detalles de la pantalla de una laptop mediante el id
    de registro, recibe el id de registro para realizar su 
    tarea de busqueda y retorno de informacion

    En el caso de no encontrar lo solicitado retorna un codigo
    de error HTTP 404 que significa que no encontro la
    pantalla solicitada
    '''

    conexion = conexionDB()
    resultado = conexion.execute(pantallas.select().where(
        pantallas.c.idRegistro == id_registro)).first()
    conexion.close()
    if resultado:
        return resultado

    raise HTTPException(status_code=404, detail='pantalla no encontrada')


@pantalla.delete('/pantalla/{id_registro}',
                 status_code=HTTP_204_NO_CONTENT,
                 tags=['Pantalla'])
def delete_pantalla(id_registro: str):

    '''
    Realiza la conexion con la base de datos con la peticion de
    eliminar de esta misma la pantalla especificada mediante
    el id de registro

    Si la pantalla es eliminado correctamente este metodo
    retornara un HTTP 204 especificando que la tarea se completo
    de manera exitosa y no hay contenido que mostrar

    En caso de no completarse con exito se retornara un HTTP 404
    especificando que no se encontro la pantalla a eliminar
    '''

    conexion = conexionDB()
    resultado = conexion.execute(pantallas.delete().where(
        pantallas.c.idRegistro == id_registro))
    conexion.close()
    if resultado:
        return Response(status_code=HTTP_204_NO_CONTENT)

    raise HTTPException(status_code=404, detail='pantalla no encontrada')


@pantalla.put('/pantalla/{id_registro}', response_model=Pantalla,
              tags=['Pantalla'])
def update_pantalla(pantalla_id: str, pantalla_actualizada: Pantalla):

    '''
    Realiza la actualizacion de datos de la pantalla especificado
    mediante el id de registro de la base de datos.
    Recibe primero el id de registro de la pantalla que a su vez
    es el id de registro de la laptop con la que guarda relacion
    seguido de eso recibe un objeto de tipo Pantalla el cual es
    la pantalla con los datos actualizados

    Si la pantalla es actualizada correctamente este metodo
    retornara un HTTP 200 especificando que la tarea se completo
    de manera exitosa y retorna la nueva informacion de la pantalla

    En caso de no completarse con exito se retornara un HTTP 404
    especificando que no se encontro la pantalla a actualizar
    '''

    conexion = conexionDB()
    resultado = conexion.execute(pantallas.update().values(
        idRegistro=pantalla_id,
        modelo=pantalla_actualizada.modelo,
        resolucion=pantalla_actualizada.resolucion,
        calidad=pantalla_actualizada.calidad,
        tipoPantalla=pantalla_actualizada.tipoPantalla,
        tamanio=pantalla_actualizada.tamanio,
        frecuenciaRefresco=pantalla_actualizada.frecuenciaRefresco
    ).where(pantallas.c.idRegistro == pantalla_id))
    conexion.close()
    if resultado:
        pantalla_actualizada.idRegistro = pantalla_id
        return pantalla_actualizada.dict()

    raise HTTPException(status_code=404, detail='pantalla no encontrada')
