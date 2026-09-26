from app.repositories.base import BaseRepository
from app.models.location import Location
from app.schemas.location import LocationCreate, LocationUpdate
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from typing import List, Any, Optional

class LocationRepository(BaseRepository[Location, LocationCreate, LocationUpdate]):
    def __init__(self):
        super().__init__(Location)

    async def create(self, db: AsyncSession, *, obj_in: LocationCreate) -> Location:
        obj_in_data = obj_in.model_dump()
        db_obj = self.model(**obj_in_data)
        db.add(db_obj)
        await db.commit()
        # Instead of just refresh, we fetch the complete object with eager loading
        result = await db.execute(
            select(Location)
            .filter(Location.id == db_obj.id)
            .options(selectinload(Location.children))
        )
        return result.scalars().first()

    async def get(self, db: AsyncSession, id: Any) -> Optional[Location]:
        result = await db.execute(
            select(Location)
            .filter(Location.id == id)
            .options(selectinload(Location.children))
        )
        return result.scalars().first()

    async def update(self, db: AsyncSession, *, db_obj: Location, obj_in: LocationUpdate) -> Location:
        update_data = obj_in.model_dump(exclude_unset=True)
        for field in ["name", "location_type", "description", "metadata_json", "parent_id"]:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        db.add(db_obj)
        await db.commit()
        # Fetch fresh with eager loading
        result = await db.execute(
            select(Location)
            .filter(Location.id == db_obj.id)
            .options(selectinload(Location.children))
        )
        return result.scalars().first()

    async def get_multi(self, db: AsyncSession, *, skip: int = 0, limit: int = 100, location_type: str = None) -> List[Location]:
        query = select(Location).options(selectinload(Location.children))
        if location_type:
            query = query.filter(Location.location_type == location_type)
        result = await db.execute(query.offset(skip).limit(limit))
        return result.scalars().all()

    async def get_tree(self, db: AsyncSession) -> List[Location]:
        # Eagerly load full hierarchy to avoid MissingGreenlet errors
        result = await db.execute(
            select(Location)
            .filter(Location.parent_id == None)
            .options(selectinload(Location.children).selectinload(Location.children))
        )
        return result.scalars().all()

location_repo = LocationRepository()
