from sqlalchemy import Table, Column, MetaData
from sqlalchemy.sql.sqltypes import String, Integer
from config.db import motor

meta = MetaData()

usuarios = Table('usuario', meta,
                 Column('nombreUsuario', String(20), primary_key=True),
                 Column('nombre', String(100)),
                 Column('apellido', String(100)),
                 Column('correoElectronico', String(100)),
                 Column('contrasena', String(255)),
                 Column('administrador', Integer))

engine = motor()
meta.create_all(engine)
