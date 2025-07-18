from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base
from enum import Enum

DATABASE_URL = "oracle+cx_oracle://usuariosbd:usuariosbd@localhost:1521/orcl"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

class RolEnum(str, Enum):
    cliente = "cliente"
    administrador = "administrador"
    vendedor = "vendedor"
    bodeguero = "bodeguero"
    contador = "contador"

class Usuario(Base):
    __tablename__ = "usuarios"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), unique=True, index=True)
    email = Column(String(100), unique=True, index=True)
    hashed_password = Column(String(255))
    rol = Column(String(50), default=RolEnum.cliente.value)
    primer_inicio = Column(Integer, default=1)

Base.metadata.create_all(bind=engine)

from sqlalchemy.orm import Session

def crear_admin_default():
    from passlib.hash import bcrypt
    session = Session(bind=engine)
    # Usuarios por defecto
    usuarios_default = [
        {
            "username": "admin",
            "email": "admin@ferremas.com",
            "password": "admin123",
            "rol": "administrador",
            "primer_inicio": 1
        },
        {
            "username": "vendedor",
            "email": "vendedor@ferremas.com",
            "password": "vendedor123",
            "rol": "vendedor",
            "primer_inicio": 0
        },
        {
            "username": "bodeguero",
            "email": "bodeguero@ferremas.com",
            "password": "bodeguero123",
            "rol": "bodeguero",
            "primer_inicio": 0
        },
        {
            "username": "contador",
            "email": "contador@ferremas.com",
            "password": "contador123",
            "rol": "contador",
            "primer_inicio": 0 
        },
        {
            "username": "cliente",
            "email": "cliente@ferremas.com",
            "password": "cliente123",
            "rol": "cliente",
            "primer_inicio": 0 
        }
    ]
    for u in usuarios_default:
        existe = session.query(Usuario).filter_by(username=u["username"]).first()
        if not existe:
            usuario = Usuario(
                username=u["username"],
                email=u["email"],
                hashed_password=bcrypt.hash(u["password"]),
                rol=u["rol"],
                primer_inicio=u.get("primer_inicio", 0)
            )
            session.add(usuario)
    session.commit()
    session.close()

crear_admin_default()
