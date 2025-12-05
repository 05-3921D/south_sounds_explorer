from fastapi import APIRouter, HTTPException, Query
from app.services.spotify import SpotifyClient
from app.schemas import SearchResults

router = APIRouter(prefix="/api/search", tags=["search"])

@router.get("", response_model=SearchResults)
async def search(q: str = Query(..., min_length=1, description="Search query")):
    """
    Busca por albums y tracks en Spotify.
    """
    client = SpotifyClient()
    try:
        results = await client.search(q, type="album,track", limit=10)
        
        # Revisa la respuesta de Spotify para ajustar con el esquema
        albums_data = results.get("albums", {}).get("items", [])
        tracks_data = results.get("tracks", {}).get("items", [])
        
        return SearchResults(
            albums=albums_data,
            tracks=tracks_data
        )
    except Exception as e:
        # In a real app, log the error
        raise HTTPException(status_code=500, detail=str(e))
