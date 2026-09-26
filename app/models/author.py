from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import relationship
from app.db.base_class import Base, TimestampMixin

class Author(Base, TimestampMixin):
    __tablename__ = "author"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    bio = Column(Text, nullable=True)
    avatar_url = Column(String(255), nullable=True)

    # Relationship through association table
    stories = relationship("TravelStory", secondary="story_author", back_populates="authors")
