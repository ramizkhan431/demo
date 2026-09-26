from pydantic import BaseModel, Field, ConfigDict, model_validator
from typing import Optional, Any
from datetime import datetime
from app.models.content import ContentType

class ContentBase(BaseModel):
    name: str = Field(..., max_length=100)
    description: Optional[str] = None
    metadata_json: Optional[Any] = None
    content_type: ContentType
    carousel_type: Optional[str] = None

class ContentCreate(ContentBase):
    image_path: Optional[str] = None
    video_url: Optional[str] = None

    @model_validator(mode='after')
    def validate_content(cls, values):
        if values.content_type == ContentType.IMAGE and not values.image_path:
            raise ValueError("image_path is required for IMAGE content")
        if values.content_type == ContentType.VIDEO and not values.video_url:
            raise ValueError("video_url is required for VIDEO content")
        return values

class ContentUpdate(ContentBase):
    name: Optional[str] = None
    content_type: Optional[ContentType] = None
    image_path: Optional[str] = None
    video_url: Optional[str] = None
    carousel_type: Optional[str] = None

class ContentResponse(ContentBase):
    id: int
    image_path: Optional[str] = None
    video_url: Optional[str] = None
    carousel_type: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)
