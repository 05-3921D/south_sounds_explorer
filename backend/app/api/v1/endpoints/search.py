from fastapi import APIRouter, HTTPException, Query, Depends
from typing import Literal, Optional
from app.services.discogs import DiscogsClient
from app.schemas.schemas import SearchResults
from app.api.dependencies import get_discogs_service

router = APIRouter(prefix="/api/search", tags=["search"])

@router.get("/genres", response_model=dict)
async def get_genres():
    """
    Retorna una lista aleatoria de géneros electrónicos soportados.
    """
    from app.services.discogs import get_random_styles
    return {"genres": get_random_styles(8)}

@router.get("/countries", response_model=dict)
async def get_countries():
    """
    Retorna una lista aleatoria de países de Latam.
    """
    from app.services.discogs import get_random_countries
    return {"countries": get_random_countries(6)}

@router.get("", response_model=SearchResults)
async def search(
    q: Optional[str] = Query(None, description="Nombre del artista o release (Opcional)"),
    sort_by: Literal["recent", "best"] = Query("best", description="Ordenar por 'reciente' o 'mejor'"),
    page: int = Query(1, ge=1, description="Número de página"),
    client: DiscogsClient = Depends(get_discogs_service)
):
    """
    Busca música electrónica sudamericana en Discogs.
    """
    data = await client.search(q, sort_by=sort_by, page=page)
    
    return SearchResults(
        releases=data.get("results", [])
    )
