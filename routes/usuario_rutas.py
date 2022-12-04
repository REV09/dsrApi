from fastapi import APIRouter, Response, HTTPException
from config.db import conexionDB
from schemas.usuario_esquema import usuarios
from models.usuario_modelo import Usuario
from starlette.status import HTTP_204_NO_CONTENT
from security.encriptacion import cargar_llave, encriptar_mensaje
from security.encriptacion import desencriptar_mensaje

usuario = APIRouter()


@usuario.get('/usuario/{nombre_usuario}', response_model=Usuario,
             tags=["Usuario"])
def get_usuario(nombre_usuario: str):

    '''
    Realiza la conexion con la base de datos para obtener los
    detalles del usuaro del sistema mediante el nombre de
    usuario, recibe el nombre de usuario para realizar su 
    tarea de busqueda y retorno de informacion

    En el caso de no encontrar lo solicitado retorna un codigo
    de error HTTP 404 que significa que no encontro el
    usuaro solicitado
    '''

    llave_seguridad = cargar_llave()
    conexion = conexionDB()
    resultado = conexion.execute(usuarios.select().where(
        usuarios.c.nombreUsuario == nombre_usuario)).first()
    conexion.close()
    if resultado:
        usuario_obtenido = dict(resultado)
        usuario_obtenido["contrasena"] = desencriptar_mensaje(
            usuario_obtenido['contrasena'], llave_seguridad)
        return usuario_obtenido

    raise HTTPException(status_code=404, detail='Usuario no encontrado')

@usuario.get('/usuario/correo/{correo_electronico}', response_model=Usuario,
             tags=["Usuario"])
def get_usuario_by_email(correo_electronico: str):

    '''
    Realiza la conexion con la base de datos para obtener los
    detalles del usuaro del sistema mediante el correo eletronico
    del usuario, recibe el correo electronico del usuario para 
    realizar su tarea de busqueda y retorno de informacion

    En el caso de no encontrar lo solicitado retorna un codigo
    de error HTTP 404 que significa que no encontro el
    usuaro solicitado
    '''

    llave_seguridad = cargar_llave()
    conexion = conexionDB()
    resultado = conexion.execute(usuarios.select().where(
        usuarios.c.correoElectronico == correo_electronico)).first()
    conexion.close()
    if resultado:
        usuario_obtenido = dict(resultado)
        usuario_obtenido["contrasena"] = desencriptar_mensaje(
            usuario_obtenido['contrasena'], llave_seguridad)
        return usuario_obtenido

    raise HTTPException(status_code=404, detail='Usuario no encontrado')

@usuario.post('/usuario', response_model=Usuario, tags=["Usuario"])
def add_usuario(usuario: Usuario):

    '''
    Realiza la conexion con la base de datos para agregar los
    detalles del usuario recibe un objeto de tipo Usuario
    

    En el caso de no completar lo solicitado retorna un codigo
    de error HTTP 500 que significa que ocurrio un error en el
    servidor y no pudo completar la tarea

    En el caso contrario retornara un codigo HTTP 200 que
    significa tarea completada con extio y retornara los datos
    del usuario registrado en la base de datos
    '''

    llave_seguridad = cargar_llave()
    nuevo_usuario = usuario.dict()
    nuevo_usuario["contrasena"] = encriptar_mensaje(
        usuario.contrasena, llave_seguridad)
    conexion = conexionDB()
    resultado = conexion.execute(usuarios.insert().values(nuevo_usuario))
    conexion.close()
    if resultado:
        return usuario.dict()
    
    raise HTTPException(status_code=500, detail='Error de servidor')


@usuario.delete('/usuario/{nombre_usuario}', status_code=HTTP_204_NO_CONTENT,
                tags=["Usuario"])
def delete_usuario(nombre_usuario: str):

    '''
    Realiza la conexion con la base de datos con la peticion de
    eliminar de esta misma el usuario especificado mediante
    el nombre de usuario

    Si el usuario es eliminado correctamente este metodo
    retornara un HTTP 204 especificando que la tarea se completo
    de manera exitosa y no hay contenido que mostrar

    En caso de no completarse con exito se retornara un HTTP 404
    especificando que no se encontro el usuario a eliminar
    '''

    conexion = conexionDB()
    resultado = conexion.execute(usuarios.delete().where(
        usuarios.c.nombreUsuario == nombre_usuario))
    conexion.close()
    if resultado:
        return Response(status_code=HTTP_204_NO_CONTENT)

    raise HTTPException(status_code=404, detail="usuario no encontrado")


@usuario.put('/usuario/{nombre_usuario}', response_model=Usuario,
             tags=['Usuario'])
def update_usuario(nombre_usuario_anterior: str, nuevo_usuario: Usuario):

    '''
    Realiza la actualizacion de datos del usuario especificado
    mediante el nombre de usuario de la base de datos.
    Recibe primero el nombre de usuario del usuario
    seguido de eso recibe un objeto de tipo Usuario el cual es
    el usuario con los datos actualizados

    Si el usuario es actualizado correctamente este metodo
    retornara un HTTP 200 especificando que la tarea se completo
    de manera exitosa y retorna la nueva informacion del usuario

    En caso de no completarse con exito se retornara un HTTP 404
    especificando que no se encontro el usuario a actualizar
    '''

    llave_seguridad = cargar_llave()
    nueva_contrasena = encriptar_mensaje(nuevo_usuario.contrasena,
                                         llave_seguridad)
    conexion = conexionDB()
    resultado = conexion.execute(usuarios.update().values(
        nombreUsuario=nuevo_usuario.nombreUsuario,
        nombre=nuevo_usuario.nombre,
        apellido=nuevo_usuario.apellido,
        correoElectronico=nuevo_usuario.correoElectronico,
        contrasena=nueva_contrasena,
        administrador=nuevo_usuario.administrador
    ).where(usuarios.c.nombreUsuario == nombre_usuario_anterior))
    conexion.close()
    if resultado:
        return nuevo_usuario.dict()

    raise HTTPException(status_code=404, detail='Usuario no encontrado')
