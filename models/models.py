from sqlalchemy import Table, Column, Integer, String, Float, Text, Boolean, ForeignKey, TIMESTAMP
from config.db import meta, engine

# Definir primero las tablas que no tienen dependencias de claves foráneas
rol = Table("rol", meta,
    Column("id_rol", Integer, primary_key=True, autoincrement=True),
    Column("descripcion", Text)
)

# Luego define las otras tablas que dependen de la tabla 'rol'
usuarios = Table("usuarios", meta,
    Column("id_usuario", Integer, primary_key=True, autoincrement=True),
    Column("created_at", TIMESTAMP),
    Column("nombre", Text),
    Column("apellido", Text),
    Column("password", String(255)),
    Column("id_rol", Integer, ForeignKey("rol.id_rol")),  # clave foránea a la tabla 'rol'
    Column("activo", Boolean),
    Column("username", Text),
    Column("last_login", TIMESTAMP)
)

# Luego definimos las otras tablas, sin dependencias de claves foráneas entre ellas
log = Table("log", meta,
    Column("id_log", Integer, primary_key=True, autoincrement=True),
    Column("created_at", TIMESTAMP),
    Column("descripcion", Text),
    Column("id_user", Integer, ForeignKey("usuarios.id_usuario"))
)

bitacora = Table("bitacora", meta,
    Column("id_bitacora", Integer, primary_key=True, autoincrement=True),
    Column("created_at", TIMESTAMP),
    Column("comentario", Text),
    Column("km_inicial", Float),
    Column("km_final", Float),
    Column("num_galones", Float),
    Column("costo", Float),
    Column("tipo_gasolina", Text),
    Column("id_usuario", Integer, ForeignKey("usuarios.id_usuario")),
    Column("id_vehiculo", Integer, ForeignKey("vehiculo.id_vehiculo")),
    Column("id_gasolinera", Integer, ForeignKey("gasolineras.id_gasolinera")),
    Column("id_proyecto", Integer, ForeignKey("proyecto.id_proyecto")),
)

vehiculo = Table("vehiculo", meta,
    Column("id_vehiculo", Integer, primary_key=True, autoincrement=True),
    Column("created_at", TIMESTAMP),
    Column("modelo", Text),
    Column("marca", Text),
    Column("placa", Text),
    Column("rendimineto", Float), 
    Column("galonaje", Float),
    Column("tipo_combustible", Text),
)

proyecto = Table("proyecto", meta,
    Column("id_proyecto", Integer, primary_key=True, autoincrement=True),
    Column("created_at", TIMESTAMP),
    Column("nombre", Text),
    Column("direccion", Text),
    Column("activo", Boolean)
)

gasolineras = Table("gasolineras", meta,
    Column("id_gasolinera", Integer, primary_key=True, autoincrement=True),
    Column("created_at", TIMESTAMP),
    Column("nombre", Text),
    Column("direccion", Text)
)

meta.create_all(engine)  # Crear todas las tablas en orden
