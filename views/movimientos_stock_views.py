from fastapi import APIRouter, Query, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from database import SessionLocal, get_db
from models import MovimientosStock

templates = Jinja2Templates(directory="templates")
def get_movimientos_stock(db: Session, skip: int = 0, limit: int = 100):
    return db.query(MovimientosStock).offset(skip).limit(limit).all()

router = APIRouter(tags=["Vistas - Movimientos Stock"])


@router.get("/movimientos", response_class=HTMLResponse)
async def movimientos_stock_view(request: Request, db: Session = Depends(get_db) , page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100)):
    skip = (page - 1) * size
    total = db.query(MovimientosStock).count()
    movimientos = db.query(MovimientosStock).offset(skip).limit(size).all()

    user = {
        "id": request.session.get("user_id"),
        "nombre": request.session.get("user_name"),
        "tipo_usuario":request.session.get("user_type")
    }

    return templates.TemplateResponse("front/movimientos.html", {"request": request, "movimientos": movimientos, "user": user,"page": page,
        "size": size,
        "total": total,
        "total_pages": (total + size - 1) // size})