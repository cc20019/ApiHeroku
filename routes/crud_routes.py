from fastapi import APIRouter, HTTPException
from config.db import conn
from models.models import usuarios, bitacora, vehiculo, proyecto, gasolineras, rol, log
from schemas.schemas import Usuario, UsuarioResponse, Bitacora, BitacoraResponse, Vehiculo, VehiculoResponse, Proyecto, ProyectoResponse, Gasolinera, GasolineraResponse, Rol, RolResponse, Log, LogResponse
from cryptography.fernet import Fernet
from datetime import datetime
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy import select

user = APIRouter()              # Define el router de usuario
bitacora_router = APIRouter()   # Define el router de bitácora
vehiculo_router = APIRouter()   # Define el router de vehiculo
proyecto_router = APIRouter()   # Definie el router de proyecto
gasolineras_router = APIRouter()
rol_router = APIRouter()
log_router = APIRouter()

# Generar la clave de encriptación
key = Fernet.generate_key()
cipher = Fernet(key)

# Crear usuario
@user.post("/usuarios/", response_model=UsuarioResponse, tags=["Usuarios"])
def create_user(user: Usuario):
    encrypted_password = cipher.encrypt(user.password.encode())
    new_user = {
        "nombre": user.nombre,
        "apellido": user.apellido,
        "password": encrypted_password,
        "id_rol": user.id_rol,
        "activo": user.activo,
        "username": user.username,
    }
    result = conn.execute(usuarios.insert().values(new_user))
    conn.commit()
    created_user = conn.execute(usuarios.select().where(usuarios.c.id_usuario == result.lastrowid)).mappings().first()
    return UsuarioResponse(**created_user)

# Leer todos los usuarios
@user.get("/usuarios/", response_model=list[UsuarioResponse], tags=["Usuarios"])
def get_users():
    result = conn.execute(usuarios.select()).mappings().fetchall()
    return [UsuarioResponse(**row) for row in result]


# Leer usuario por ID
@user.get("/usuarios/{id}", response_model=UsuarioResponse, tags=["Usuarios"])
def get_user(id: int):
    result = conn.execute(usuarios.select().where(usuarios.c.id_usuario == id)).mappings().first()
    if not result:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return UsuarioResponse(**result)


# Clave para cifrar la contraseña (esto debe ser guardado de manera segura en producción)
key = b'your_key_here'  # Reemplaza con tu clave secreta para el cifrado
cipher = Fernet(key)

# Actualizar usuario
@user.put("/usuarios/{id}", response_model=UsuarioResponse, tags=["Usuarios"])
def update_user(id: int, user: Usuario):
    encrypted_password = cipher.encrypt(user.password.encode())  # Cifrado de la contraseña
    update_data = {
        "nombre": user.nombre,
        "apellido": user.apellido,
        "password": encrypted_password,
        "id_rol": user.id_rol,
        "activo": user.activo,
        "username": user.username,
    }
    result = conn.execute(usuarios.update().values(update_data).where(usuarios.c.id_usuario == id))
    conn.commit()
    if result.rowcount == 0:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    updated_user = conn.execute(usuarios.select().where(usuarios.c.id_usuario == id)).mappings().first()
    return UsuarioResponse(**updated_user)


# Eliminar usuario
@user.delete("/usuarios/{id}", status_code=204, tags=["Usuarios"])
def delete_user(id: int):
    try:
        result = conn.execute(usuarios.delete().where(usuarios.c.id_usuario == id))
        conn.commit()
        if result.rowcount == 0:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        return {"mensaje": "Usuario eliminado correctamente"}
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail="Error al eliminar el usuario")


#-----------------BITACORAS------------------------------------------ 

# Ruta para crear una nueva bitácora
@bitacora_router.post("/bitacoras/", response_model=BitacoraResponse, tags=["bitacoras"])
def create_bitacora(entry: Bitacora):
    new_entry = entry.dict()
    new_entry["created_at"] = new_entry.get("created_at") or datetime.utcnow()
    
    try:
        result = conn.execute(bitacora.insert().values(new_entry))
        conn.commit()
        
        created_bitacora = conn.execute(select(bitacora).where(bitacora.c.id_bitacora == result.lastrowid)).mappings().first()
        
        if created_bitacora:
            return BitacoraResponse(**created_bitacora)  # Se devuelve BitacoraResponse con el ID generado
    except IntegrityError as e:
        raise HTTPException(status_code=400, detail=f"Error de integridad: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error del servidor: {str(e)}")


# Ruta para obtener todas las bitácoras
@bitacora_router.get("/bitacoras/", response_model=list[BitacoraResponse], tags=["bitacoras"])
def get_all_bitacoras():
    try:
        result = conn.execute(bitacora.select()).mappings().fetchall()
        return [BitacoraResponse(**row) for row in result]  # Devuelve las bitácoras con su ID
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener las bitácoras: {str(e)}")

# Extraer bitácoras por id
@bitacora_router.get("/bitacoras/{id}", response_model=BitacoraResponse, tags=["bitacoras"])
def get_bitacora_by_id(id: int):
    try:
        # Realiza la consulta para obtener la bitácora por ID
        bitacora_data = conn.execute(select(bitacora).where(bitacora.c.id_bitacora == id)).mappings().first()
        
        # Si no se encuentra la bitácora, lanza un error 404
        if not bitacora_data:
            raise HTTPException(status_code=404, detail="Bitácora no encontrada")
        
        # Devuelve la bitácora como un objeto Pydantic con el ID
        return BitacoraResponse(**bitacora_data)
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener la bitácora: {str(e)}")

# Eliminar una bitácora
@bitacora_router.delete("/bitacoras/{id}", status_code=204, tags=["bitacoras"])
def delete_bitacora(id: int):
    try:
        # Ejecuta la eliminación de la bitácora con el ID especificado
        result = conn.execute(bitacora.delete().where(bitacora.c.id_bitacora == id))
        conn.commit()
        
        # Verifica si el registro existía y se eliminó
        if result.rowcount == 0:
            raise HTTPException(status_code=404, detail="Bitácora no encontrada")
        
        return {"mensaje": "Bitácora eliminada correctamente"}
    
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail="Error al eliminar la bitácora")



# Actualizar una bitácora
@bitacora_router.put("/bitacoras/{id}", response_model=BitacoraResponse, tags=["bitacoras"])
def update_bitacora(id: int, entry: Bitacora):
    # Convertir los datos de la bitácora en un diccionario
    update_data = entry.dict(exclude_unset=True)  # Excluir campos no establecidos
    
    # No enviamos 'updated_at' porque se actualizará automáticamente en el backend
    if "updated_at" in update_data:
        del update_data["updated_at"]
    
    # Establecemos la fecha de creación (created_at) con la fecha y hora actuales
    update_data["created_at"] = datetime.utcnow().isoformat()  # Actualizamos la fecha de creación (sin que el usuario lo envíe)

    try:
        # Ejecuta la actualización de la bitácora con el ID especificado
        result = conn.execute(bitacora.update().values(update_data).where(bitacora.c.id_bitacora == id))
        conn.commit()
        
        # Si no se encuentra la bitácora, lanza un error 404
        if result.rowcount == 0:
            raise HTTPException(status_code=404, detail="Bitácora no encontrada")
        
        # Recupera la bitácora actualizada con su ID
        updated_bitacora = conn.execute(select(bitacora).where(bitacora.c.id_bitacora == id)).mappings().first()
        if updated_bitacora:
            # Devuelve la bitácora actualizada como un objeto Pydantic con el ID
            return BitacoraResponse(**updated_bitacora)
    except IntegrityError as e:
        raise HTTPException(status_code=400, detail=f"Error de integridad: {str(e)}")
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Error al actualizar la bitácora: {str(e)}")




#---------------------VEHICULO-------------------------
# Crear un nuevo vehiculo
@vehiculo_router.post("/vehiculos/", response_model=VehiculoResponse, tags=["vehiculos"])
def create_vehiculo(entry: Vehiculo):
    new_entry = entry.dict()
    new_entry["created_at"] = new_entry.get("created_at") or datetime.utcnow()

    try:
        result = conn.execute(vehiculo.insert().values(new_entry))
        conn.commit()
        created_vehiculo = conn.execute(select(vehiculo).where(vehiculo.c.id_vehiculo == result.lastrowid)).mappings().first()
        if created_vehiculo:
            return VehiculoResponse(**created_vehiculo)
    except IntegrityError as e:
        raise HTTPException(status_code=400, detail=f"Error de integridad: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error del servidor: {str(e)}")


# Obtener todos los vehiculos
@vehiculo_router.get("/vehiculos/", response_model=list[VehiculoResponse], tags=["vehiculos"])
def get_all_vehiculos():
    try:
        result = conn.execute(vehiculo.select()).mappings().fetchall()
        return [VehiculoResponse(**row) for row in result]
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener los vehículos: {str(e)}")


# Obtener un vehiculo por ID
@vehiculo_router.get("/vehiculos/{id}", response_model=VehiculoResponse, tags=["vehiculos"])
def get_vehiculo(id: int):
    vehiculo_data = conn.execute(vehiculo.select().where(vehiculo.c.id_vehiculo == id)).first()
    if not vehiculo_data:
        raise HTTPException(status_code=404, detail="Vehículo no encontrado")
    return VehiculoResponse(**dict(vehiculo_data))


@vehiculo_router.put("/vehiculos/{id}", response_model=VehiculoResponse, tags=["vehiculos"])
def update_vehiculo(id: int, entry: Vehiculo):
    # Convertir los datos del vehiculo en un diccionario, excluyendo `created_at` ya que lo actualizaremos automáticamente
    update_data = entry.dict(exclude_unset=True)  # Excluir campos no establecidos

    # Si el campo `updated_at` está en los datos, lo eliminamos ya que no queremos que lo envíen
    if "updated_at" in update_data:
        del update_data["updated_at"]
    
    # Actualizamos `created_at` con la fecha y hora actual
    update_data["created_at"] = datetime.utcnow()  # Actualizamos la fecha de creación (sin que el usuario lo envíe)

    try:
        # Realizar la actualización del vehículo
        result = conn.execute(vehiculo.update().values(update_data).where(vehiculo.c.id_vehiculo == id))
        conn.commit()

        # Si no se actualizó ningún registro, arrojar un error
        if result.rowcount == 0:
            raise HTTPException(status_code=404, detail="Vehículo no encontrado")

        # Obtener el vehículo actualizado
        updated_vehiculo = conn.execute(select(vehiculo).where(vehiculo.c.id_vehiculo == id)).mappings().first()
        if updated_vehiculo:
            return VehiculoResponse(**updated_vehiculo)
    except IntegrityError as e:
        raise HTTPException(status_code=400, detail=f"Error de integridad: {str(e)}")
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Error al actualizar el vehículo: {str(e)}")


# Eliminar un vehiculo por ID
@vehiculo_router.delete("/vehiculos/{id}", status_code=204, tags=["vehiculos"])
def delete_vehiculo(id: int):
    result = conn.execute(vehiculo.delete().where(vehiculo.c.id_vehiculo == id))
    conn.commit()
    if result.rowcount == 0:
        raise HTTPException(status_code=404, detail="Vehículo no encontrado")
    return {"mensaje": "Vehículo eliminado correctamente"}


#----------------Proyectos----------------------

# Para extraer todos los proyectos
@proyecto_router.get("/proyectos/", response_model=list[ProyectoResponse], tags=["proyectos"])
def get_all_proyectos():
    try:
        result = conn.execute(proyecto.select()).mappings().fetchall()
        return [ProyectoResponse(**row) for row in result]
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener los proyectos: {str(e)}")


# Para crear un nuevo proyecto
@proyecto_router.post("/proyectos/", response_model=ProyectoResponse, tags=["proyectos"])
def create_proyecto(entry: Proyecto):
    new_entry = entry.dict()
    new_entry["created_at"] = new_entry.get("created_at") or datetime.utcnow()

    try:
        result = conn.execute(proyecto.insert().values(new_entry))
        conn.commit()
        created_proyecto = conn.execute(select(proyecto).where(proyecto.c.id_proyecto == result.lastrowid)).mappings().first()
        if created_proyecto:
            return ProyectoResponse(**created_proyecto)
    except IntegrityError as e:
        raise HTTPException(status_code=400, detail=f"Error de integridad: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error del servidor: {str(e)}")


# Extraer un proyecto por id
@proyecto_router.get("/proyectos/{id}", response_model=ProyectoResponse, tags=["proyectos"])
def get_proyecto_by_id(id: int):
    try:
        proyecto_data = conn.execute(select(proyecto).where(proyecto.c.id_proyecto == id)).mappings().first()
        if not proyecto_data:
            raise HTTPException(status_code=404, detail="Proyecto no encontrado")
        return ProyectoResponse(**proyecto_data)
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener el proyecto: {str(e)}")


@proyecto_router.put("/proyectos/{id}", response_model=ProyectoResponse, tags=["proyectos"])
def update_proyecto(id: int, entry: Proyecto):
    # Convertir el objeto de entrada en un diccionario
    update_data = entry.dict(exclude_unset=True)  # Excluir los campos no establecidos

    # Asegurarnos de que 'updated_at' no se incluya, ya que no existe en la base de datos
    if "updated_at" in update_data:
        del update_data["updated_at"]
    
    # Solo actualizar 'created_at' si es necesario (si la base de datos requiere que se pase)
    update_data["created_at"] = datetime.utcnow()  # Mantener el campo 'created_at' actualizado

    try:
        # Ejecutar la actualización en la base de datos
        result = conn.execute(proyecto.update().values(update_data).where(proyecto.c.id_proyecto == id))
        conn.commit()

        if result.rowcount == 0:
            raise HTTPException(status_code=404, detail="Proyecto no encontrado")

        # Obtener el proyecto actualizado
        updated_proyecto = conn.execute(select(proyecto).where(proyecto.c.id_proyecto == id)).mappings().first()
        if updated_proyecto:
            return ProyectoResponse(**updated_proyecto)
    except IntegrityError as e:
        raise HTTPException(status_code=400, detail=f"Error de integridad: {str(e)}")
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Error al actualizar el proyecto: {str(e)}")



# Eliminar un proyecto
@proyecto_router.delete("/proyectos/{id}", status_code=204, tags=["proyectos"])
def delete_proyecto(id: int):
    try:
        result = conn.execute(proyecto.delete().where(proyecto.c.id_proyecto == id))
        conn.commit()
        if result.rowcount == 0:
            raise HTTPException(status_code=404, detail="Proyecto no encontrado")
        return {"mensaje": "Proyecto eliminado correctamente"}
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Error al eliminar el proyecto: {str(e)}")


#----------------GASOLINERAS--------------------------

# Obtener todas las gasolineras
@gasolineras_router.get("/gasolineras/", response_model=list[GasolineraResponse], tags=["gasolineras"])
def get_all_gasolineras():
    try:
        result = conn.execute(gasolineras.select()).mappings().fetchall()
        return [GasolineraResponse(**row) for row in result]
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener las gasolineras: {str(e)}")

# Crear gasolinera
@gasolineras_router.post("/gasolineras/", response_model=GasolineraResponse, tags=["gasolineras"])
def create_gasolinera(entry: Gasolinera):
    new_entry = entry.dict()
    new_entry["created_at"] = new_entry.get("created_at") or datetime.utcnow()

    try:
        result = conn.execute(gasolineras.insert().values(new_entry))
        conn.commit()
        created_gasolinera = conn.execute(select(gasolineras).where(gasolineras.c.id_gasolinera == result.lastrowid)).mappings().first()
        if created_gasolinera:
            return GasolineraResponse(**created_gasolinera)
    except IntegrityError as e:
        raise HTTPException(status_code=400, detail=f"Error de integridad: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error del servidor: {str(e)}")

# Actualizar gasolinera
@gasolineras_router.put("/gasolineras/{id}", response_model=GasolineraResponse, tags=["gasolineras"])
def update_gasolinera(id: int, entry: Gasolinera):
    # Convertir los datos de la gasolinera en un diccionario, excluyendo `created_at` ya que lo actualizamos automáticamente
    update_data = entry.dict(exclude_unset=True)  # Excluir campos no establecidos

    # Si el campo `updated_at` está en los datos, lo eliminamos ya que no queremos que lo envíen
    if "updated_at" in update_data:
        del update_data["updated_at"]
    
    # Actualizamos `created_at` con la fecha y hora actual (sin que el usuario lo envíe)
    update_data["created_at"] = datetime.utcnow()  # Actualizamos la fecha de creación

    try:
        # Realizar la actualización de la gasolinera
        result = conn.execute(gasolineras.update().values(update_data).where(gasolineras.c.id_gasolinera == id))
        conn.commit()

        # Si no se actualizó ningún registro, arrojar un error
        if result.rowcount == 0:
            raise HTTPException(status_code=404, detail="Gasolinera no encontrada")

        # Obtener la gasolinera actualizada
        updated_gasolinera = conn.execute(select(gasolineras).where(gasolineras.c.id_gasolinera == id)).mappings().first()
        if updated_gasolinera:
            return GasolineraResponse(**updated_gasolinera)
    except IntegrityError as e:
        raise HTTPException(status_code=400, detail=f"Error de integridad: {str(e)}")
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Error al actualizar la gasolinera: {str(e)}")


# Obtener gasolinera por ID
@gasolineras_router.get("/gasolineras/{id}", response_model=GasolineraResponse, tags=["gasolineras"])
def get_gasolinera_by_id(id: int):
    try:
        gasolinera_data = conn.execute(select(gasolineras).where(gasolineras.c.id_gasolinera == id)).mappings().first()
        if not gasolinera_data:
            raise HTTPException(status_code=404, detail="Gasolinera no encontrada")
        return GasolineraResponse(**gasolinera_data)
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener la gasolinera: {str(e)}")

# Eliminar gasolinera
@gasolineras_router.delete("/gasolineras/{id}", status_code=204, tags=["gasolineras"])
def delete_gasolinera(id: int):
    try:
        result = conn.execute(gasolineras.delete().where(gasolineras.c.id_gasolinera == id))
        conn.commit()
        if result.rowcount == 0:
            raise HTTPException(status_code=404, detail="Gasolinera no encontrada")
        return {"mensaje": "Gasolinera eliminada correctamente"}
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Error al eliminar la gasolinera: {str(e)}")


#----------------ROLES------------------

# Obtener todos los roles
@rol_router.get("/roles/", response_model=list[RolResponse], tags=["roles"])
def get_all_roles():
    try:
        result = conn.execute(rol.select()).mappings().fetchall()
        return [RolResponse(**row) for row in result]
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener los roles: {str(e)}")

# Crear rol
@rol_router.post("/roles/", response_model=RolResponse, tags=["roles"])
def create_rol(entry: Rol):
    new_entry = entry.dict()

    try:
        result = conn.execute(rol.insert().values(new_entry))
        conn.commit()
        created_rol = conn.execute(select(rol).where(rol.c.id_rol == result.lastrowid)).mappings().first()
        if created_rol:
            return RolResponse(**created_rol)
    except IntegrityError as e:
        raise HTTPException(status_code=400, detail=f"Error de integridad: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error del servidor: {str(e)}")

# Actualizar rol
@rol_router.put("/roles/{id}", response_model=RolResponse, tags=["roles"])
def update_rol(id: int, entry: Rol):
    update_data = entry.dict()

    try:
        result = conn.execute(rol.update().values(update_data).where(rol.c.id_rol == id))
        conn.commit()
        if result.rowcount == 0:
            raise HTTPException(status_code=404, detail="Rol no encontrado")
        updated_rol = conn.execute(select(rol).where(rol.c.id_rol == id)).mappings().first()
        if updated_rol:
            return RolResponse(**updated_rol)
    except IntegrityError as e:
        raise HTTPException(status_code=400, detail=f"Error de integridad: {str(e)}")
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Error al actualizar el rol: {str(e)}")

# Obtener rol por id
@rol_router.get("/roles/{id}", response_model=RolResponse, tags=["roles"])
def get_rol_by_id(id: int):
    try:
        rol_data = conn.execute(select(rol).where(rol.c.id_rol == id)).mappings().first()
        if not rol_data:
            raise HTTPException(status_code=404, detail="Rol no encontrado")
        return RolResponse(**rol_data)
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener el rol: {str(e)}")

# Eliminar rol
@rol_router.delete("/roles/{id}", status_code=204, tags=["roles"])
def delete_rol(id: int):
    try:
        result = conn.execute(rol.delete().where(rol.c.id_rol == id))
        conn.commit()
        if result.rowcount == 0:
            raise HTTPException(status_code=404, detail="Rol no encontrado")
        return {"mensaje": "Rol eliminado correctamente"}
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Error al eliminar el rol: {str(e)}")


#-----------------LOGS--------------------------

# Obtener todos los logs
@log_router.get("/logs/", response_model=list[LogResponse], tags=["logs"])
def get_all_logs():
    try:
        result = conn.execute(log.select()).mappings().fetchall()
        return [LogResponse(**row) for row in result]
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener los logs: {str(e)}")

# Obtener un log por ID
@log_router.get("/logs/{id}", response_model=LogResponse, tags=["logs"])
def get_log_by_id(id: int):
    try:
        log_data = conn.execute(select(log).where(log.c.id_log == id)).mappings().first()
        if not log_data:
            raise HTTPException(status_code=404, detail="Log no encontrado")
        return LogResponse(**log_data)
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener el log: {str(e)}")
