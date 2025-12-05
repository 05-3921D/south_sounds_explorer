from fastapi import FastAPI
from fastapi.responses import JSONResponse

app = FastAPI(
    title="South Sounds Explorer API",
    description="API para explorar música de América del Sur",
    version="0.1.0"
)

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # En producción, reemplazar con URL del frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def health_check():
    """Endpoint de verificación."""
    return {"status": "ok", "message": "South Sounds Explorer API está corriendo!"}

@app.get("/api/health")
async def api_health():
    """Verificación de API."""
    return JSONResponse(content={"status": "Activo"})

# Import and include the search router
from app.routers import search
app.include_router(search.router)
