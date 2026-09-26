from fastapi import APIRouter
from app.api.routers import admin_author, admin_location, admin_content, admin_story
from app.api.routers import user_content, user_story, user_location, contact
from app.api.routers import auth

api_router = APIRouter()

# Auth routes (public for login)
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])

# Contact route (public email endpoint)
api_router.include_router(contact.router, prefix="/contact", tags=["contact"])

# Admin routes (require JWT + superuser)
api_router.include_router(admin_author.router, prefix="/admin/authors", tags=["admin-authors"])
api_router.include_router(admin_location.router, prefix="/admin/locations", tags=["admin-locations"])
api_router.include_router(admin_content.router, prefix="/admin/contents", tags=["admin-contents"])
api_router.include_router(admin_story.router, prefix="/admin/stories", tags=["admin-stories"])

# User routes (public GET only, require secret key)
api_router.include_router(user_content.router, prefix="/user/contents", tags=["user-contents"])
api_router.include_router(user_story.router, prefix="/user/stories", tags=["user-stories"])
api_router.include_router(user_location.router, prefix="/user/locations", tags=["user-locations"])
