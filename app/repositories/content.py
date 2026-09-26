from app.repositories.base import BaseRepository
from app.models.content import Content
from app.schemas.content import ContentCreate, ContentUpdate

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import Optional, List

from app.models.content import Content, ContentType

from sqlalchemy import func, or_

class ContentRepository(BaseRepository[Content, ContentCreate, ContentUpdate]):
    def __init__(self):
        super().__init__(Content)

    async def get_filtered_contents(
        self,
        db: AsyncSession,
        *,
        search: Optional[str] = None,
        content_type: Optional[ContentType] = None,
        carousel_type: Optional[str] = None,
        is_carousel: Optional[bool] = None,
        random: bool = False,
        skip: int = 0,
        limit: int = 1000
    ) -> List[Content]:
        query = select(self.model)
        if search:
            query = query.filter(
                (self.model.name.ilike(f"%{search}%")) | 
                (self.model.description.ilike(f"%{search}%"))
            )
        if content_type:
            query = query.filter(self.model.content_type == content_type)
        if carousel_type:
            query = query.filter(self.model.carousel_type == carousel_type)
        elif is_carousel is True:
            query = query.filter(self.model.carousel_type.isnot(None), self.model.carousel_type != "")
        elif is_carousel is False:
            query = query.filter(or_(self.model.carousel_type.is_(None), self.model.carousel_type == ""))
        
        if random:
            query = query.order_by(func.random())
        
        result = await db.execute(query.offset(skip).limit(limit))
        return result.scalars().all()

content_repo = ContentRepository()
