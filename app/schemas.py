from pydantic import BaseModel
from typing import List, Optional

#Esquema para ordenar la información de la API de Spotify
class Image(BaseModel):
    url: str
    height: Optional[int] = None
    width: Optional[int] = None

class Artist(BaseModel):
    id: str
    name: str

class Album(BaseModel):
    id: str
    name: str
    artists: List[Artist]
    images: List[Image]
    release_date: str
    total_tracks: int
    external_urls: dict

class Track(BaseModel):
    id: str
    name: str
    artists: List[Artist]
    album: Album
    duration_ms: int
    popularity: int
    external_urls: dict

class SearchResults(BaseModel):
    albums: List[Album]
    tracks: List[Track]
