from sqlalchemy import Table, Column, MetaData
from sqlalchemy.sql.sqltypes import String
from config.db import motor

meta = MetaData()

almacenamientos = Table('almacenamiento', meta,
                Column('idRegistro', String(50), primary_key=True),
                Column('tipoAlmacenamiento', String(10))
                )

engine = motor()
meta.create_all(engine)