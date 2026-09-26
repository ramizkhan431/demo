from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.db.session import get_db
from app.repositories.location import location_repo
from app.schemas.location import LocationCreate, LocationUpdate, LocationResponse
from app.api.deps import get_current_superuser

router = APIRouter()

@router.get("/", response_model=List[LocationResponse])
async def list_locations(
    current_user=Depends(get_current_superuser),
    db: AsyncSession = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    location_type: str = Query(None)
):
    return await location_repo.get_multi(db, skip=skip, limit=limit, location_type=location_type)

@router.get("/tree", response_model=List[LocationResponse])
async def get_location_tree(
    current_user=Depends(get_current_superuser),
    db: AsyncSession = Depends(get_db)
):
    return await location_repo.get_tree(db)

@router.post("/", response_model=LocationResponse)
async def create_location(
    current_user=Depends(get_current_superuser),
    *,
    db: AsyncSession = Depends(get_db),
    obj_in: LocationCreate
):
    return await location_repo.create(db, obj_in=obj_in)

@router.get("/{id}", response_model=LocationResponse)
async def get_location(
    id: int,
    current_user=Depends(get_current_superuser),
    db: AsyncSession = Depends(get_db)
):
    location = await location_repo.get(db, id=id)
    if not location:
        raise HTTPException(status_code=404, detail="Location not found")
    return location

@router.patch("/{id}", response_model=LocationResponse)
async def update_location(
    id: int,
    obj_in: LocationUpdate,
    current_user=Depends(get_current_superuser),
    db: AsyncSession = Depends(get_db)
):
    db_obj = await location_repo.get(db, id=id)
    if not db_obj:
        raise HTTPException(status_code=404, detail="Location not found")
    return await location_repo.update(db, db_obj=db_obj, obj_in=obj_in)

