import smtplib
from email.message import EmailMessage

from app.core.celery import celery
from app.core.config import settings


def get_email_message(email_to: str, code: int):
    email = EmailMessage()
    email['Subject'] = "FastAPI Flight"
    email['From'] = settings.SMTP_USER
    email['To'] = email_to
    email.set_content(f"Your verification code is <b>{code}</b>", subtype='html')
    return email


@celery.task
def send_code_email(email_to, code):
    email = get_email_message(email_to=email_to, code=code)
    with smtplib.SMTP_SSL(settings.SMTP_HOST, settings.SMTP_PORT) as server:
        server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
        server.send_message(email)
