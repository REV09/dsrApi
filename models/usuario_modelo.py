from pydantic import BaseModel

class Usuario(BaseModel):
    nombreUsuario: str
    nombre: str
    apellido: str
    correoElectronico: str
    contrasena: str
    administrador: int