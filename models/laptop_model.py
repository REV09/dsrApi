from pydantic import BaseModel

class Laptop(BaseModel):
    idRegistro: str
    modelo: str
    memoriaRam: str
    tarjetaVideo: str
    pantalla: str
    almacenamiento: str
    procesador: str
