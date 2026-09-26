import smtplib
import ssl
import asyncio
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from app.core.config import settings

logger = logging.getLogger(__name__)

def send_email_sync(to_email: str, subject: str, body_text: str, reply_to: str = None) -> bool:
    smtp_host = settings.SMTP_HOST
    smtp_port = settings.SMTP_PORT
    smtp_username = settings.SMTP_USERNAME
    smtp_password = settings.SMTP_PASSWORD
    use_ssl = settings.SMTP_USE_SSL
    from_address = settings.MAIL_FROM_ADDRESS or smtp_username or "info@travelchronicles.net"
    from_name = settings.MAIL_FROM_NAME or "travelchronicles"

    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = f"{from_name} <{from_address}>"
    msg["To"] = to_email
    if reply_to:
        msg["Reply-To"] = reply_to

    msg.attach(MIMEText(body_text, "plain"))

    try:
        if use_ssl:
            context = ssl.create_default_context()
            with smtplib.SMTP_SSL(smtp_host, smtp_port, context=context, timeout=20) as server:
                server.login(smtp_username, smtp_password)
                server.send_message(msg)
        else:
            with smtplib.SMTP(smtp_host, smtp_port, timeout=20) as server:
                server.starttls()
                server.login(smtp_username, smtp_password)
                server.send_message(msg)
        logger.info(f"Successfully sent email to {to_email}")
        return True
    except Exception as e:
        logger.error(f"Failed to send email to {to_email}: {e}")
        raise e

async def send_contact_form_email(sender_email: str, subject: str, details: str):
    to_email = settings.MAIL_TO_ADDRESS or "info@travelchronicles.net"
    email_subject = f"[TravelChronicles Contact] {subject}"
    body = (
        f"New Contact Form Submission from TravelChronicles Front Page\n\n"
        f"Sender Email: {sender_email}\n"
        f"Subject: {subject}\n\n"
        f"Details:\n"
        f"{details}\n\n"
        f"---\n"
        f"Sent via TravelChronicles Contact Desk"
    )
    return await asyncio.to_thread(send_email_sync, to_email, email_subject, body, sender_email)
