from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .usuarios import router as usuarios_router

app = FastAPI(
    title="API de gestión de usuarios",
    version="1.0.0",
    description="API para gestionar usuario usando FastAPI"
)

app.include_router(usuarios_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"msg": "API de usuarios funcionando"}