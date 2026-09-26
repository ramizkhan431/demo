from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.story import story_repo
from app.schemas.story import StoryCreate, StoryUpdate
from typing import List, Optional

class StoryService:
    async def get_stories(
        self, 
        db: AsyncSession, 
        *, 
        search: Optional[str] = None, 
        author_id: Optional[int] = None, 
        location_id: Optional[int] = None, 
        skip: int = 0, 
        limit: int = 10
    ):
        return await story_repo.search_and_filter(
            db, search=search, author_id=author_id, location_id=location_id, skip=skip, limit=limit
        )

    async def create_story(self, db: AsyncSession, *, obj_in: StoryCreate):
        return await story_repo.create_story(db, obj_in=obj_in)

    async def get_story_by_id(self, db: AsyncSession, id: int):
        return await story_repo.get(db, id=id)

    async def update_story(self, db: AsyncSession, *, id: int, obj_in: StoryUpdate):
        db_obj = await self.get_story_by_id(db, id=id)
        if not db_obj:
            return None
        return await story_repo.update_story(db, db_obj=db_obj, obj_in=obj_in)

    async def delete_story(self, db: AsyncSession, id: int):
        return await story_repo.remove(db, id=id)

story_service = StoryService()
