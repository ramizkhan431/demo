from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel, EmailStr
from app.services.email import send_contact_form_email
import logging

logger = logging.getLogger(__name__)
router = APIRouter()

class ContactFormRequest(BaseModel):
    email: EmailStr
    subject: str
    details: str

@router.post("/")
async def send_contact_message(payload: ContactFormRequest):
    try:
        await send_contact_form_email(
            sender_email=payload.email,
            subject=payload.subject,
            details=payload.details
        )
        return {"success": True, "message": "Email sent successfully!"}
    except Exception as e:
        logger.error(f"Contact email dispatch failed: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to send email: {str(e)}")
