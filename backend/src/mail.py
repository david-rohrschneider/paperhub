from logging import Logger

from pydantic import EmailStr
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

from src.config import CONFIG


SG = SendGridAPIClient(CONFIG.mail.sendgrid_api_key)
__logger = Logger(__name__)


def send_mail(to_emails: list[EmailStr], subject: str, html_content: str):
    """Send an email using the SendGrid API.

    Args:
        to_emails (list[str]): List of email addresses to send the email to.
        subject (str): Email subject.
        html_content (str): Email content in HTML format.
    """
    message = Mail(
        from_email=CONFIG.mail.sendgrid_from_email,
        to_emails=to_emails,
        subject=subject,
        html_content=html_content,
    )

    try:
        SG.send(message)
    except Exception as e:
        __logger.error(e)
