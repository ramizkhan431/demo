from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.db.session import get_db
from app.repositories.location import location_repo
from app.schemas.location import LocationResponse

router = APIRouter()

@router.get("/", response_model=List[LocationResponse])
async def list_locations(
    db: AsyncSession = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    location_type: str = Query(None)
):
    return await location_repo.get_multi(db, skip=skip, limit=limit, location_type=location_type)

@router.get("/tree", response_model=List[LocationResponse])
async def get_location_tree(
    db: AsyncSession = Depends(get_db)
):
    return await location_repo.get_tree(db)

@router.get("/{id}", response_model=LocationResponse)
async def get_location(
    id: int,
    db: AsyncSession = Depends(get_db)
):
    location = await location_repo.get(db, id=id)
    if not location:
        raise HTTPException(status_code=404, detail="Location not found")
    return location