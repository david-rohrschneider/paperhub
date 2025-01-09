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
        to_emails (list[EmailStr]): List of email addresses to send the email to.
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


EMAIL_VERIFICATION_SUBJECT = "Verify your email address for paperhub"
EMAIL_VERIFICATION_TEMPLATE = """
<h1>Verify your email address</h1>
<p>Dear,</p>
<p>Thank you for signing up to paperhub.</p>
<p>Please click the link below to verify your email address:</p>
<br>
<a href="{verification_url}">{verification_url}</a>
<br>
<p>If you didn't sign up to our service, please ignore this email.</p>
<p>Best regards,</p>
<p>The paperhub team</p>
"""

PASSWORD_RESET_SUBJECT = "Reset your password for paperhub"
PASSWORD_RESET_TEMPLATE = """
<h1>Reset your password</h1>
<p>Dear,</p>
<p>We received a request to reset your password.</p>
<p>Please click the link below to reset your password:</p>
<br>
<a href="{password_reset_link}">{password_reset_link}</a>
<br>
<p>If you didn't request a password reset, please ignore this email.</p>
<p>Best regards,</p>
<p>The paperhub team</p>
"""
