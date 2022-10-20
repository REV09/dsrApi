from pydantic import BaseModel

class MemoriaRam(BaseModel):
    idRegistro : str
    modelo: str
    marca: str
    tipoMemoria: str
    cantidadMemoria: int
    cantidadMemorias: int
    velocidad: int
    ecc: int