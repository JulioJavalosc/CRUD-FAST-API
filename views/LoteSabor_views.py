from fastapi import APIRouter, HTTPException, Query, Request, Depends, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy import desc
from sqlalchemy.orm import Session
from database import get_db
from models import LotesSaboresBase, SaboresBase, ConsumoLoteHelado
from operations.LoteSabor_operations import create_lote
from schemas.LoteSabor import LoteSaborCreate

router = APIRouter(tags=["Lotes - Web"])

templates = Jinja2Templates(directory="templates")
@router.get("/lotes", response_class=HTMLResponse)
async def mostrar_lotes(
    request: Request,
    db: Session = Depends(get_db),
    page: int = Query(1, ge=1),
    size: int = Query(5, ge=1, le=100)
):
    skip = (page - 1) * size
    total = db.query(LotesSaboresBase).count()
    lotes = db.query(LotesSaboresBase).order_by(desc(LotesSaboresBase.fecha_ingreso)).offset(skip).limit(size).all()

    user = {
        "id": request.session.get("user_id"),
        "nombre": request.session.get("user_name"),
        "tipo_usuario":request.session.get("user_type")
    }

    return templates.TemplateResponse("front/lotes.html", {
        "request": request,
        "lotes": lotes,
        "user": user,
        "page": page,
        "size": size,
        "total": total,
        "total_pages": (total + size - 1) // size
    })


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
    print("Peso_Total:",peso_total_gr)
    print(id_sabor)
    print(numero_lote)


    lote_data = LoteSaborCreate(
    id_sabor=id_sabor,
    peso_total_gr=peso_total_gr,
    numero_lote=numero_lote
)

# Pasar la instancia a la función
    create_lote(db=db, lote=lote_data)
    return RedirectResponse(url="/lotes", status_code=303)