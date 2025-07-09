from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import and_, extract, func
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
from views.ventas_views import router as ventas_web_router
from routers.helados_personalizado_router import router as helados_personalizados_router
from routers.detalle_helado_personalizado_router import router as detalle_helado_personalizado_router
from routers.LoteSabor_router import router as lote_sabor_router
from routers.sabores_base_router import router as api_sabores_router
from views.sabores_base_views import router as web_sabores_router
from routers.detalle_venta_router import router as detalle_venta_router
from views.usuarios_views import router as usuarios_admin_router
from models import Base, ConsumoLoteHelado, LotesSaboresBase, SaboresBase, Ventas
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
app.include_router(ventas_web_router)
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
app.include_router(usuarios_admin_router)
app.mount("/static", StaticFiles(directory="templates/front"), name="static")
templates = Jinja2Templates(directory="templates")




# Registrar el middleware
app.middleware("http")(session_middleware)
# Rutas básicas
@app.get("/")
def read_root(request: Request):
    return templates.TemplateResponse("front/login.html", {"request": request})

@app.get("/index")
def read_index(request: Request, db: Session = Depends(get_db)):
    user_id = request.session.get("user_id")
    nombre_usuario = request.session.get("user_name")
    tipo_usuario = request.session.get("user_type")
    print("TIPO DE USUARIO",tipo_usuario)
    user = {
        "id": user_id,
        "nombre": nombre_usuario,
        "tipo_usuario":tipo_usuario
    }

    ahora = datetime.now()

    ganancias_mensuales = db.query(func.sum(Ventas.total)).filter(
        func.extract('month', Ventas.Fecha) == ahora.month,
        func.extract('year', Ventas.Fecha) == ahora.year,
        Ventas.estado == 2
    ).scalar() or 0

    ganancias_anuales = db.query(func.sum(Ventas.total)).filter(
        func.extract('year', Ventas.Fecha) == ahora.year,
        Ventas.estado == 2
    ).scalar() or 0

    # ➕ Consulta para lotes
    lotes_disponibles = db.query(func.count()).select_from(LotesSaboresBase).filter(
        LotesSaboresBase.peso_disponible_gr > 0
    ).scalar()

    lotes_escasez = db.query(func.count()).select_from(LotesSaboresBase).filter(
        and_(
            LotesSaboresBase.peso_disponible_gr <= 2000,
            LotesSaboresBase.peso_disponible_gr > 0
        )
    ).scalar()
    year = datetime.now().year

# Consulta a la base de datos
    ventas_crudas = (
        db.query(
        extract("month", Ventas.Fecha).label("mes"),
        func.sum(Ventas.total).label("total")
    )
    .filter(
        extract("year", Ventas.Fecha) == year,
        Ventas.estado == 2  # solo ventas confirmadas
    )
    .group_by("mes")
    .all()
    )

    # Crear diccionario base con todos los meses en 0
    ventas_por_mes_dict = {mes: 0 for mes in range(1, 13)}

# Completar con los valores reales
    for mes, total in ventas_crudas:
        ventas_por_mes_dict[int(mes)] = float(total or 0)

# Convertir a lista ordenada si se necesita para pasar al frontend o gráfico
    ventas_por_mes = [ventas_por_mes_dict[mes] for mes in range(1, 13)]

    print("Ventas por Mes:", ventas_por_mes)
    return templates.TemplateResponse("front/blank copy.html", {
        "request": request,
        "user": user,
        "ganancias_mensuales": ganancias_mensuales,
        "ganancias_anuales": ganancias_anuales,
        "lotes_disponibles": lotes_disponibles,
        "lotes_escasez": lotes_escasez,
        "ventas_por_mes":ventas_por_mes
    })

@app.post("/logout/")
def logout(request: Request):
    request.session.clear()
    response = RedirectResponse(url="/", status_code=303)
    response.delete_cookie(key="Authorization")
    return response
app.add_middleware(SessionMiddleware, secret_key="password")

@app.get("/chart")
def charts(request:Request):
    return templates.TemplateResponse("front/blank copy.html", {"request": request})