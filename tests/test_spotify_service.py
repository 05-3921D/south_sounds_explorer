import pytest
import respx
import httpx
from app.services.spotify import SpotifyClient
from app.config import settings

@pytest.fixture
async def spotify_client():
    async with httpx.AsyncClient() as http_client:
        client = SpotifyClient(http_client)
        # Mock settings to ensure valid credentials check passes
        settings.SPOTIFY_CLIENT_ID = "test_id"
        settings.SPOTIFY_CLIENT_SECRET = "test_secret"
        yield client

@pytest.mark.asyncio
async def test_get_token_success(spotify_client):
    async with respx.mock:
        route = respx.post("https://accounts.spotify.com/api/token").respond(
            json={"access_token": "mock_token", "expires_in": 3600}
        )
        
        token = await spotify_client._get_token()
        
        assert token == "mock_token"
        assert route.called
        assert spotify_client.access_token == "mock_token"

@pytest.mark.asyncio
async def test_search_success(spotify_client):
    async with respx.mock:
        # Mock auth
        respx.post("https://accounts.spotify.com/api/token").respond(
            json={"access_token": "mock_token", "expires_in": 3600}
        )
        
        # Mock search
        search_route = respx.get("https://api.spotify.com/v1/search").respond(
            json={"albums": {"items": []}, "tracks": {"items": []}}
        )
        
        results = await spotify_client.search("query")
        
        assert search_route.called
        assert "albums" in results
