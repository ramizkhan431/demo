from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
import json
from app.db.session import get_db
from app.repositories.content import content_repo
from app.schemas.content import ContentCreate, ContentUpdate, ContentResponse
from app.services.storage import storage_service
from app.models.content import ContentType
from app.api.deps import get_current_superuser

router = APIRouter()

@router.get("/", response_model=List[ContentResponse])
async def list_contents(
    current_user=Depends(get_current_superuser),
    db: AsyncSession = Depends(get_db),
    search: Optional[str] = Query(None),
    content_type: Optional[ContentType] = Query(None),
    carousel_type: Optional[str] = Query(None),
    skip: int = 0,
    limit: int = 1000
):
    return await content_repo.get_filtered_contents(
        db, search=search, content_type=content_type, carousel_type=carousel_type, skip=skip, limit=limit
    )

@router.post("/", response_model=ContentResponse)
async def create_content(
    current_user=Depends(get_current_superuser),
    *,
    db: AsyncSession = Depends(get_db),
    name: str = Form(...),
    description: Optional[str] = Form(None),
    metadata_json: Optional[str] = Form(None),
    content_type: ContentType = Form(...),
    video_url: Optional[str] = Form(None),
    carousel_type: Optional[str] = Form(None),
    image_file: Optional[UploadFile] = File(None)
):
    image_path = None
    if content_type == ContentType.IMAGE:
        if not image_file:
            raise HTTPException(status_code=400, detail="image_file required for IMAGE type")
        image_path = await storage_service.save_file(image_file)
    elif content_type == ContentType.VIDEO:
        if not video_url:
            raise HTTPException(status_code=400, detail="video_url required for VIDEO type")

    parsed_metadata = None
    if metadata_json:
        try:
            parsed_metadata = json.loads(metadata_json)
        except:
            raise HTTPException(status_code=400, detail="Invalid JSON in metadata_json")

    obj_in = ContentCreate(
        name=name,
        description=description,
        metadata_json=parsed_metadata,
        content_type=content_type,
        image_path=image_path,
        video_url=video_url,
        carousel_type=carousel_type
    )
    return await content_repo.create(db, obj_in=obj_in)

@router.get("/{id}", response_model=ContentResponse)
async def get_content(
    id: int,
    current_user=Depends(get_current_superuser),
    db: AsyncSession = Depends(get_db)
):
    content = await content_repo.get(db, id=id)
    if not content:
        raise HTTPException(status_code=404, detail="Content not found")
    return content

@router.patch("/{id}", response_model=ContentResponse)
async def update_content(
    *,
    id: int,
    current_user=Depends(get_current_superuser),
    db: AsyncSession = Depends(get_db),
    name: Optional[str] = Form(None),
    description: Optional[str] = Form(None),
    metadata_json: Optional[str] = Form(None),
    content_type: Optional[ContentType] = Form(None),
    video_url: Optional[str] = Form(None),
    carousel_type: Optional[str] = Form(None),
    image_file: Optional[UploadFile] = File(None)
):
    db_obj = await content_repo.get(db, id=id)
    if not db_obj:
        raise HTTPException(status_code=404, detail="Content not found")

    # Build update data conditionally
    update_data = {
        "name": name,
        "description": description,
        "metadata_json": None,
        "content_type": content_type,
        "carousel_type": carousel_type,
        "video_url": video_url,
    }

    # Only update image_path if a new image file is provided
    if image_file:
        image_path = await storage_service.save_file(image_file)
        update_data["image_path"] = image_path

    if metadata_json:
        try:
            update_data["metadata_json"] = json.loads(metadata_json)
        except:
            raise HTTPException(status_code=400, detail="Invalid JSON in metadata_json")

    obj_in = ContentUpdate(**update_data)
    return await content_repo.update(db, db_obj=db_obj, obj_in=obj_in)

@router.delete("/{id}", response_model=ContentResponse)
async def delete_content(
    id: int,
    current_user=Depends(get_current_superuser),
    db: AsyncSession = Depends(get_db)
):
    return await content_repo.remove(db, id=id)