from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from app.routers import search
from app.logging_config import setup_logging
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

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # En producción, reemplazar con URL del frontend
    allow_credentials=True,
    allow_methods=["*"],
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
