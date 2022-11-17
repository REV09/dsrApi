from pydantic import BaseModel


class Almacenamiento(BaseModel):
    idRegistro: str
    tipoAlmacenamiento: str
