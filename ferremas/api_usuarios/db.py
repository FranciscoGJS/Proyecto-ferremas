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

Base.metadata.create_all(bind=engine)