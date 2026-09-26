from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from app.db.session import get_db
from app.services.story import story_service
from app.schemas.story import StoryCreate, StoryFullResponse, StoryUpdate
from app.api.deps import get_current_superuser

router = APIRouter()

@router.get("/", response_model=List[StoryFullResponse])
async def list_stories(
    current_user=Depends(get_current_superuser),
    db: AsyncSession = Depends(get_db),
    search: Optional[str] = Query(None),
    author_id: Optional[int] = Query(None),
    location_id: Optional[int] = Query(None),
    skip: int = 0,
    limit: int = 10
):
    return await story_service.get_stories(
        db, search=search, author_id=author_id, location_id=location_id, skip=skip, limit=limit
    )

@router.post("/", response_model=StoryFullResponse)
async def create_story(
    current_user=Depends(get_current_superuser),
    *,
    db: AsyncSession = Depends(get_db),
    obj_in: StoryCreate
):
    return await story_service.create_story(db, obj_in=obj_in)

@router.get("/{id}", response_model=StoryFullResponse)
async def get_story_by_id(
    id: int,
    current_user=Depends(get_current_superuser),
    db: AsyncSession = Depends(get_db)
):
    story = await story_service.get_story_by_id(db, id=id)
    if not story:
        raise HTTPException(status_code=404, detail="Story not found")
    return story

@router.patch("/{id}", response_model=StoryFullResponse)
async def update_story(
    *,
    id: int,
    obj_in: StoryUpdate,
    current_user=Depends(get_current_superuser),
    db: AsyncSession = Depends(get_db)
):
    story = await story_service.update_story(db, id=id, obj_in=obj_in)
    if not story:
        raise HTTPException(status_code=404, detail="Story not found")
    return story

@router.delete("/{id}", response_model=StoryFullResponse)
async def delete_story(
    id: int,
    current_user=Depends(get_current_superuser),
    db: AsyncSession = Depends(get_db)
):
    story = await story_service.delete_story(db, id=id)
    if not story:
        raise HTTPException(status_code=404, detail="Story not found")
    return story