import asyncio
import sys
import os
# Ensure backend is in path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'backend'))

from app.services.discogs import DiscogsClient
from app.core.config import settings

async def main():
    print(f"Testing Discogs Connection with key ending in ...{settings.DISCOGS_CONSUMER_KEY[-4:]}")
    
    client = DiscogsClient()
    
    # Test 1: Search for known Latam Electronic artist
    query = "Ricardo Villalobos"
    print(f"\n--- Probando búsqueda: '{query}' (Best Match) ---")
    data = await client.search(query, sort_by="best")
    results = data.get("results", [])
    
    if not results:
        print("❌ No se encontraron resultados (puede ser por filtros estrictos).")
    else:
        print(f"✅ Se encontraron {len(results)} resultados filtrados.")
        for item in results[:3]:
            print(f"  - [{item.get('year')}] {item.get('title')} ({item.get('country')}) - {item.get('style')}")

    # Test 2: Recent
    print(f"\n--- Probando búsqueda: '{query}' (Más Recientes) ---")
    data = await client.search(query, sort_by="recent")
    results = data.get("results", [])
    if results:
        top_item = results[0]
        print(f"  Top Recent: [{top_item.get('year')}] {top_item.get('title')}")

if __name__ == "__main__":
    asyncio.run(main())
