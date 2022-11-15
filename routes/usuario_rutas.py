from fastapi import APIRouter, Response, HTTPException
from config.db import conexionDB
from schemas.usuario_esquema import usuarios
from models.usuario_modelo import Usuario
from starlette.status import HTTP_204_NO_CONTENT
from security.encriptacion import cargar_llave, encriptar_mensaje, desencriptar_mensaje

usuario = APIRouter()

@usuario.get('/usuario/{nombreUsuario}', response_model=Usuario, tags=["Usuario"])
def get_usuario(nombreUsuario: str):
    llaveSeguridad = cargar_llave()
    conexion = conexionDB()
    resultado = conexion.execute(usuarios.select().where(usuarios.c.nombreUsuario == nombreUsuario)).first()
    conexion.close()
    if resultado:
        usuarioObtenido = dict(resultado)
        usuarioObtenido["contrasena"] = desencriptar_mensaje(usuarioObtenido['contrasena'], llaveSeguridad)
        return usuarioObtenido        

@usuario.post('/usuario', response_model=Usuario, tags=["Usuario"])
def add_usuario(usuario: Usuario):
    llaveSeguridad = cargar_llave()
    nuevo_usuario = usuario.dict()
    nuevo_usuario["contrasena"] = encriptar_mensaje(usuario.contrasena, llaveSeguridad)
    conexion = conexionDB()
    resultado = conexion.execute(usuarios.insert().values(nuevo_usuario))
    conexion.close()
    if resultado:
        return usuario.dict()

@usuario.delete('/usuario/{nombreUsuario}', status_code=HTTP_204_NO_CONTENT, tags=["Usuario"])
def delete_usuario(nombreUsuario: str):
    conexion = conexionDB()
    resultado = conexion.execute(usuarios.delete().where(usuarios.c.nombreUsuario == nombreUsuario))
    conexion.close()
    if resultado:
        return Response(status_code=HTTP_204_NO_CONTENT)

    raise HTTPException(status_code=404, detail="usuario no encontrado")

@usuario.put('/usuario/{nombreUsuario}', response_model=Usuario, tags=['Usuario'])
def update_usuario(nombreUsuarioAnterior: str, nuevo_usuario: Usuario):
    llaveSeguridad = cargar_llave()
    nuevaContrasena = encriptar_mensaje(nuevo_usuario.contrasena, llaveSeguridad)
    conexion = conexionDB()
    resultado = conexion.execute(usuarios.update().values(
        nombreUsuario = nuevo_usuario.nombreUsuario,
        nombre = nuevo_usuario.nombre,
        apellido = nuevo_usuario.apellido,
        correoElectronico = nuevo_usuario.correoElectronico,
        contrasena = nuevaContrasena,
        administrador = nuevo_usuario.administrador
    ).where(usuarios.c.nombreUsuario == nombreUsuarioAnterior))
    conexion.close()
    if resultado:
        return nuevo_usuario.dict()

    return HTTPException(status_code=404, detail='Usuario no encontrado')