import httpx
from typing import AsyncGenerator
from fastapi import Depends
from app.services.discogs import DiscogsClient

async def get_http_client() -> AsyncGenerator[httpx.AsyncClient, None]:
    async with httpx.AsyncClient() as client:
        yield client

async def get_discogs_service(client: httpx.AsyncClient = Depends(get_http_client)) -> DiscogsClient:
    return DiscogsClient(client)
