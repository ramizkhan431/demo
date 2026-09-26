from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os
from app.api.api_v1 import api_router
from app.core.config import settings

# Ensure uploads directory exists (local storage)
if not os.path.exists("uploads"):
    os.makedirs("uploads")

app = FastAPI(
    title="Travel Blog API",
    description="A production-ready travel storytelling platform.",
    version="1.0.0",
)

# Custom Middleware to protect from outside access (enabled via INTERNAL_API_KEY)
@app.middleware("http")
async def verify_internal_secret(request: Request, call_next):
    # Allow static files in uploads directory to be publicly accessible
    if request.url.path.startswith("/uploads/"):
        return await call_next(request)
    
    # Allow user routes to pass through with secret key verification
    if request.url.path.startswith("/api/v1/user/"):
        if request.headers.get("X-Internal-Secret") != settings.INTERNAL_API_KEY:
            return JSONResponse(
                status_code=403,
                content={"detail": "Forbidden: Direct API access is not allowed."}
            )
    
    return await call_next(request)

# Set up CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include V1 API
app.include_router(api_router, prefix="/api/v1")

# Serve static files from the uploads directory
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

@app.get("/")
async def root():
    return {"message": "Welcome to the Travel Blog API!"}
