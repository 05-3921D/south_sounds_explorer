import pytest
import respx
from httpx import AsyncClient, ASGITransport
from app.main import app
from app.config import settings

@pytest.fixture
def mock_env():
    settings.SPOTIFY_CLIENT_ID = "test_id"
    settings.SPOTIFY_CLIENT_SECRET = "test_secret"

@pytest.mark.asyncio
async def test_search_endpoint_success(mock_env):
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        async with respx.mock:
            # Mock Token
            respx.post("https://accounts.spotify.com/api/token").respond(
                json={"access_token": "mock_token", "expires_in": 3600}
            )
            # Mock Search
            respx.get("https://api.spotify.com/v1/search").respond(
                json={
                    "albums": {
                        "items": [
                            {
                                "name": "Test Album", 
                                "id": "1", 
                                "images": [{"url": "http://img", "height": 640, "width": 640}],
                                "artists": [{"id": "a1", "name": "Artist"}],
                                "release_date": "2023-01-01",
                                "total_tracks": 10,
                                "external_urls": {"spotify": "http://url"}
                            }
                        ]
                    },
                    "tracks": {
                        "items": [
                            {
                                "name": "Test Track", 
                                "id": "2", 
                                "duration_ms": 300000,
                                "artists": [{"id": "a1", "name": "Artist"}],
                                "album": {
                                    "name": "Test Album", 
                                    "id": "1", 
                                    "images": [{"url": "http://img", "height": 640, "width": 640}],
                                    "artists": [{"id": "a1", "name": "Artist"}],
                                    "release_date": "2023-01-01",
                                    "total_tracks": 10,
                                    "external_urls": {"spotify": "http://url"}
                                },
                                "popularity": 50,
                                "external_urls": {"spotify": "http://url"}
                            }
                        ]
                    }
                }
            )
            
            response = await ac.get("/api/search", params={"q": "test"})
            
            assert response.status_code == 200
            data = response.json()
            assert len(data["albums"]) == 1
            assert data["albums"][0]["name"] == "Test Album"

@pytest.mark.asyncio
async def test_search_endpoint_validation_error(mock_env):
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/api/search", params={"q": ""}) # Empty query
        assert response.status_code == 422
