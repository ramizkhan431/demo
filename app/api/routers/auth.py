from fastapi import APIRouter, Depends, HTTPException, status, Form, Body, Response, Request
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from jose import jwt, JWTError
from app.db.session import get_db
from app.repositories.user import user_repo
from app.services.auth import verify_password, create_access_token, create_refresh_token
from app.api.deps import get_current_active_user_no_totp
from app.models.user import User
from datetime import timedelta
from typing import Optional
from app.core.config import settings
import pyotp

router = APIRouter()

@router.post("/login/access-token")
async def login_access_token(
    response: Response,
    db: AsyncSession = Depends(get_db), 
    form_data: OAuth2PasswordRequestForm = Depends(),
    totp_code: Optional[str] = Form(None)
):
    user = await user_repo.get_by_email(db, email=form_data.username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password",
        )

    try:
        password_valid = verify_password(form_data.password, user.hashed_password)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc) or "Password length issue",
        )

    if not password_valid:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password",
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user",
        )

    # TOTP Validation
    if user.is_totp_enabled:
        if not totp_code:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="totp_required"
            )
        totp = pyotp.TOTP(user.totp_secret)
        if not totp.verify(totp_code):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid Google Authenticator code"
            )

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    refresh_token_expires = timedelta(minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        user.id, expires_delta=access_token_expires
    )
    refresh_token = create_refresh_token(
        user.id, expires_delta=refresh_token_expires
    )

    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        max_age=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        samesite="none",
        secure=False,  # Set to True in production with HTTPS
    )
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        max_age=settings.REFRESH_TOKEN_EXPIRE_MINUTES * 60,
        samesite="none",
        secure=False,  # Set to True in production with HTTPS
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "is_totp_enabled": user.is_totp_enabled
    }

@router.post("/logout")
async def logout(response: Response):
    response.delete_cookie("access_token")
    response.delete_cookie("refresh_token")
    return {"detail": "Successfully logged out"}

@router.post("/setup-totp")
async def setup_totp(
    current_user: User = Depends(get_current_active_user_no_totp),
    db: AsyncSession = Depends(get_db)
):
    if current_user.is_totp_enabled:
        raise HTTPException(status_code=400, detail="TOTP already enabled")
    
    # Merge the user object into this session before modifying
    current_user = await db.merge(current_user)
    
    secret = pyotp.random_base32()
    current_user.totp_secret = secret
    await db.commit()
    
    provisioning_uri = pyotp.totp.TOTP(secret).provisioning_uri(
        name=current_user.email,
        issuer_name="Wanderlust Admin"
    )
    return {"secret": secret, "provisioning_uri": provisioning_uri}

@router.post("/verify-totp")
async def verify_totp(
    totp_code: str = Form(...),
    current_user: User = Depends(get_current_active_user_no_totp),
    db: AsyncSession = Depends(get_db)
):
    if current_user.is_totp_enabled:
        raise HTTPException(status_code=400, detail="TOTP already enabled")
    
    if not current_user.totp_secret:
        raise HTTPException(status_code=400, detail="TOTP secret not setup")
    
    # Merge the user object into this session before modifying
    current_user = await db.merge(current_user)
        
    totp = pyotp.TOTP(current_user.totp_secret)
    if totp.verify(totp_code):
        current_user.is_totp_enabled = True
        await db.commit()
        return {"success": True, "detail": "Google Authenticator enabled successfully"}
    
    raise HTTPException(status_code=400, detail="Invalid verification code")

@router.post("/refresh-token")
async def refresh_access_token(
    request: Request,
    response: Response,
    refresh_token: str = Body(None),
    db: AsyncSession = Depends(get_db),
):
    if not refresh_token:
        refresh_token = request.cookies.get("refresh_token")
    
    if not refresh_token:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Refresh token missing",
        )
    try:
        payload = jwt.decode(refresh_token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        token_type: str = payload.get("token_type")
        user_id: str = payload.get("sub")
    except (JWTError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate refresh token",
        )

    if token_type != "refresh":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid token type")

    try:
        parsed_id = int(user_id)
    except (TypeError, ValueError):
        raise HTTPException(status_code=403, detail="Invalid user id in token")

    user = await user_repo.get(db, id=parsed_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if not user.is_active:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user")

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    refresh_token_expires = timedelta(minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(user.id, expires_delta=access_token_expires)
    new_refresh_token = create_refresh_token(user.id, expires_delta=refresh_token_expires)

    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        max_age=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        samesite="none",
        secure=False,
    )
    response.set_cookie(
        key="refresh_token",
        value=new_refresh_token,
        httponly=True,
        max_age=settings.REFRESH_TOKEN_EXPIRE_MINUTES * 60,
        samesite="none",
        secure=False,
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
    }
