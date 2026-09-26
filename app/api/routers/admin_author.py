from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.db.session import get_db
from app.repositories.author import author_repo
from app.schemas.author import AuthorCreate, AuthorUpdate, AuthorResponse
from app.api.deps import get_current_superuser

router = APIRouter()

@router.get("/", response_model=List[AuthorResponse])
async def list_authors(
    current_user=Depends(get_current_superuser),
    db: AsyncSession = Depends(get_db),
    skip: int = 0,
    limit: int = 100
):
    return await author_repo.get_multi(db, skip=skip, limit=limit)

@router.post("/", response_model=AuthorResponse)
async def create_author(
    current_user=Depends(get_current_superuser),
    *,
    db: AsyncSession = Depends(get_db),
    obj_in: AuthorCreate
):
    return await author_repo.create(db, obj_in=obj_in)

@router.get("/{id}", response_model=AuthorResponse)
async def get_author(
    id: int,
    current_user=Depends(get_current_superuser),
    db: AsyncSession = Depends(get_db)
):
    author = await author_repo.get(db, id=id)
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")
    return author

@router.patch("/{id}", response_model=AuthorResponse)
async def update_author(
    id: int,
    obj_in: AuthorUpdate,
    current_user=Depends(get_current_superuser),
    db: AsyncSession = Depends(get_db)
):
    db_obj = await author_repo.get(db, id=id)
    if not db_obj:
        raise HTTPException(status_code=404, detail="Author not found")
    return await author_repo.update(db, db_obj=db_obj, obj_in=obj_in)

@router.delete("/{id}", response_model=AuthorResponse)
async def delete_author(
    id: int,
    current_user=Depends(get_current_superuser),
    db: AsyncSession = Depends(get_db)
):
    return await author_repo.remove(db, id=id)