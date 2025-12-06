import asyncio
import sys
import os
sys.path.append(os.getcwd())
from app.services.spotify import SpotifyClient

async def main():
    print("Testing Spotify Connection...")
    client = SpotifyClient()
    
    try:
        # Test basic search
        print("\nSearching for 'Soda Stereo'...")
        results = await client.search("Soda Stereo", limit=2)
        
        albums = results.get('albums', {}).get('items', [])
        print(f"\nFound {len(albums)} albums:")
        for album in albums:
            print(f"- {album['name']} ({album['release_date']})")
            
        print("\n✅ Spotify connection successful!")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("Please check your .env file credentials.")

if __name__ == "__main__":
    asyncio.run(main())
