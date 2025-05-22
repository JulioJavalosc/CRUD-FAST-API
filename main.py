from datetime import datetime
from database import SessionLocal, engine, get_db
from fastapi import FastAPI, Form, HTTPException, Request, Depends, requests
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, HTMLResponse, JSONResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware
import logging
from views.movimientos_stock_views import router as movimientos_stock_views_router
from views.productofijo_views import router as productos_router
from middleware.session_middleware import session_middleware
from routers.productos_fijos_router import router as productos_fijos_router
from routers.tipo_usuarios_router import router as tipo_usuarios_router
from routers.usuarios_router import router as usuarios_router
from routers.clientes_router import router as clientes_router
from routers.LoteSabor_router import router as api_lotes_router
from views.LoteSabor_views import router as web_lotes_router
from routers.sabores_base_router import router as sabores_router
from routers.ConsumoLoteHelado_router import router as consumo_lote_router
from routers.movimientos_stock_router import router as movimientos_stock_router
from fastapi.staticfiles import StaticFiles
from routers.ventas_router import router as ventas_router
from routers.helados_personalizado_router import router as helados_personalizados_router
from routers.detalle_helado_personalizado_router import router as detalle_helado_personalizado_router
from routers.LoteSabor_router import router as lote_sabor_router
from routers.sabores_base_router import router as api_sabores_router
from views.sabores_base_views import router as web_sabores_router
from routers.detalle_venta_router import router as detalle_venta_router
from models import Base, ConsumoLoteHelado, LotesSaboresBase, SaboresBase
# Configuración inicial
logging.basicConfig(level=logging.INFO)
app = FastAPI()

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


app.include_router(consumo_lote_router)
app.include_router(detalle_helado_personalizado_router)
app.include_router(helados_personalizados_router)
app.include_router(detalle_venta_router)
app.include_router(ventas_router)
app.include_router(usuarios_router)
app.include_router(clientes_router)
app.include_router(tipo_usuarios_router)
app.include_router(sabores_router)
app.include_router(lote_sabor_router)
app.include_router(productos_fijos_router)
app.include_router(movimientos_stock_router) 
app.include_router(api_lotes_router)
app.include_router(web_lotes_router)
app.include_router(movimientos_stock_views_router)
app.include_router(api_sabores_router)
app.include_router(web_sabores_router)
app.include_router(productos_router)
app.mount("/static", StaticFiles(directory="templates/front"), name="static")
templates = Jinja2Templates(directory="templates")




# Registrar el middleware
app.middleware("http")(session_middleware)
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

@app.post("/logout/")
def logout(request: Request):
    request.session.clear()
    response = RedirectResponse(url="/", status_code=303)
    response.delete_cookie(key="Authorization")
    return response
app.add_middleware(SessionMiddleware, secret_key="password")