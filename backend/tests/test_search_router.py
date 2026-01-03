import pytest
import respx
from httpx import AsyncClient, ASGITransport
from app.main import app
from app.core.config import settings

@pytest.fixture
def mock_env():
    settings.DISCOGS_CONSUMER_KEY = "test_key"
    settings.DISCOGS_CONSUMER_SECRET = "test_secret"

@pytest.mark.asyncio
async def test_search_endpoint_success(mock_env):
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        async with respx.mock:
            # Mock Discogs Search
            # Return a valid result that matches our filters (Chile, Techno)
            respx.get("https://api.discogs.com/database/search").respond(
                json={
                    "results": [
                        {
                            "id": 123,
                            "title": "Ricardo Villalobos - Alcachofa",
                            "year": "2003",
                            "country": "Chile",
                            "style": ["Minimal", "Techno"],
                            "genre": ["Electronic"],
                            "thumb": "http://img.jpg",
                            "cover_image": "http://img_full.jpg",
                            "uri": "/release/123",
                            "label": ["Perlon"]
                        },
                        {
                            "id": 999,
                            "title": "Random Artist - Pop Song",
                            "country": "USA", # Should be filtered out
                            "style": ["Pop"],
                            "genre": ["Pop"]
                        }
                    ]
                }
            )
            
            response = await ac.get("/api/search", params={"q": "Villalobos"})
            
            assert response.status_code == 200
            data = response.json()
            
            # Should have filtered out the USA result
            assert len(data["releases"]) == 1
            assert data["releases"][0]["title"] == "Ricardo Villalobos - Alcachofa"
            assert data["releases"][0]["country"] == "Chile"

@pytest.mark.asyncio
async def test_search_endpoint_validation_error(mock_env):
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/api/search", params={"q": ""}) # Empty query
        assert response.status_code == 422
