"""
ZapForm - Sistema de coleta de dados via WhatsApp com IA
"""
from contextlib import asynccontextmanager
from fastapi import FastAPI
from sqlmodel import SQLModel

from app.core.database import engine
from app.core.logging_clean import setup_clean_logging, log_startup
from app.routers import webhook


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Gerencia o ciclo de vida da aplicação"""
    # Startup
    log_startup()
    SQLModel.metadata.create_all(engine)
    yield
    # Shutdown
    print("\n👋 Encerrando ZapForm...\n")


# Configurar logging limpo
setup_clean_logging()

# Criar app FastAPI
app = FastAPI(
    title="ZapForm",
    description="Sistema inteligente de coleta de dados via WhatsApp",
    version="1.0.0",
    lifespan=lifespan
)

# Registrar routers
app.include_router(webhook.router, prefix="/webhook", tags=["webhook"])


@app.get("/")
def root():
    """Health check"""
    return {
        "status": "online",
        "service": "ZapForm",
        "version": "1.0.0"
    }


@app.get("/health")
def health():
    """Health check detalhado"""
    return {
        "status": "healthy",
        "database": "connected",
        "webhook": "ready"
    }