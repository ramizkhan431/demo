from sqlalchemy import Column, Integer, ForeignKey, UniqueConstraint
from app.db.base_class import Base

# Many-to-one (One author per story)
class StoryAuthor(Base):
    __tablename__ = "story_author"
    story_id = Column(Integer, ForeignKey("travel_story.id", ondelete="CASCADE"), primary_key=True)
    author_id = Column(Integer, ForeignKey("author.id", ondelete="CASCADE"), primary_key=True)
    
    # Ensure one author per story
    __table_args__ = (UniqueConstraint('story_id', name='uq_story_author'),)

# Many-to-one (One location per story)
class StoryLocation(Base):
    __tablename__ = "story_location"
    story_id = Column(Integer, ForeignKey("travel_story.id", ondelete="CASCADE"), primary_key=True)
    location_id = Column(Integer, ForeignKey("location.id", ondelete="CASCADE"), primary_key=True)
    
    # Ensure one location per story
    __table_args__ = (UniqueConstraint('story_id', name='uq_story_location'),)

# Many-to-many with ordering
class StoryContent(Base):
    __tablename__ = "story_content"
    story_id = Column(Integer, ForeignKey("travel_story.id", ondelete="CASCADE"), primary_key=True)
    content_id = Column(Integer, ForeignKey("content.id", ondelete="CASCADE"), primary_key=True)
    ordering_index = Column(Integer, default=0, nullable=False)
