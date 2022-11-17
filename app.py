from fastapi import FastAPI
from routes.laptop_rutas import laptop
from routes.memoria_ram_rutas import memoria_ram
from routes.catalogo_rutas import catalogo
from routes.procesador_rutas import procesador
from routes.tarjeta_de_video_rutas import tarjeta_video
from routes.pantalla_rutas import pantalla
from routes.almacenamiento_rutas import almacenamiento
from routes.hdd_rutas import hdd
from routes.ssd_rutas import ssd
from routes.usuario_rutas import usuario

app = FastAPI(
    title='Laptop API DSR',
    description='Api de obtencion de informacion de hardware de laptops',
    openapi_tags=[{
        'name': 'laptops',
        'description': 'laptops routes CRUD'
    },
    {
        'name': 'Memoria Ram',
        'description': 'Memorias Ram routes CRUD'
    },
    {
        'name': 'Catalogo',
        'description': 'Catalogo routes CRUD'
    },
    {
        'name': 'Procesador',
        'description': 'Procesador routes CRUD'
    },
    {
        'name': 'Tarjeta de video',
        'description': 'Tarjeta de video routes CRUD'
    },
    {
        'name': 'Pantalla',
        'description': 'Pantalla routes CRUD'
    },
    {
        'name': 'Almacenamiento',
        'description': 'Almacenamiento routes CRUD'
    },
    {
        'name': 'HDD',
        'description': 'HDD routes CRUD'
    },
    {
        'name': 'SSD',
        'description': 'SSD routes CRUD'
    },
    {
        'name': 'Usuario',
        'description': 'Usuario routes CRUD'
    }
    ]
)

app.include_router(laptop)
app.include_router(memoria_ram)
app.include_router(catalogo)
app.include_router(procesador)
app.include_router(tarjeta_video)
app.include_router(pantalla)
app.include_router(almacenamiento)
app.include_router(hdd)
app.include_router(ssd)
app.include_router(usuario)
