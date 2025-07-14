from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from passlib.hash import bcrypt
from .db import Usuario
from .schemas import UsuarioCreate, UsuarioLogin
from .deps import get_db

router = APIRouter()

@router.post("/registro/")
def registro(usuario: UsuarioCreate, db: Session = Depends(get_db)):
    if db.query(Usuario).filter(Usuario.username == usuario.username).first():
        raise HTTPException(status_code=400, detail="Usuario ya existe")
    hashed_password = bcrypt.hash(usuario.password)
    db_usuario = Usuario(
        username=usuario.username,
        email=usuario.email,
        hashed_password=hashed_password,
        rol=usuario.rol
    )
    db.add(db_usuario)
    db.commit()
    db.refresh(db_usuario)
    return {"msg": "Usuario creado correctamente"}

@router.post("/login/")
def login(usuario: UsuarioLogin, db: Session = Depends(get_db)):
    db_usuario = db.query(Usuario).filter(Usuario.username == usuario.username).first()
    if not db_usuario or not bcrypt.verify(usuario.password, db_usuario.hashed_password):
        raise HTTPException(status_code=400, detail="Credenciales incorrectas")
    
    # Verificar si es administrador y primer inicio
    primer_inicio = False
    if db_usuario.rol == "administrador" and db_usuario.primer_inicio == 1:
        primer_inicio = True
    
    return {
        "msg": "Login exitoso", 
        "rol": db_usuario.rol, 
        "username": db_usuario.username,
        "primer_inicio": primer_inicio,
        "user_id": db_usuario.id
    }

@router.get("/usuarios/")
def listar_usuarios(db: Session = Depends(get_db)):
    usuarios = db.query(Usuario).order_by(Usuario.id.asc()).all()
    return [
        {"id": u.id, "username": u.username, "email": u.email, "rol": u.rol}
        for u in usuarios
    ]

@router.get("/usuarios/{user_id}")
def obtener_usuario(user_id: int, db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(Usuario.id == user_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return {"id": usuario.id, "username": usuario.username, "email": usuario.email, "rol": usuario.rol}

@router.put("/usuarios/{user_id}")
def actualizar_usuario(user_id: int, usuario_data: UsuarioCreate, db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(Usuario.id == user_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    usuario.username = usuario_data.username
    usuario.email = usuario_data.email
    usuario.hashed_password = bcrypt.hash(usuario_data.password)
    usuario.rol = usuario_data.rol
    db.commit()
    db.refresh(usuario)
    return {"msg": "Usuario actualizado"}

@router.patch("/usuarios/{user_id}")
def actualizar_usuario_parcial(user_id: int, usuario_data: dict, db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(Usuario.id == user_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    for key, value in usuario_data.items():
        if key == "password":
            value = bcrypt.hash(value)
            setattr(usuario, "hashed_password", value)
        elif hasattr(usuario, key):
            setattr(usuario, key, value)
    db.commit()
    db.refresh(usuario)
    return {"msg": "Usuario actualizado parcialmente"}

@router.delete("/usuarios/{user_id}")
def eliminar_usuario(user_id: int, db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(Usuario.id == user_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    db.delete(usuario)
    db.commit()
    return {"msg": "Usuario eliminado"}

@router.post("/usuarios/cambiar-rol/")
def cambiar_rol(user_id: int, nuevo_rol: str, db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(Usuario.id == user_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    usuario.rol = nuevo_rol
    db.commit()
    return {"msg": "Rol actualizado"}

@router.post("/cambiar-password-primer-inicio/")
def cambiar_password_primer_inicio(
    data: dict,
    db: Session = Depends(get_db)
):
    user_id = data.get("user_id")
    nueva_password = data.get("nueva_password")
    
    usuario = db.query(Usuario).filter(Usuario.id == user_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    

    usuario.hashed_password = bcrypt.hash(nueva_password)
    usuario.primer_inicio = 0
    db.commit()
    
    return {"msg": "Contraseña actualizada correctamente"}

DATABASE_URL = "oracle+cx_oracle://usuariosbd:usuariosbd@localhost:1521/?service_name=orcl"
