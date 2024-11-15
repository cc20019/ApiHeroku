from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class Usuario(BaseModel):
    nombre: str
    apellido: str
    password: str
    id_rol: int
    activo: bool
    username: str

class UsuarioResponse(BaseModel):
    id_usuario: int
    nombre: str
    apellido: str
    username: str
    id_rol: int
    activo: bool

    class Config:
        orm_mode = True

# Esquema para la bitácora de entrada
class Bitacora(BaseModel):
    comentario: str
    km_inicial: float
    km_final: float
    num_galones: float
    costo: float
    tipo_gasolina: str
    id_usuario: int
    id_vehiculo: int
    id_gasolinera: int
    id_proyecto: int
    created_at: Optional[datetime] = None  # Opcional, se establecerá automáticamente
    
    class Config:
        orm_mode = True

class BitacoraResponse(BaseModel):
    id_bitacora: int
    comentario: str
    km_inicial: float
    km_final: float
    num_galones: float
    costo: float
    tipo_gasolina: str
    id_usuario: int
    id_vehiculo: int
    id_gasolinera: int
    id_proyecto: int
    created_at: Optional[datetime]

    class Config:
        orm_mode = True

class Vehiculo(BaseModel):
    modelo: str
    marca: str
    placa: str
    rendimineto: float  
    galonaje: float
    tipo_combustible: str
    created_at: Optional[datetime] = None

    class Config:
        orm_mode = True

class VehiculoResponse(BaseModel):
    id_vehiculo: int
    modelo: str
    marca: str
    placa: str
    rendimineto: float
    galonaje: float
    tipo_combustible: str
    created_at: Optional[datetime]

    class Config:
        orm_mode = True


class Proyecto(BaseModel):
    #id_proyecto: int
    created_at: Optional[datetime]
    nombre: str
    direccion: str
    activo: int

    class Config:
        orm_mode = True

class ProyectoResponse(BaseModel):
    id_proyecto: int
    created_at: Optional[datetime]
    nombre: str
    direccion: str
    activo: int

    class Config:
        orm_mode = True

class Gasolinera(BaseModel):
    #id_gasolinera: int
    created_at: Optional[datetime]
    nombre: str
    direccion: str

    class Config:
        orm_mode = True

class GasolineraResponse(BaseModel):
    id_gasolinera: int
    created_at: Optional[datetime]
    nombre: str
    direccion: str

    class Config:
        orm_mode = True

class Rol(BaseModel):
    #id_rol: int
    descripcion: str

    class Config:
        orm_mode = True

class RolResponse(BaseModel):
    id_rol: int
    descripcion: str

    class Config:
        orm_mode = True

class Log(BaseModel):
    #id_log: int
    created_at: Optional[datetime]
    descripcion: str
    id_user: int

    class Config:
        orm_mode = True

class LogResponse(BaseModel):
    id_log: int
    created_at: Optional[datetime]
    descripcion: str
    id_user: int

    class Config:
        orm_mode = True

