from sqlalchemy import Table, Column, MetaData
from sqlalchemy.sql.sqltypes import String

from config.db import motor

meta = MetaData()

Laptops = Table("laptop", meta, 
        Column("idRegistro", String(50), primary_key=True),
        Column("modelo", String(45)),
        Column("memoriaRam", String(30)),
        Column("tarjetaVideo", String(45)),
        Column("pantalla", String(45)),
        Column("almacenamiento", String(45)),
        Column("procesador", String(45),))

engine = motor()

meta.create_all(engine)