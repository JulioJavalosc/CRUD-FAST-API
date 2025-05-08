from datetime import datetime
from database import SessionLocal, engine
from fastapi import FastAPI, HTTPException, Request, Depends, requests
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, HTMLResponse, JSONResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware
import logging
import requests
from operations.movimientos_stock_operations import get_movimientos_stock
from routers.productos_fijos_router import router as productos_fijos_router
from routers.tipo_usuarios_router import router as tipo_usuarios_router
from routers.usuarios_router import router as usuarios_router
from routers.clientes_router import router as clientes_router
from routers.sabores_routers import router as sabores_router
from routers.movimientos_stock_router import router as movimientos_stock_router
from fastapi.staticfiles import StaticFiles
from routers.ventas_router import router as ventas_router
from routers.helados_personalizado_router import router as helados_personalizados_router
from routers.detalle_helado_personalizado_router import router as detalle_helado_personalizado_router

from routers.detalle_venta_router import router as detalle_venta_router
from models import Base
# Configuración inicial
logging.basicConfig(level=logging.INFO)
app = FastAPI()

# Configurar SessionMiddleware primero

logging.info("SessionMiddleware configurado correctamente.")
Base.metadata.create_all(bind=engine)
# Configurar CORS después
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



app.include_router(detalle_helado_personalizado_router)
app.include_router(helados_personalizados_router)
app.include_router(detalle_venta_router)
app.include_router(ventas_router)
app.include_router(usuarios_router)
app.include_router(clientes_router)
app.include_router(tipo_usuarios_router)
app.include_router(sabores_router)
app.include_router(productos_fijos_router)
app.include_router(movimientos_stock_router)  # Asegúrate de importar y registrar el router de productos
app.mount("/static", StaticFiles(directory="templates/front"), name="static")
templates = Jinja2Templates(directory="templates")

@app.middleware("http")
async def session_middleware(request: Request, call_next):
    logging.info(f"Solicitud recibida para ruta: {request.url.path}")

    # Permitir solicitudes a archivos estáticos
    if request.url.path.startswith("/static"):
        logging.info(f"Solicitud a archivo estático: {request.url.path}")
        response = await call_next(request)
        return response

    # Rutas públicas (sin validación de sesión)
    public_routes = ["/", "/usuarios/validate/", "/logout/", "/favicon.ico","/docs"]
    if request.url.path in public_routes:
        logging.info(f"Ruta pública detectada: {request.url.path}")
        response = await call_next(request)
        return response

    try:
        logging.info("Validando sesión...")
        session_data = request.session
        logging.info(f"Datos de sesión: {session_data}")

        if not session_data.get("user_id"):
            logging.info("Sesión no válida, redirigiendo a /")
            return RedirectResponse(url="/")

        logging.info("Sesión válida, continuando con la solicitud.")
    except Exception as e:
        logging.error(f"Error inesperado en middleware: {e}")
        return RedirectResponse(url="/")

    response = await call_next(request)
    return response

# Rutas básicas
@app.get("/")
def read_root(request: Request):
    return templates.TemplateResponse("front/login.html", {"request": request})

@app.get("/index")
def read_index(request: Request):
    user_id = request.session.get("user_id")
    nombre_usuario = request.session.get("user_name")
    user = {
        "id": user_id,
        "nombre": nombre_usuario
    }
    return templates.TemplateResponse("front/blank copy.html", {"request": request,"user":user})
@app.get("/productos")
def read_procutos(request: Request):
    user_id = request.session.get("user_id")
    nombre_usuario = request.session.get("user_name")
    user = {
        "id": user_id,
        "nombre": nombre_usuario
    }
    return templates.TemplateResponse("front/productosfijos.html", {"request": request,"user":user})
@app.get("/sabores")
def read_procutos(request: Request):
    return templates.TemplateResponse("front/sabores.html", {"request": request})
@app.get("/venta")
def read_procutos(request: Request):
    return templates.TemplateResponse("front/blank.html", {"request": request})
@app.get("/movimientos", response_class=HTMLResponse)
async def movimientos_stock(request: Request):
    db = SessionLocal()
    movimientos = get_movimientos_stock(db)
    user_id = request.session.get("user_id")
    nombre_usuario = request.session.get("user_name")
    user = {
        "id": user_id,
        "nombre": nombre_usuario
    }
    return templates.TemplateResponse(
        "front/movimientos.html", {"request": request, "movimientos": movimientos,"user":user}
    )
@app.get("/clients")
def read_clientes(request: Request):
    return templates.TemplateResponse("clientes.html", {"request": request})
@app.post("/set-session/")
def set_session(request: Request):
    request.session["user_id"] = 321
    return JSONResponse(content={"message": "Session set"})

@app.get("/get-session/")
def get_session(request: Request):
    user_id = request.session.get("user_id")
    return JSONResponse(content={"user_id": user_id})

@app.post("/logout/")
def logout(request: Request):
    request.session.clear()
    response = RedirectResponse(url="/", status_code=303)
    response.delete_cookie(key="Authorization")
    return response
app.add_middleware(SessionMiddleware, secret_key="clave_super_segura_B)")