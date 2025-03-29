from datetime import datetime
from database import engine
from fastapi import FastAPI, HTTPException, Request, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware
import logging
from routers.users import router as user_router  # Importar las rutas de usuarios
from fastapi.staticfiles import StaticFiles
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

# Registrar el router de usuarios
app.include_router(user_router)
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# @app.middleware("http")
# async def session_middleware(request: Request, call_next):
#     logging.info(f"Solicitud recibida para ruta: {request.url.path}")

#     # Permitir solicitudes a archivos estáticos
#     if request.url.path.startswith("/static"):
#         logging.info(f"Solicitud a archivo estático: {request.url.path}")
#         response = await call_next(request)
#         return response

#     # Rutas públicas (sin validación de sesión)
#     public_routes = ["/", "/users/validate/", "/logout/", "/favicon.ico"]
#     if request.url.path in public_routes:
#         logging.info(f"Ruta pública detectada: {request.url.path}")
#         response = await call_next(request)
#         return response

#     try:
#         logging.info("Validando sesión...")
#         session_data = request.session
#         logging.info(f"Datos de sesión: {session_data}")

#         if not session_data.get("user_id"):
#             logging.info("Sesión no válida, redirigiendo a /")
#             return RedirectResponse(url="/")

#         logging.info("Sesión válida, continuando con la solicitud.")
#     except Exception as e:
#         logging.error(f"Error inesperado en middleware: {e}")
#         return RedirectResponse(url="/")

#     response = await call_next(request)
#     return response

# Rutas básicas
@app.get("/")
def read_root(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.get("/index")
def read_index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

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
    response = JSONResponse(content={"message": "Logged out successfully"})
    response.delete_cookie(key="Authorization")
    return response


app.add_middleware(SessionMiddleware, secret_key="clave_super_segura_B)")