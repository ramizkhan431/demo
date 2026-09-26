from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from typing import Optional

class AuthorBase(BaseModel):
    name: str = Field(..., max_length=100)
    bio: Optional[str] = None
    avatar_url: Optional[str] = None

class AuthorCreate(AuthorBase):
    pass

class AuthorUpdate(AuthorBase):
    name: Optional[str] = None

class AuthorResponse(AuthorBase):
    id: int
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)
