import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.api.v1 import (
    producto_controller,
    categoria_controller,
    proveedor_controller,
    cliente_controller,
    inventario_controller,
    rol_controller,
    usuario_controller,
    auth_controller,
    compra_controller,
    venta_controller,
    ai_controller,
)

from app.core.config import settings

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    debug=settings.DEBUG
)

# CORS: permite que el frontend (React, en otro origen/puerto)
# pueda consumir esta API. En desarrollo se permite localhost;
# en producción esto se restringe a los dominios reales.
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:5173",  # Puerto por defecto de Vite
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    """
    Endpoint raíz, útil solo para verificar que el servidor
    está levantado y respondiendo.
    """
    return {
        "mensaje": "SmartStock API funcionando correctamente",
        "version": settings.APP_VERSION
    }


# Registro de controladores
app.include_router(auth_controller.router, prefix="/api/v1")
app.include_router(rol_controller.router, prefix="/api/v1")
app.include_router(usuario_controller.router, prefix="/api/v1")
app.include_router(producto_controller.router, prefix="/api/v1")
app.include_router(categoria_controller.router, prefix="/api/v1")
app.include_router(proveedor_controller.router, prefix="/api/v1")
app.include_router(cliente_controller.router, prefix="/api/v1")
app.include_router(inventario_controller.router, prefix="/api/v1")
app.include_router(compra_controller.router, prefix="/api/v1")
app.include_router(venta_controller.router, prefix="/api/v1")
app.include_router(ai_controller.router, prefix="/api/v1")

static_dir = os.path.join(os.path.dirname(__file__), "..", "static")
os.makedirs(os.path.join(static_dir, "graficas"), exist_ok=True)
app.mount("/static", StaticFiles(directory=static_dir), name="static")