from calendar import month_name
from datetime import datetime
import json
from typing import List, Optional
from fastapi import APIRouter, Form, HTTPException, Query, Request, Depends, Response
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from jinja2 import Environment, FileSystemLoader
from sqlalchemy import extract
from sqlalchemy.orm import Session

from models import Clientes, ConsumoLoteHelado, DetalleHeladoPersonalizado, DetalleVenta, HeladosPersonalizados, LotesSaboresBase, MovimientosStock, ProductosFijos,SaboresBase, Ventas
from database import get_db
import io
from xhtml2pdf import pisa
templates = Jinja2Templates(directory="templates")
env = Environment(loader=FileSystemLoader("templates"))
router = APIRouter(tags=["Ventas - Web"])


def generar_pdf_con_xhtml2pdf(venta_data: dict) -> bytes:
    template = env.get_template("venta_pdf.html")
    html_content = template.render(venta=venta_data)

    pdf_buffer = io.BytesIO()
    pisa_status = pisa.CreatePDF(
        src=html_content,
        dest=pdf_buffer
    )

    if pisa_status.err:
        raise Exception("Error al generar el PDF")

    return pdf_buffer.getvalue()
@router.get("/ventas/nueva", response_class=HTMLResponse)
def nueva_venta(request: Request, db: Session = Depends(get_db)):
    clientes = db.query(Clientes).all()
    productos = db.query(ProductosFijos).all()
    sabores = db.query(SaboresBase).join(SaboresBase.lotes).all()
    user = {
        "id": request.session.get("user_id"),
        "nombre": request.session.get("user_name"),
        "tipo_usuario":request.session.get("user_type")
    }

    return templates.TemplateResponse("front/ventas_form.html", {
        "request": request,
        "clientes": clientes,
        "productos": productos,
        "user": user,
        "sabores":sabores
    })


@router.post("/ventas/guardar")
async def guardar_venta(
    request: Request,
    Clientes_id: int = Form(...),
    Usuarios_id: int = Form(...),
    idProducto: Optional[List[int]] = Form(None),
    Cantidad: Optional[List[int]] = Form(None),
    total_general: float = Form(...),
    helados_json: Optional[str] = Form(None),
    db: Session = Depends(get_db)
):
    PESO_POR_BOLA_GR = 60

    # Recolectar info para el PDF
    productos_fijos_data = []
    helados_data = []

    try:
        nueva_venta = Ventas(
            Fecha=datetime.now(),
            Clientes_id=Clientes_id,
            total=0,
            estado=2,
            Usuarios_id=Usuarios_id
        )
        db.add(nueva_venta)
        db.commit()
        db.refresh(nueva_venta)

        # Procesar productos fijos
        if idProducto:
            for i in range(len(idProducto)):
                id_producto = idProducto[i]
                cantidad = Cantidad[i] if i < len(Cantidad) else 1

                producto = db.query(ProductosFijos).get(id_producto)
                if not producto:
                    raise ValueError(f"Producto {id_producto} no encontrado")

                detalle = DetalleVenta(
                    idVenta=nueva_venta.idVenta,
                    idProducto=id_producto,
                    idHelado=None,
                    Cantidad=cantidad,
                    subtotal=producto.Precio * cantidad
                )
                db.add(detalle)

                producto.Stock = max(producto.Stock - cantidad, 0)

                movimiento = MovimientosStock(
                    Cantidad=cantidad,
                    Fecha=datetime.utcnow(),
                    Tipo_Movimiento=2,
                    idProducto=id_producto,
                    idUsuario=Usuarios_id
                )
                db.add(movimiento)

                productos_fijos_data.append({
                    "nombre": producto.Descripcion,
                    "cantidad": cantidad,
                    "subtotal": producto.Precio * cantidad
                })

            db.commit()

        # Procesar helados personalizados
        if helados_json:
            helados_list = json.loads(helados_json)

            for helado in helados_list:
                cantidad_helado = helado["cantidad"]
                precio_helado = helado["precio"]
                sabores = helado["sabores"]

                nuevo_helado = HeladosPersonalizados(
                    precio_total=precio_helado
                )
                db.add(nuevo_helado)
                db.commit()
                db.refresh(nuevo_helado)

                sabores_data = []

                for sabor in sabores:
                    sabor_id = int(sabor["id"])
                    bolas = int(sabor["bolas"])
                    gramos_necesarios = bolas * PESO_POR_BOLA_GR

                    sabor_nombre = db.query(SaboresBase).get(sabor_id).Nombre
                    sabores_data.append({
                        "nombre": sabor_nombre,
                        "bolas": bolas
                    })

                    detalle_sabor = DetalleHeladoPersonalizado(
                        idHelado=nuevo_helado.idHelado,
                        id_Sabor=sabor_id,
                        Cantidad_Bolas=bolas
                    )
                    db.add(detalle_sabor)
                    db.commit()
                    db.refresh(detalle_sabor)

                    lotes = db.query(LotesSaboresBase)\
                        .filter(
                            LotesSaboresBase.id_sabor == sabor_id,
                            LotesSaboresBase.peso_disponible_gr > 0
                        )\
                        .order_by(LotesSaboresBase.fecha_ingreso.asc())\
                        .all()

                    for lote in lotes:
                        if gramos_necesarios <= 0:
                            break

                        disponible = lote.peso_disponible_gr
                        a_consumir = min(disponible, gramos_necesarios)

                        lote.peso_disponible_gr -= a_consumir
                        gramos_necesarios -= a_consumir

                        consumo = ConsumoLoteHelado(
                            id_detalle_helado=detalle_sabor.idDetalle_Helado_Personalizado,
                            id_lote=lote.id_lote,
                            cantidad_utilizada_gr=a_consumir
                        )
                        db.add(consumo)

                    if gramos_necesarios > 0:
                        raise HTTPException(
                            status_code=400,
                            detail=f"No hay suficiente stock para el sabor ID {sabor_id} (faltan {gramos_necesarios}g)"
                        )

                detalle_venta_helado = DetalleVenta(
                    idVenta=nueva_venta.idVenta,
                    idProducto=None,
                    idHelado=nuevo_helado.idHelado,
                    Cantidad=cantidad_helado,
                    subtotal=precio_helado * cantidad_helado
                )
                db.add(detalle_venta_helado)

                helados_data.append({
                    "sabores": sabores_data,
                    "cantidad": cantidad_helado,
                    "subtotal": precio_helado * cantidad_helado
                })

            db.commit()

        # Total final
        nueva_venta.total = total_general
        db.commit()

        # Armar datos para PDF
        venta_data = {
            "id": nueva_venta.idVenta,
            "fecha": nueva_venta.Fecha.strftime("%d/%m/%Y %H:%M"),
            "cliente_id": Clientes_id,
            "productos": productos_fijos_data + helados_data,
            "total": total_general
        }

        pdf_bytes = generar_pdf_con_xhtml2pdf(venta_data)

        return Response(
            content=pdf_bytes,
            media_type="application/pdf",
            headers={"Content-Disposition": f"inline; filename=venta_{nueva_venta.idVenta}.pdf"}
        )

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Error al registrar la venta: {str(e)}")

@router.get("/ventas/listar", response_class=HTMLResponse)
def listar_venta(request: Request, db: Session = Depends(get_db) ,    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100)):
    skip = (page - 1) * size
    totalp = db.query(Ventas).where(Ventas.total>0).count()
    ventas = db.query(Ventas).where(Ventas.total>0).offset(skip).limit(size).all()
    user = {
        "id": request.session.get("user_id"),
        "nombre": request.session.get("user_name"),
        "tipo_usuario":request.session.get("user_type")
    }

    return templates.TemplateResponse("front/ventas_listado.html", {
        "request": request,
        "user": user,
        "ventas": ventas,
        "page": page,
        "size": size,
        "total": totalp,
        "total_pages": (totalp + size - 1) // size
    })


@router.get("/ventas/{id_Venta}", response_class=HTMLResponse)
async def mostrar_detalle_venta(request: Request, id_Venta: int, db: Session = Depends(get_db)):
    venta = db.query(Ventas).filter(Ventas.idVenta == id_Venta).first()

    if not venta:
        raise HTTPException(status_code=404, detail="venta no encontrada")

    detalle = db.query(DetalleVenta).filter(DetalleVenta.idVenta == id_Venta).all()
    print("Venta:", venta.__dict__)
    for d in detalle:
        print("Detalle:", d.__dict__)
    user = {
        "id": request.session.get("user_id"),
        "nombre": request.session.get("user_name")
    }

    return templates.TemplateResponse("front/detalle_venta.html",
                                      {"request": request, "venta": venta, "detalles": detalle, "user": user})



@router.get("/ventas/{id_venta}/pdf")
def generar_pdf_venta(id_venta: int, db: Session = Depends(get_db)):
    venta = db.query(Ventas).get(id_venta)
    if not venta:
        raise HTTPException(status_code=404, detail="Venta no encontrada")

    productos = db.query(DetalleVenta).filter(DetalleVenta.idVenta == id_venta).all()

    productos_fijos_data = []
    helados_data = []

    for p in productos:
        if p.idProducto:
            producto = db.query(ProductosFijos).get(p.idProducto)
            productos_fijos_data.append({
                "nombre": producto.Descripcion,
                "cantidad": p.Cantidad,
                "subtotal": p.subtotal
            })
        elif p.idHelado:
            detalle_helado = db.query(DetalleHeladoPersonalizado).filter(
                DetalleHeladoPersonalizado.idHelado == p.idHelado
            ).all()

            sabores = []
            for s in detalle_helado:
                sabor = db.query(SaboresBase).get(s.id_Sabor)
                sabores.append({
                    "nombre": sabor.Nombre,
                    "bolas": s.Cantidad_Bolas
                })

            helados_data.append({
                "sabores": sabores,
                "cantidad": p.Cantidad,
                "subtotal": p.subtotal
            })

    venta_data = {
        "id": venta.idVenta,
        "fecha": venta.Fecha.strftime("%d/%m/%Y %H:%M"),
        "cliente_id": venta.cliente.Nombre + " " + venta.cliente.Apellido,
        "encargado": venta.usuario.Nombre , 
        "productos": productos_fijos_data + helados_data,
        "total": venta.total
    }

    pdf_bytes = generar_pdf_con_xhtml2pdf(venta_data)

    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={"Content-Disposition": f"inline; filename=venta_{venta.idVenta}.pdf"}
    )


@router.get("/reportes/ventas-anuales/pdf")
def generar_informe_anual_pdf(request: Request,db: Session = Depends(get_db)):
    
    anio = datetime.now().year
    resumen_mensual = []
    total_anual = 0

    user = {
        "id": request.session.get("user_id"),
        "nombre": request.session.get("user_name"),
        "tipo_usuario":request.session.get("user_type")
    }
    for mes in range(1, 13):
        ventas_mes = db.query(DetalleVenta).join(Ventas).filter(
            extract("month", Ventas.Fecha) == mes,
            extract("year", Ventas.Fecha) == anio
        ).all()

        productos_resumen = {}
        total_mes = 0

        for detalle in ventas_mes:
            if detalle.idProducto:
                producto = db.query(ProductosFijos).get(detalle.idProducto)
                if producto:
                    nombre = producto.Descripcion
                    if nombre not in productos_resumen:
                        productos_resumen[nombre] = {
                            "cantidad": 0,
                            "total": 0
                        }
                    productos_resumen[nombre]["cantidad"] += detalle.Cantidad
                    productos_resumen[nombre]["total"] += detalle.subtotal
                    total_mes += detalle.subtotal

        productos_list = [
            {
                "nombre": nombre,
                "cantidad": datos["cantidad"],
                "total": datos["total"]
            }
            for nombre, datos in productos_resumen.items()
        ]

        resumen_mensual.append({
            "nombre_mes": month_name[mes],
            "productos": productos_list,
            "total_mes": total_mes
        })

        total_anual += total_mes

    # Renderizar PDF
    template = env.get_template("ventas_form.html")
    html_content = template.render(
        resumen_mensual=resumen_mensual,
        total_anual=total_anual,
        anio=anio,
        fecha=datetime.now().strftime("%d/%m/%Y"),
        encargado = user["nombre"] , 
    )

    buffer = io.BytesIO()
    pisa_status = pisa.CreatePDF(html_content, dest=buffer)
    if pisa_status.err:
        return {"error": "No se pudo generar el PDF"}

    buffer.seek(0)
    return Response(
        content=buffer.read(),
        media_type="application/pdf",
        headers={"Content-Disposition": f"inline; filename=informe_ventas_{anio}.pdf"}
    )