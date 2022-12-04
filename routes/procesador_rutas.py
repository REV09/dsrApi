from fastapi import APIRouter, Response, HTTPException
from models.procesador_modelo import Procesador
from config.db import conexionDB
from schemas.procesador_esquema import procesadores
from starlette.status import HTTP_204_NO_CONTENT

procesador = APIRouter()


@procesador.get('/procesador/{id_registro}',
                response_model=Procesador, tags=['Procesador'])
def get_procesador(id_registro: str):

    '''
    Realiza la conexion con la base de datos para obtener los
    detalles del procesador de una laptop mediante el id
    de registro, recibe el id de registro para realizar su 
    tarea de busqueda y retorno de informacion

    En el caso de no encontrar lo solicitado retorna un codigo
    de error HTTP 404 que significa que no encontro el
    procesador solicitado
    '''

    conexion = conexionDB()
    resultado = conexion.execute(procesadores.select().where(
        procesadores.c.idRegistro == id_registro)).first()
    conexion.close()
    if resultado:
        return resultado

    raise HTTPException(status_code=404, detail='procesador no encontrado')


@procesador.post('/procesador', response_model=Procesador,
                 tags=['Procesador'])
def add_procesador(procesador: Procesador):

    '''
    Realiza la conexion con la base de datos para agregar los
    detalles del procesador de una laptop asociandolos 
    mediante el id de registro de la laptop ya existente, 
    recibe un objeto de tipo Procesador el cual contiene
    el id de registro con el que se asociara

    En el caso de no completar lo solicitado retorna un codigo
    de error HTTP 500 que significa que ocurrio un error en el
    servidor y no pudo completar la tarea

    En el caso contrario retornara un codigo HTTP 200 que
    significa tarea completada con extio y retornara los datos
    del procesador registrado en la base de datos
    '''

    conexion = conexionDB()
    resultado = conexion.execute(procesadores.insert().values(
        procesador.dict()))
    conexion.close()
    if resultado:
        return procesador.dict()
    
    raise HTTPException(status_code=500, detail='Error del servidor')


@procesador.delete('/procesador/{id_registro}',
                   status_code=HTTP_204_NO_CONTENT, tags=['Procesador'])
def delete_procesador(id_registro: str):

    '''
    Realiza la conexion con la base de datos con la peticion de
    eliminar de esta misma el procesador especificado mediante
    el id de registro

    Si el procesador es eliminado correctamente este metodo
    retornara un HTTP 204 especificando que la tarea se completo
    de manera exitosa y no hay contenido que mostrar

    En caso de no completarse con exito se retornara un HTTP 404
    especificando que no se encontro el procesador a eliminar
    '''

    conexion = conexionDB()
    resultado = conexion.execute(procesadores.delete().where(
        procesadores.c.idRegistro == id_registro))
    conexion.close()
    if resultado:
        return Response(status_code=HTTP_204_NO_CONTENT)

    raise HTTPException(status_code=404, detail='procesador no encontrado')


@procesador.put('/procesador/{id_registro}', response_model=Procesador,
                tags=['Procesador'])
def update_procesador(procesador_id: str, procesador_actualizado: Procesador):

    '''
    Realiza la actualizacion de datos del procesador especificado
    mediante el id de registro de la base de datos.
    Recibe primero el id de registro del procesador que a su vez
    es el id de registro de la laptop con la que guarda relacion
    seguido de eso recibe un objeto de tipo Procesador el cual es
    el procesador con los datos actualizados

    Si el procesador es actualizado correctamente este metodo
    retornara un HTTP 200 especificando que la tarea se completo
    de manera exitosa y retorna la nueva informacion del procesador

    En caso de no completarse con exito se retornara un HTTP 404
    especificando que no se encontro el procesador a actualizar
    '''

    conexion = conexionDB()
    resultado = conexion.execute(procesadores.update().values(
        idRegistro=procesador_id,
        modelo=procesador_actualizado.modelo,
        marca=procesador_actualizado.marca,
        numeroNucleos=procesador_actualizado.numeroNucleos,
        numeroHilos=procesador_actualizado.numeroHilos,
        velocidadMaxima=procesador_actualizado.velocidadMaxima,
        velocidadMinima=procesador_actualizado.velocidadMinima,
        litografia=procesador_actualizado.litografia
    ).where(procesadores.c.idRegistro == procesador_id))
    conexion.close()
    if resultado:
        procesador_actualizado.idRegistro = procesador_id
        return procesador_actualizado.dict()

    return HTTPException(status_code=404, detail='Procesador no encontrado')
