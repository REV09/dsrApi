from sqlalchemy import Table, Column, MetaData
from sqlalchemy.sql.sqltypes import String, FLOAT, Integer
from config.db import motor

meta = MetaData()

tarjetas_video = Table('tarjetavideo', meta,
                Column('idRegistro', String(50), primary_key=True),
                Column('modelo', String(45)),
                Column('marca', String(45)),
                Column('cantidadVram', Integer),
                Column('tipoMemoria', String(10)),
                Column('bits', Integer),
                Column('velocidadReloj', FLOAT),
                Column('tipo', String(10)),
                )

engine = motor()
meta.create_all(engine)