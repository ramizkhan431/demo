from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List, Any
from datetime import datetime

class LocationBase(BaseModel):
    name: str = Field(..., max_length=100)
    location_type: Optional[str] = None
    description: Optional[str] = None
    metadata_json: Optional[Any] = None
    parent_id: Optional[int] = None

class LocationCreate(LocationBase):
    pass

class LocationUpdate(LocationBase):
    name: Optional[str] = None

class LocationSummaryResponse(LocationBase):
    id: int
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

class LocationResponse(LocationSummaryResponse):
    children: List['LocationResponse'] = []
    
    model_config = ConfigDict(from_attributes=True)

# Important for circular dependency in type hints
LocationResponse.model_rebuild()
