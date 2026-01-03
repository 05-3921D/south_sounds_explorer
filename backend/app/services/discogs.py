import httpx
from typing import Dict, Any, List
from app.core.config import settings
import random

LATAM_COUNTRIES = [
    'Argentina', 'Bolivia', 'Brazil', 'Chile', 'Colombia', 'Costa Rica', 'Cuba',
    'Dominican Republic', 'Ecuador', 'El Salvador', 'Guatemala', 'Honduras', 
    'Mexico', 'Nicaragua', 'Panama', 'Paraguay', 'Peru', 'Puerto Rico', 
    'Uruguay', 'Venezuela'
]

ELECTRONIC_STYLES = [
    # Club/Classic
    "Techno", "House", "Deep House", "Progressive House", "Minimal", "Trance", 
    "Hard Trance", "Acid", "Electro", "Hard Techno", "Schranz",
    # Industrial/Hard
    "Industrial", "EBM", "Darkwave", "Noise", "Power Electronics", "Rhythmic Noise", 
    "IDM", "Breakcore",
    # Atmospheric
    "Ambient", "Drone", "Experimental", "Downtempo", "Illbient", "Berlin-School", "Leftfield",
    # Bass
    "Breakbeat", "Drum n Bass", "Jungle", "UK Garage", "Dubstep", "Deep Dubstep", "Grime",
    # Global
    "Tribal", "Latin", "Afrobeat", "Middle Eastern", "Dub", "Dub Techno"
]

def get_random_styles(limit: int = 8) -> List[str]:
    return random.sample(ELECTRONIC_STYLES, min(limit, len(ELECTRONIC_STYLES)))

def get_random_countries(limit: int = 6) -> List[str]:
    return random.sample(LATAM_COUNTRIES, min(limit, len(LATAM_COUNTRIES)))


class DiscogsClient:
    BASE_URL = "https://api.discogs.com"

    def __init__(self, client: httpx.AsyncClient = None):
        self.client = client or httpx.AsyncClient()
        self.headers = {
            "User-Agent": "SouthSoundsExplorer/0.1",
            "Authorization": f"Discogs key={settings.DISCOGS_CONSUMER_KEY}, secret={settings.DISCOGS_CONSUMER_SECRET}"
        }

    async def search(self, query: str = None, sort_by: str = "relevance", page: int = 1) -> Dict[str, Any]:
        """
        Search for electronic music releases in Latin America.
        sort_by: 'recent' (year desc) or 'best' (relevance)
        """
        params = {
            "type": "release", # Focus on specific releases
            "genre": "Electronic",
            "per_page": 100, # Fetch more to filter locally effectively
            "page": page,
        }
        
        if query:
            # Check if query is actually a known Style (Genre Mode)
            # Case insensitive check
            matching_style = next((s for s in ELECTRONIC_STYLES if s.lower() == query.lower()), None)
            
            if matching_style:
                # User clicked a Genre Chip or searched for a specific style.
                # To avoid getting 0 results due to API limits (Global top 100), 
                # we force a Country filter here, picking a random Latam country to "Example" the genre in the region.
                # This ensures we get Hits.
                random_country = random.choice(LATAM_COUNTRIES)
                params["country"] = random_country
                params["style"] = matching_style
                # We remove 'q' so it doesn't do a text search, but relies on strict Style filter
            else:
                # Normal Text Search (Artist, Album name)
                params["q"] = query
        else:
            # Suggestion Mode: Pick a random Latam country to ensure we get results from the region
            # without needing a keyword.
            random_country = random.choice(LATAM_COUNTRIES)
            params["country"] = random_country

        # Sorting logic
        if sort_by == "recent":
            params["sort"] = "year"
            params["sort_order"] = "desc"
        
        try:
            response = await self.client.get(
                f"{self.BASE_URL}/database/search", 
                params=params, 
                headers=self.headers
            )
            response.raise_for_status()
            data = response.json()
            
            filtered_results = self._filter_results(data.get("results", []))
            return {"results": filtered_results}
            
        except httpx.HTTPError as e:
            print(f"Discogs API Error: {e}")
            return {"results": []}

    def _filter_results(self, results: List[Dict]) -> List[Dict]:
        filtered = []
        for item in results:
            # 1. Country Filter
            country = item.get("country", "")
            if country not in LATAM_COUNTRIES:
                continue
                
            # 2. Style Filter
            # Item styles is a list, we check if ANY of the item's styles match our allowed list
            item_styles = item.get("style", [])
            if not any(style in ELECTRONIC_STYLES for style in item_styles):
                continue
                
            filtered.append(item)
            
        return filtered[:20] # Return top 20 after filtering
