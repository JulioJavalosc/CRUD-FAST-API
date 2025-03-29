from datetime import datetime, timedelta
import secrets
from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from typing import List
from schemas.user import UserCreate, UserUpdate, UserResponse, UserValidate
from database import get_db
from operations.user_operations import (
    get_users,
    get_user,
    create_user,
    update_user,
    delete_user,
    validate_user,
)
from session.session_layer import create_random_session_string

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/", response_model=List[UserResponse])
def read_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return get_users(db, skip=skip, limit=limit)

@router.get("/{user_id}", response_model=UserResponse)
def read_user(user_id: int, db: Session = Depends(get_db)):
    user = get_user(db, user_id=user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.post("/validate/")
def validate_user_route(user_data: dict, request: Request, db=Depends(get_db)):
    email = user_data.get("email")
    print("Email",email)
    password = user_data.get("password")
    print("Password",password)
    # Validar credenciales
    user = validate_user(db, email=email, password=password)
    if not user:
        raise HTTPException(status_code=401, detail="Credenciales inválidas")

    # Crear una sesión segura
    session_id = secrets.token_urlsafe(32)
    print(session_id)
    access_token = secrets.token_urlsafe(32)
    token_expiry = int((datetime.now() + timedelta(minutes=30)).timestamp())

    # Almacenar datos en la sesión
    request.session.update({
        "user_id": user.id, 
        "session_id": session_id,
        "access_token": access_token,
        "token_expiry": token_expiry,
    })

    # Almacenar el session_id en una cookie
    response = JSONResponse(content={"message": "Login successful"})
    response.set_cookie(key="Authorization", value=session_id, httponly=True, secure=True)
    return response

@router.post("/", response_model=UserResponse)
def create_new_user(user: UserCreate, db: Session = Depends(get_db)):
    return create_user(db=db, user=user)

@router.put("/{user_id}", response_model=UserResponse)
def update_existing_user(user_id: int, user: UserUpdate, db: Session = Depends(get_db)):
    db_user = update_user(db, user_id=user_id, user=user)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@router.delete("/{user_id}", response_model=UserResponse)
def delete_existing_user(user_id: int, db: Session = Depends(get_db)):
    db_user = delete_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user