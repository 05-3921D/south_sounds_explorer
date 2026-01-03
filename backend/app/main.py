from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from app.api.v1.endpoints import search
from app.core.logging_config import setup_logging
from app.core.config import settings
import logging

@asynccontextmanager
async def lifespan(app: FastAPI):
    setup_logging()
    logger = logging.getLogger("south_sounds_explorer")
    logger.info("Application starting up...")
    yield
    logger.info("Application shutting down...")

app = FastAPI(
    title="South Sounds Explorer API",
    description="API para explorar música de América del Sur",
    version="0.1.0",
    lifespan=lifespan
)

# Security Middlewares

# 1. Trusted Host (Prevent Host Header Attacks)
app.add_middleware(
    TrustedHostMiddleware, 
    allowed_hosts=["localhost", "127.0.0.1", "south-sounds-explorer.onrender.com", "*.onrender.com"] 
)

# 2. CORS (Restrict frontend access)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS, 
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"], # Limit methods if possible
    allow_headers=["*"],
)

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logging.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal Server Error"}
    )

@app.get("/")
async def health_check():
    """Endpoint de verificación."""
    return {"status": "ok", "message": "South Sounds Explorer API está corriendo!"}

@app.get("/api/health")
async def api_health():
    """Verificación de API."""
    return JSONResponse(content={"status": "Activo"})

app.include_router(search.router)
