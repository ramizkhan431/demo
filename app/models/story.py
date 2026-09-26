from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import relationship
from app.db.base_class import Base, TimestampMixin

class TravelStory(Base, TimestampMixin):
    __tablename__ = "travel_story"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), index=True, nullable=False)
    description = Column(Text, nullable=True)

    # Relationships
    # authors relationship through story_author association
    authors = relationship("Author", secondary="story_author", back_populates="stories", lazy="selectin")
    
    # locations relationship through story_location association
    locations = relationship("Location", secondary="story_location", back_populates="stories", lazy="selectin")
    
    # contents relationship through story_content association with ordering
    contents = relationship(
        "Content", 
        secondary="story_content", 
        back_populates="stories", 
        lazy="selectin",
        order_by="StoryContent.ordering_index"
    )
