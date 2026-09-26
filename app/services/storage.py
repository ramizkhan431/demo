import os
from fastapi import UploadFile
from app.core.config import settings
import uuid

class StorageService:
    def __init__(self):
        if settings.STORAGE_TYPE == "local" and not os.path.exists(settings.STORAGE_PATH):
            os.makedirs(settings.STORAGE_PATH)

    async def save_file(self, file: UploadFile) -> str:
        # Simple local storage implementation
        filename = f"{uuid.uuid4()}_{file.filename}"
        file_path = os.path.join(settings.STORAGE_PATH, filename)
        
        with open(file_path, "wb") as f:
            f.write(await file.read())
        
        # Normalize path to use forward slashes for URLs (important for Windows)
        return file_path.replace("\\", "/")

storage_service = StorageService()
