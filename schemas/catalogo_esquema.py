from sqlalchemy import Table, Column, MetaData
from sqlalchemy.sql.sqltypes import String
from config.db import motor

meta = MetaData()

catalogos = Table("catalogo", meta,
    Column("idRegistro", String(50), primary_key=True),
    Column("modelo", String(45)))

engine = motor()
meta.create_all(engine)
