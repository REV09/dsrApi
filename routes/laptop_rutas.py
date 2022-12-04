from fastapi import APIRouter, HTTPException, Response
from config.db import conexionDB
from schemas.laptops_esquema import laptops
from models.laptop_modelo import Laptop
from uuid import uuid4 as uuid
from starlette.status import HTTP_204_NO_CONTENT

laptop = APIRouter()


@laptop.get('/laptops', response_model=list[Laptop], tags=["laptops"])
def get_laptops():

    '''
    Realiza la conexion con la base de datos para obtener los
    detalles de todas laptops

    En el caso de no encontrar ninguna laptop retorna un codigo
    de error HTTP 500 que significa que ha ocurrido un error en el
    servidor y no logro recuperar todas las laptops registradas
    '''

    conexion = conexionDB()
    conjunto_resultado = conexion.execute(laptops.select()).fetchall()
    conexion.close()
    if conjunto_resultado:
        return conjunto_resultado

    raise HTTPException(status_code=500, detail="Error del servidor")


@laptop.post('/laptop', response_model=Laptop, tags=["laptops"])
def add_laptop(laptop: Laptop):

    '''
    Realiza la conexion con la base de datos para agregar los
    detalles de una laptop, a su vez crea un identificador unico
    para cada registro que es el id de registro de la laptop, 
    recibe un objeto de tipo Laptop el cual contiene aun no posee el
    id de registro pues se le asiganra uno en este metodo con uuid

    En el caso de no completar lo solicitado retorna un codigo
    de error HTTP 500 que significa que ocurrio un error en el
    servidor y no pudo completar la tarea

    En el caso contrario retornara un codigo HTTP 200 que
    significa tarea completada con extio y retornara los datos
    de la Laptop registrada en la base de datos
    '''

    laptop.idRegistro = str(uuid())
    conexion = conexionDB()
    resultado = conexion.execute(laptops.insert().values(laptop.dict()))
    lap = conexion.execute(laptops.select().where(
        laptops.c.idRegistro == laptop.idRegistro)).first()
    conexion.close()
    if resultado:
        return lap
    
    raise HTTPException(status_code=500, detail="Error del servidor")



@laptop.get('/laptop/{laptop_id}', response_model=Laptop, tags=["laptops"])
def get_laptop(laptop_id: str):

    '''
    Realiza la conexion con la base de datos para obtener los
    detalles de una laptop mediante el id
    de registro, recibe el id de registro para realizar su 
    tarea de busqueda y retorno de informacion

    En el caso de no encontrar lo solicitado retorna un codigo
    de error HTTP 404 que significa que no encontro la
    laptop solicitada
    '''

    conexion = conexionDB()
    resultado = conexion.execute(laptops.select().where(
        laptops.c.idRegistro == laptop_id)).first()
    conexion.close()
    if resultado:
        return resultado

    raise HTTPException(status_code=404, detail="Laptop no encontrada")


@laptop.get('/laptopModelo/{modelo_laptop}', response_model=list[Laptop],
            tags=["laptops"])
def get_laptops_modelo(modelo_laptop: str):

    '''
    Realiza la conexion con la base de datos para obtener los
    detalles de un grupo de laptops mediante el modelo
    recibe el modelo de la laptop para realizar su 
    tarea de busqueda y retorno de informacion del grupo encontrado

    En el caso de no encontrar lo solicitado retorna un codigo
    de error HTTP 404 que significa que no encontro las
    laptops solicitadas
    '''

    conexion = conexionDB()
    conjunto_resultado = conexion.execute(laptops.select().where(
        laptops.c.modelo == modelo_laptop)).fetchall()
    conexion.close()
    print(conjunto_resultado)
    if conjunto_resultado:
        return conjunto_resultado

    raise HTTPException(status_code=404, detail="Laptop no encontrada")


@laptop.delete('/laptop/{laptop_id}', status_code=HTTP_204_NO_CONTENT,
               tags=["laptops"])
def delete_laptop(laptop_id: str):

    '''
    Realiza la conexion con la base de datos con la peticion de
    eliminar de esta misma la Laptop especificado mediante
    el id de registro

    Si la Laptop es eliminado correctamente este metodo
    retornara un HTTP 204 especificando que la tarea se completo
    de manera exitosa y no hay contenido que mostrar

    En caso de no completarse con exito se retornara un HTTP 404
    especificando que no se encontro la Laptop a eliminar
    '''

    conexion = conexionDB()
    resultado = conexion.execute(laptops.delete().where(
        laptops.c.idRegistro == laptop_id))
    conexion.close()
    if resultado:
        return Response(status_code=HTTP_204_NO_CONTENT)

    raise HTTPException(status_code=404, detail="Laptop no encontrada")


@laptop.put('/laptop/{laptop_id}', response_model=Laptop, tags=["laptops"])
def update_laptop(laptop_id: str, laptop_actualizada: Laptop):

    '''
    Realiza la actualizacion de datos de la Laptop especificada
    mediante el id de registro de la base de datos.
    Recibe primero el id de registro de la Laptop seguido
    de eso recibe un objeto de tipo Laptop el cual es
    la Laptop con los datos actualizados

    Si la Laptop es actualizado correctamente este metodo
    retornara un HTTP 200 especificando que la tarea se completo
    de manera exitosa y retorna la nueva informacion del Laptop

    En caso de no completarse con exito se retornara un HTTP 404
    especificando que no se encontro la Laptop a actualizar
    '''

    conexion = conexionDB()
    resultado = conexion.execute(laptops.update().values(
        idRegistro=laptop_id,
        modelo=laptop_actualizada.modelo,
        memoriaRam=laptop_actualizada.memoriaRam,
        tarjetaVideo=laptop_actualizada.tarjetaVideo,
        pantalla=laptop_actualizada.pantalla,
        almacenamiento=laptop_actualizada.almacenamiento,
        procesador=laptop_actualizada.procesador).where(
            laptops.c.idRegistro == laptop_id))
    conexion.close()
    if resultado:
        laptop_actualizada.idRegistro = laptop_id
        return laptop_actualizada.dict()

    raise HTTPException(status_code=404, detail="Laptop no encontrada")
