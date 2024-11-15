from fastapi import FastAPI
from routes.crud_routes import user, bitacora_router, vehiculo_router, proyecto_router, gasolineras_router, rol_router, log_router  # Importa ambos routers correctamente

app = FastAPI()

# Registrar las rutas de usuario y bitácora
app.include_router(user)
app.include_router(bitacora_router)
app.include_router(vehiculo_router)
app.include_router(proyecto_router)
app.include_router(gasolineras_router)
app.include_router(rol_router)
app.include_router(log_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
