from sqlalchemy import Table, Column, MetaData
from sqlalchemy.sql.sqltypes import Integer, String
from config.db import motor

meta = MetaData()

memoria_rams = Table("memoriaram", meta,
    Column("idRegistro", String(40), primary_key=True),
    Column("modelo", String(45)),
    Column("marca", String(20)),
    Column("tipoMemoria", String(10)),
    Column("cantidadMemoria", Integer),
    Column("cantidadMemorias", Integer),
    Column("velocidad", Integer),
    Column("ecc", Integer))

engine = motor()
meta.create_all(engine)
