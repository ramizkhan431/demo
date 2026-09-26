from sqlalchemy import Column, Integer, String, Text, ForeignKey, JSON
from sqlalchemy.orm import relationship, backref
from app.db.base_class import Base, TimestampMixin

class Location(Base, TimestampMixin):
    __tablename__ = "location"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    location_type = Column(String(50), nullable=True) # e.g., 'country', 'city', 'poi'
    description = Column(Text, nullable=True)
    metadata_json = Column(JSON, nullable=True) # JSONB in Postgres
    
    # Hierarchical support
    parent_id = Column(Integer, ForeignKey("location.id", ondelete="CASCADE"), nullable=True)
    children = relationship("Location", backref=backref("parent", remote_side=[id]), cascade="all, delete-orphan", lazy="selectin")

    # Relationship through association table
    stories = relationship("TravelStory", secondary="story_location", back_populates="locations")
