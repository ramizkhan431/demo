from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from app.db.session import get_db
from app.repositories.content import content_repo
from app.schemas.content import ContentResponse
from app.models.content import ContentType

router = APIRouter()

@router.get("/", response_model=List[ContentResponse])
async def list_contents(
    db: AsyncSession = Depends(get_db),
    search: Optional[str] = Query(None),
    content_type: Optional[ContentType] = Query(None),
    carousel_type: Optional[str] = Query(None),
    is_carousel: Optional[bool] = Query(None),
    random: bool = Query(False),
    skip: int = 0,
    limit: int = 100
):
    return await content_repo.get_filtered_contents(
        db, search=search, content_type=content_type, carousel_type=carousel_type, is_carousel=is_carousel, random=random, skip=skip, limit=limit
    )

@router.get("/{id}", response_model=ContentResponse)
async def get_content(
    id: int,
    db: AsyncSession = Depends(get_db)
):
    content = await content_repo.get(db, id=id)
    if not content:
        raise HTTPException(status_code=404, detail="Content not found")
    return content