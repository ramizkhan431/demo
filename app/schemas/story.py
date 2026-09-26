from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional
from datetime import datetime
from app.schemas.author import AuthorResponse
from app.schemas.location import LocationSummaryResponse
from app.schemas.content import ContentResponse

class StoryContentLink(BaseModel):
    content_id: int
    ordering_index: int = 0

class StoryBase(BaseModel):
    name: str = Field(..., max_length=200)
    description: Optional[str] = None

class StoryCreate(StoryBase):
    author_id: int
    location_id: int
    content_links: List[StoryContentLink]

class StoryUpdate(StoryBase):
    name: Optional[str] = None
    author_id: Optional[int] = None
    location_id: Optional[int] = None
    content_links: Optional[List[StoryContentLink]] = None

class StoryFullResponse(StoryBase):
    id: int
    created_at: datetime
    updated_at: datetime
    # We use singular here as per the constraint, but models might allow multiple theoretically; 
    # we'll use first entry or just represent it cleanly
    authors: List[AuthorResponse]
    locations: List[LocationSummaryResponse]
    contents: List[ContentResponse]
    
    model_config = ConfigDict(from_attributes=True)
