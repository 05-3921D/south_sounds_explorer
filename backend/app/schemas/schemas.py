from typing import List, Optional
from pydantic import BaseModel

class DiscogsImage(BaseModel):
    uri: str
    height: int
    width: int

class DiscogsRelease(BaseModel):
    id: int
    title: str
    year: Optional[str] = None
    country: Optional[str] = None
    thumb: Optional[str] = None
    cover_image: Optional[str] = None
    style: List[str] = []
    genre: List[str] = []
    uri: Optional[str] = None
    label: Optional[List[str]] = None
    
class SearchResults(BaseModel):
    releases: List[DiscogsRelease]
