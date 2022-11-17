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


@usuario.post('/usuario', response_model=Usuario, tags=["Usuario"])
def add_usuario(usuario: Usuario):
    llave_seguridad = cargar_llave()
    nuevo_usuario = usuario.dict()
    nuevo_usuario["contrasena"] = encriptar_mensaje(
        usuario.contrasena, llave_seguridad)
    conexion = conexionDB()
    resultado = conexion.execute(usuarios.insert().values(nuevo_usuario))
    conexion.close()
    if resultado:
        return usuario.dict()


@usuario.delete('/usuario/{nombre_usuario}', status_code=HTTP_204_NO_CONTENT,
    tags=["Usuario"])
def delete_usuario(nombre_usuario: str):
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

    return HTTPException(status_code=404, detail='Usuario no encontrado')
