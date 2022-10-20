from pydantic import BaseModel

class Catalogo(BaseModel):
    idRegistro: str
    modelo: str