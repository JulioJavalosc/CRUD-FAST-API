from typing import Optional
from fastapi import APIRouter, Depends, Form, Request, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from operations.sabores_base_operations import (
    get_sabores_base,
    get_sabor_base,
    create_sabor_base,
    update_sabor_base,
    delete_sabor_base
)
from database import get_db
router = APIRouter(tags=["Sabores Base - Web"])
templates = Jinja2Templates(directory="templates")
@router.get("/sabores-base", response_class=HTMLResponse)
def read_sabores(request: Request, db: Session = Depends(get_db)):
    sabores = get_sabores_base(db)
    return templates.TemplateResponse("front/sabores.html", {"request": request, "sabores": sabores})
@router.get("/sabores-base/{sabor_id}", response_class=HTMLResponse)
def read_sabor(request: Request, sabor_id: int, db: Session = Depends(get_db)):
    sabor = get_sabor_base(db, sabor_id=sabor_id)
    if not sabor:
        raise HTTPException(status_code=404, detail="Sabor no encontrado")
    return templates.TemplateResponse("front/sabor_detalle.html", {"request": request, "sabor": sabor})
@router.get("/sabores-base/nuevo", response_class=HTMLResponse)
def mostrar_formulario_nuevo_sabor(request: Request):
    return templates.TemplateResponse("front/sabor_form.html", {"request": request})
@router.post("/sabores-base/guardar")
def guardar_sabor(
    Nombre: str = Form(...),
    Precio: int = Form(...),
    sabor_id: Optional[str] = Form(None), 
    db: Session = Depends(get_db)
):
    sabor_id_int = int(sabor_id) if sabor_id and sabor_id.isdigit() else None

    if sabor_id_int:
        db_sabor = update_sabor_base(db, sabor_id=sabor_id_int, Nombre=Nombre, Precio=Precio)
    else:
        db_sabor = create_sabor_base(db, Nombre=Nombre, Precio=Precio)

    if not db_sabor:
        raise HTTPException(status_code=400, detail="Error al guardar")

    return RedirectResponse(url="/sabores-base", status_code=303)
@router.get("/sabores-base/{sabor_id}/eliminar")
def eliminar_sabor_web(sabor_id: int, db: Session = Depends(get_db)):
    resultado = delete_sabor_base(db, sabor_id=sabor_id)
    if not resultado:
        raise HTTPException(status_code=404, detail="Sabor no encontrado")
    return RedirectResponse(url="/sabores-base", status_code=303)