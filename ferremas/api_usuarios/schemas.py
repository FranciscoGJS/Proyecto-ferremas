from pydantic import BaseModel
from .db import RolEnum

class UsuarioCreate(BaseModel):
    username: str
    email: str
    password: str
    rol: RolEnum = RolEnum.cliente

class UsuarioLogin(BaseModel):
    username: str
    password: str