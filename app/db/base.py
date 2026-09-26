# Import all models here so that Alembic can discover them
from app.db.base_class import Base
from app.models.author import Author
from app.models.location import Location
from app.models.content import Content, ContentType
from app.models.story import TravelStory
from app.models.associations import StoryAuthor, StoryLocation, StoryContent
from app.models.user import User
