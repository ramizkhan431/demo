from sqlalchemy import Column, Integer, String, Text, Enum, JSON
from sqlalchemy.orm import relationship
import enum
from app.db.base_class import Base, TimestampMixin

class ContentType(str, enum.Enum):
    IMAGE = "IMAGE"
    VIDEO = "VIDEO"

class Content(Base, TimestampMixin):
    __tablename__ = "content"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    metadata_json = Column(JSON, nullable=True)
    content_type = Column(Enum(ContentType, name="content_type_enum"), nullable=False)
    image_path = Column(String(255), nullable=True)
    video_url = Column(String(255), nullable=True)
    carousel_type = Column(String(100), nullable=True)

    # Relationship through association table
    stories = relationship("TravelStory", secondary="story_content", back_populates="contents")
