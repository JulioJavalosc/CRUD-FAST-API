from typing import Optional
from fastapi import APIRouter, Request, Depends, Form
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from operations.productos_fijos_operations import (
    get_productos_fijos,
    create_producto_fijo,
    update_producto_fijo,
    delete_producto_fijo,
    actualizar_stock_producto
)

from schemas.productos_fijos import ProductoFijoCreate, ProductoFijoUpdate

from database import get_db

router = APIRouter(tags=["Productos Fijos - Web"])
templates = Jinja2Templates(directory="templates")
@router.get("/productos")
async def read_productos(request: Request, db: Session = Depends(get_db)):
    productos = get_productos_fijos(db)
    user = {
        "id": request.session.get("user_id"),
        "nombre": request.session.get("user_name"),
        "tipo_usuario":request.session.get("user_type")
    }
    return templates.TemplateResponse("front/productosfijos.html", {"request": request, "productos": productos, "user": user})

@router.post("/productos/guardar")
async def guardar_producto(
    Descripcion: str = Form(...),
    Precio: int = Form(...),
    Stock: int = Form(...),
    producto_id: Optional[str] = Form(None),
    usuario_id: int = Form(1),  # ← Debe venir del login real después
    db: Session = Depends(get_db)
):
    producto_id_int = int(producto_id) if producto_id and producto_id.isdigit() else None

    if producto_id_int:
        # Llamar a update_producto_fijo con usuario_id
        update_producto_fijo(db, producto_id=producto_id_int, producto_data=ProductoFijoUpdate(
            Descripcion=Descripcion,
            Precio=Precio,
            Stock=Stock
        ), usuario_id=usuario_id)
    else:
        create_producto_fijo(db, ProductoFijoCreate(
            Descripcion=Descripcion,
            Precio=Precio,
            Stock=Stock,
            idUsuario=usuario_id
        ))

    return RedirectResponse(url="/productos", status_code=303)

@router.get("/productos/{producto_id}/eliminar")
async def eliminar_producto_web(producto_id: int, db: Session = Depends(get_db)):
    delete_producto_fijo(db, producto_id=producto_id)
    return RedirectResponse(url="/productos", status_code=303)