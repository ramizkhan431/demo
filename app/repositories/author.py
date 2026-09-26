from app.repositories.base import BaseRepository
from app.models.author import Author
from app.schemas.author import AuthorCreate, AuthorUpdate

class AuthorRepository(BaseRepository[Author, AuthorCreate, AuthorUpdate]):
    def __init__(self):
        super().__init__(Author)

author_repo = AuthorRepository()
