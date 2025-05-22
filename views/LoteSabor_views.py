from fastapi import APIRouter, HTTPException, Request, Depends, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from database import get_db
from models import LotesSaboresBase, SaboresBase, ConsumoLoteHelado
from operations.LoteSabor_operations import create_lote

router = APIRouter(tags=["Lotes - Web"])

templates = Jinja2Templates(directory="templates")
@router.get("/lotes", response_class=HTMLResponse)
async def mostrar_lotes(request: Request, db: Session = Depends(get_db)):
    lotes = db.query(LotesSaboresBase).all()
    user = {
        "id": request.session.get("user_id"),
        "nombre": request.session.get("user_name")
    }
    return templates.TemplateResponse("front/lotes.html", {"request": request, "lotes": lotes, "user": user})


@router.get("/lotes/nuevo", response_class=HTMLResponse)
async def mostrar_formulario_nuevo_lote(request: Request, db: Session = Depends(get_db)):
    sabores = db.query(SaboresBase).all()
    user = {
        "id": request.session.get("user_id"),
        "nombre": request.session.get("user_name")
    }
    return templates.TemplateResponse("front/nuevo_lote.html", {"request": request, "sabores": sabores, "user": user})


@router.get("/lotes/{id_lote}", response_class=HTMLResponse)
async def mostrar_detalle_lote(request: Request, id_lote: int, db: Session = Depends(get_db)):
    lote = db.query(LotesSaboresBase).filter(LotesSaboresBase.id_lote == id_lote).first()
    if not lote:
        raise HTTPException(status_code=404, detail="Lote no encontrado")

    consumos = db.query(ConsumoLoteHelado).filter(ConsumoLoteHelado.id_lote == id_lote).all()

    user = {
        "id": request.session.get("user_id"),
        "nombre": request.session.get("user_name")
    }

    return templates.TemplateResponse("front/detalle_lote.html",
                                      {"request": request, "lote": lote, "consumos": consumos, "user": user})


@router.post("/lotes")
async def guardar_nuevo_lote(
    id_sabor: int = Form(...),
    peso_total_gr: int = Form(...),
    numero_lote: str = Form(None),
    db: Session = Depends(get_db)
):
    create_lote(db=db, id_sabor=id_sabor, peso_total_gr=peso_total_gr, numero_lote=numero_lote)
    return RedirectResponse(url="/lotes", status_code=303)