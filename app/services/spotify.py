import httpx
import base64
import time
from app.config import settings

#Maneja la autenticación automáticamente.
class SpotifyClient:
    def __init__(self, http_client: httpx.AsyncClient):
        self.auth_url = "https://accounts.spotify.com/api/token"
        self.base_url = "https://api.spotify.com/v1"
        self.access_token = None
        self.token_expiry = 0
        self.client = http_client

#Pide un token nuevo a Spotify solo si el anterior ya expiró
    async def _get_token(self):
        if self.access_token and time.time() < self.token_expiry:
            return self.access_token

        if not settings.is_spotify_configured:
            raise ValueError("Spotify credentials not configured")

        auth_str = f"{settings.SPOTIFY_CLIENT_ID}:{settings.SPOTIFY_CLIENT_SECRET}"
        b64_auth = base64.b64encode(auth_str.encode()).decode()

        headers = {
            "Authorization": f"Basic {b64_auth}",
            "Content-Type": "application/x-www-form-urlencoded"
        }
        data = {"grant_type": "client_credentials"}

        response = await self.client.post(self.auth_url, headers=headers, data=data)
        response.raise_for_status()
        token_data = response.json()
        
        self.access_token = token_data["access_token"]
        # Set de tiempo expiración
        self.token_expiry = time.time() + token_data["expires_in"] - 60
            
        return self.access_token

#Metodo para buscar álbumes y canciones. Crea solo un cliente http para todas las peticiones.
    async def search(self, query: str, type: str = "album,track", limit: int = 10):
        token = await self._get_token()
        headers = {"Authorization": f"Bearer {token}"}
        params = {
            "q": query,
            "type": type,
            "limit": limit
        }

        response = await self.client.get(f"{self.base_url}/search", headers=headers, params=params)
        response.raise_for_status()
        return response.json()
