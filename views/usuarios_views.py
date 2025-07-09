import bcrypt
from fastapi import APIRouter, Depends, Form, Path, Request, HTTPException, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from typing import List

from models import Usuarios, TipoUsuarios  # Asegúrate que las rutas sean correctas
from database import get_db
from schemas.user import UsuarioCreate

router = APIRouter(tags=["Usuarios-Admin"])

def encriptar_contraseña(contraseña: str) -> str:
    contraseña_bytes = contraseña.encode('utf-8')
    salt = bcrypt.gensalt()
    hash = bcrypt.hashpw(contraseña_bytes, salt)
    return hash.decode('utf-8')

templates = Jinja2Templates(directory="templates")
@router.get("/usuarios/crear", response_class=HTMLResponse)
async def mostrar_formulario_crear_usuario(request: Request, db: Session = Depends(get_db)):
    tipos_usuarios = db.query(TipoUsuarios).filter(TipoUsuarios.activo == True).all()
    print(tipos_usuarios)
    return templates.TemplateResponse("front/crear_usuario.html", {
        "request": request,
        "tipos_usuarios": tipos_usuarios,
        "user": request.session.get("user")  
    })


@router.post("/usuarios/crear")
async def crear_usuario(
    request: Request,
    Nombre: str = Form(...),
    telefono: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    Tipo_Usuarios_id: int = Form(...),
    db: Session = Depends(get_db)
):
    if not Nombre or not password or not Tipo_Usuarios_id:
        raise HTTPException(status_code=400, detail="Faltan campos obligatorios")

    # Verificar si el tipo de usuario existe
    tipo_usuario = db.query(TipoUsuarios).get(Tipo_Usuarios_id)
    if not tipo_usuario:
        raise HTTPException(status_code=400, detail="Tipo de usuario inválido")
    contraseña_encriptada = encriptar_contraseña(password)
    nuevo_usuario = Usuarios(
        Nombre=Nombre,
        telefono=telefono,
        email=email,
        password=contraseña_encriptada,
        Tipo_Usuarios_id=Tipo_Usuarios_id
    )

    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)

    return RedirectResponse(url="/usuarios/listar", status_code=303)


@router.get("/usuarios/listar", response_class=HTMLResponse)
async def listar_usuarios(request: Request, db: Session = Depends(get_db)):
    usuarios = db.query(Usuarios).all()
    tipos_usuarios = db.query(TipoUsuarios).filter(TipoUsuarios.activo == True).all()
    return templates.TemplateResponse("front/listar_usuarios.html", {
        "request": request,
        "usuarios": usuarios,
        "tipos_usuarios": tipos_usuarios,
        "user": request.session.get("user")
    })




@router.get("/usuarios/{id}/editar", response_class=HTMLResponse)
async def editar_usuario_form(request: Request, id: int, db: Session = Depends(get_db)):
    usuario = db.query(Usuarios).get(id)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    tipos_usuarios = db.query(TipoUsuarios).filter(TipoUsuarios.activo == True).all()
    return templates.TemplateResponse("front/editar_usuario.html", {
        "request": request,
        "usuario": usuario,
        "tipos_usuarios": tipos_usuarios
    })


@router.post("/usuarios/{id}/actualizar")
async def actualizar_usuario(
    id: int = Path(...),
    Nombre: str = Form(...),
    telefono: str = Form(...),
    email: str = Form(...),
    password: str = Form(None),
    Tipo_Usuarios_id: int = Form(...),
    db: Session = Depends(get_db)
):
    usuario = db.query(Usuarios).get(id)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    usuario.Nombre = Nombre
    usuario.telefono = telefono
    usuario.email = email
    if password:
        usuario.password = password  # Asegúrate de tener esta función
    usuario.Tipo_Usuarios_id = Tipo_Usuarios_id
    db.commit()
    return RedirectResponse(url="/usuarios/listar", status_code=303)


@router.post("/usuarios/{id}/desactivar")
async def desactivar_usuario(id: int = Path(...), db: Session = Depends(get_db)):
    usuario = db.query(Usuarios).get(id)
    print("Usuario",usuario.__dict__)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    usuario.activo = False
    db.commit()
    return RedirectResponse(url="/usuarios/listar", status_code=303)

@router.post("/usuarios/{id}/activar")
async def activar_usuario(id: int = Path(...), db: Session = Depends(get_db)):
    usuario = db.query(Usuarios).get(id)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    usuario.activo = True
    db.commit()
    return RedirectResponse(url="/usuarios/listar", status_code=303)