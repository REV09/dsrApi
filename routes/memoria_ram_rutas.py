from fastapi import APIRouter, HTTPException, Response
from config.db import conexionDB
from schemas.memoria_ram_esquema import memoria_rams
from models.memoria_ram_modelo import MemoriaRam
from starlette.status import HTTP_204_NO_CONTENT

memoria_ram = APIRouter()


@memoria_ram.post("/memoria", response_model=MemoriaRam, tags=["Memoria Ram"])
def add_memoriaRam(memoria: MemoriaRam):

    '''
    Realiza la conexion con la base de datos para agregar los
    detalles de la memoria ram de una laptop asociandolos 
    mediante el id de registro de la laptop ya existente, 
    recibe un objeto de tipo Memoria Ram el cual contiene
    el id de registro con el que se asociara

    En el caso de no completar lo solicitado retorna un codigo
    de error HTTP 500 que significa que ocurrio un error en el
    servidor y no pudo completar la tarea

    En el caso contrario retornara un codigo HTTP 200 que
    significa tarea completada con extio y retornara los datos
    de la memoria ram registrado en la base de datos
    '''

    conexion = conexionDB()
    result = conexion.execute(memoria_rams.insert().values(memoria.dict()))
    conexion.close()
    if result:
        return memoria.dict()

    raise HTTPException(status_code=500, detail="Memoria ram no encontrada")


@memoria_ram.get('/memoria/{id_registro}', response_model=MemoriaRam,
                 tags=['Memoria Ram'])
def get_memoriaRam(id_registro: str):

    '''
    Realiza la conexion con la base de datos para obtener los
    detalles de la memoria ram de una laptop mediante el id
    de registro, recibe el id de registro para realizar su 
    tarea de busqueda y retorno de informacion

    En el caso de no encontrar lo solicitado retorna un codigo
    de error HTTP 404 que significa que no encontro la
    memoria ram solicitado
    '''

    conexion = conexionDB()
    result = conexion.execute(memoria_rams.select().where(
        memoria_rams.c.idRegistro == id_registro)).first()
    conexion.close()
    if result:
        return result

    raise HTTPException(status_code=404, detail="Memoria ram no encontrada")


@memoria_ram.delete('/memoria/{id_registro}', status_code=HTTP_204_NO_CONTENT,
                    tags=['Memoria Ram'])
def delete_memoria(id_registro: str):

    '''
    Realiza la conexion con la base de datos con la peticion de
    eliminar de esta misma la memoria ram especificada mediante
    el id de registro

    Si la memoria ram es eliminado correctamente este metodo
    retornara un HTTP 204 especificando que la tarea se completo
    de manera exitosa y no hay contenido que mostrar

    En caso de no completarse con exito se retornara un HTTP 404
    especificando que no se encontro la memoria ram a eliminar
    '''

    conexion = conexionDB()
    result = conexion.execute(memoria_rams.delete().where(
        memoria_rams.c.idRegistro == id_registro))
    conexion.close()
    if result:
        return Response(status_code=HTTP_204_NO_CONTENT)

    raise HTTPException(status_code=404, detail="Memoria ram no encontrada")


@memoria_ram.put('/memoria/{id_registro}', response_model=MemoriaRam,
                 tags=['Memoria Ram'])
def update_memoriaRam(ram_id: str, memoria_ram_actualizada: MemoriaRam):

    '''
    Realiza la actualizacion de datos de la memoria ram especificado
    mediante el id de registro de la base de datos.
    Recibe primero el id de registro de la memoria ram que a su vez
    es el id de registro de la laptop con la que guarda relacion
    seguido de eso recibe un objeto de tipo MemoriaRam el cual es
    la memoria ram con los datos actualizados

    Si la memoria ram es actualizado correctamente este metodo
    retornara un HTTP 200 especificando que la tarea se completo
    de manera exitosa y retorna la nueva informacion de la memoria ram

    En caso de no completarse con exito se retornara un HTTP 404
    especificando que no se encontro la memoria ram a actualizar
    '''

    conexion = conexionDB()
    result = conexion.execute(memoria_rams.update().values(
        idRegistro=ram_id,
        modelo=memoria_ram_actualizada.modelo,
        marca=memoria_ram_actualizada.marca,
        tipoMemoria=memoria_ram_actualizada.tipoMemoria,
        cantidadMemoria=memoria_ram_actualizada.cantidadMemoria,
        cantidadMemorias=memoria_ram_actualizada.cantidadMemorias,
        velocidad=memoria_ram_actualizada.velocidad,
        ecc=memoria_ram_actualizada.ecc).where(
        memoria_rams.c.idRegistro == ram_id))
    conexion.close()
    if result:
        memoria_ram_actualizada.idRegistro = ram_id
        return memoria_ram_actualizada.dict()

    raise HTTPException(status_code=404, detail="Memoria ram no encontrada")
