from pydantic import BaseModel


class Ssd(BaseModel):
    idRegistro: str
    marca: str
    modelo: str
    capacidad: int
    factorForma: str
    durabilidad: str
    tipoMemorias: str
    generacionMemorias: str
    velocidadLectura: str
    velocidadEscritura: str
    protocolo: str
