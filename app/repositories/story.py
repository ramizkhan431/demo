from app.repositories.base import BaseRepository
from app.models.story import TravelStory
from app.models.author import Author
from app.models.location import Location
from app.models.content import Content
from app.models.associations import StoryAuthor, StoryLocation, StoryContent
from app.schemas.story import StoryCreate, StoryUpdate
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from sqlalchemy import or_, cast, String
from typing import List, Optional

class StoryRepository(BaseRepository[TravelStory, StoryCreate, StoryUpdate]):
    def __init__(self):
        super().__init__(TravelStory)

    async def get_multi(self, db: AsyncSession, *, skip: int = 0, limit: int = 100) -> List[TravelStory]:
        query = select(TravelStory).options(
            selectinload(TravelStory.authors),
            selectinload(TravelStory.contents),
            selectinload(TravelStory.locations).selectinload(Location.children)
        ).offset(skip).limit(limit)
        result = await db.execute(query)
        return result.scalars().all()

    async def get(self, db: AsyncSession, id: int) -> Optional[TravelStory]:
        query = select(TravelStory).filter(TravelStory.id == id).options(
            selectinload(TravelStory.authors),
            selectinload(TravelStory.contents),
            selectinload(TravelStory.locations).selectinload(Location.children)
        )
        result = await db.execute(query)
        return result.scalars().first()

    async def create_story(self, db: AsyncSession, *, obj_in: StoryCreate) -> TravelStory:
        # Create core story
        story = TravelStory(
            name=obj_in.name,
            description=obj_in.description
        )
        db.add(story)
        await db.flush() # Gain story.id

        # Associate Author
        story_author = StoryAuthor(story_id=story.id, author_id=obj_in.author_id)
        db.add(story_author)

        # Associate Location
        story_location = StoryLocation(story_id=story.id, location_id=obj_in.location_id)
        db.add(story_location)

        # Associate Content with ordering
        for link in obj_in.content_links:
            story_content = StoryContent(
                story_id=story.id, 
                content_id=link.content_id, 
                ordering_index=link.ordering_index
            )
            db.add(story_content)

        await db.commit()
        # Fetch consistent full object with eager loading
        result = await db.execute(
            select(TravelStory).filter(TravelStory.id == story.id).options(
                selectinload(TravelStory.authors),
                selectinload(TravelStory.contents),
                selectinload(TravelStory.locations).selectinload(Location.children)
            )
        )
        return result.scalars().first()

    async def update_story(self, db: AsyncSession, *, db_obj: TravelStory, obj_in: StoryUpdate) -> TravelStory:
        update_data = obj_in.model_dump(exclude_unset=True)
        
        # Update basic fields
        if "name" in update_data:
            db_obj.name = update_data["name"]
        if "description" in update_data:
            db_obj.description = update_data["description"]

        # Update Author if provided
        if "author_id" in update_data:
            from sqlalchemy import delete
            await db.execute(delete(StoryAuthor).where(StoryAuthor.story_id == db_obj.id))
            new_author_link = StoryAuthor(story_id=db_obj.id, author_id=update_data["author_id"])
            db.add(new_author_link)

        # Update Location if provided
        if "location_id" in update_data:
            from sqlalchemy import delete
            await db.execute(delete(StoryLocation).where(StoryLocation.story_id == db_obj.id))
            new_location_link = StoryLocation(story_id=db_obj.id, location_id=update_data["location_id"])
            db.add(new_location_link)

        # Update Content Links if provided (handles reordering)
        if "content_links" in update_data:
            from sqlalchemy import delete
            await db.execute(delete(StoryContent).where(StoryContent.story_id == db_obj.id))
            for link in update_data["content_links"]:
                c_id = link["content_id"] if isinstance(link, dict) else link.content_id
                o_idx = link["ordering_index"] if isinstance(link, dict) else link.ordering_index
                new_content_link = StoryContent(
                    story_id=db_obj.id, 
                    content_id=c_id, 
                    ordering_index=o_idx
                )
                db.add(new_content_link)

        await db.commit()
        # Fetch consistent full object with eager loading
        result = await db.execute(
            select(TravelStory).filter(TravelStory.id == db_obj.id).options(
                selectinload(TravelStory.authors),
                selectinload(TravelStory.contents),
                selectinload(TravelStory.locations).selectinload(Location.children)
            )
        )
        return result.scalars().first()

    async def search_and_filter(
        self, 
        db: AsyncSession, 
        search: Optional[str] = None, 
        location_id: Optional[int] = None, 
        author_id: Optional[int] = None, 
        skip: int = 0, 
        limit: int = 10
    ) -> List[TravelStory]:
        query = select(TravelStory).options(
            selectinload(TravelStory.authors),
            selectinload(TravelStory.contents),
            selectinload(TravelStory.locations).selectinload(Location.children)
        )

        if search:
            search_term = f"%{search}%"
            query = query.filter(
                or_(
                    TravelStory.name.ilike(search_term),
                    TravelStory.description.ilike(search_term),
                    TravelStory.locations.any(
                        or_(
                            Location.name.ilike(search_term),
                            Location.parent.has(
                                or_(
                                    Location.name.ilike(search_term),
                                    Location.parent.has(
                                        Location.name.ilike(search_term)
                                    )
                                )
                            )
                        )
                    ),
                    TravelStory.contents.any(
                        or_(
                            Content.name.ilike(search_term),
                            cast(Content.metadata_json, String).ilike(search_term)
                        )
                    )
                )
            )

        if location_id:
            query = query.join(StoryLocation).filter(StoryLocation.location_id == location_id)

        if author_id:
            query = query.join(StoryAuthor).filter(StoryAuthor.author_id == author_id)

        query = query.offset(skip).limit(limit)
        result = await db.execute(query)
        return result.scalars().all()

story_repo = StoryRepository()
