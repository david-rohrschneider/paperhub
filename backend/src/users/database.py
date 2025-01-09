import logging

from fastapi import HTTPException, status
from firebase_admin import auth

from src.libraries.models import Library
from src.mail import (
    EMAIL_VERIFICATION_SUBJECT,
    EMAIL_VERIFICATION_TEMPLATE,
    PASSWORD_RESET_SUBJECT,
    PASSWORD_RESET_TEMPLATE,
    send_mail,
)
from src.users.models import User, UserCreateInput, UserUpdateInput
from src.config import CONFIG


__logger = logging.getLogger(__name__)


async def create(body: UserCreateInput) -> User:
    try:
        firebase_user: auth.UserRecord = auth.create_user(
            display_name=f"{body.first_name} {body.last_name}",
            email=body.email,
            password=body.password,
            email_verified=False,
            disabled=False,
        )

    except auth.EmailAlreadyExistsError:
        raise HTTPException(status.HTTP_409_CONFLICT, "Email already exists")

    except Exception:
        __logger.error(f"Firebase user creation failed: {e}")
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR)

    try:
        verification_link: str = auth.generate_email_verification_link(
            firebase_user.email
        )
    except Exception as e:
        __logger.error(f"Failed to generate email verification link: {e}")
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR)

    send_mail(
        [firebase_user.email],
        EMAIL_VERIFICATION_SUBJECT,
        EMAIL_VERIFICATION_TEMPLATE.format(
            username=body.first_name,
            verification_url=verification_link,
        ),
    )

    user = await User(
        id=firebase_user.uid,
        email=firebase_user.email,
        first_name=body.first_name,
        last_name=body.last_name,
        fields=body.fields,
        affiliation=body.affiliation,
        title=body.title,
        bday=body.bday,
        bio=body.bio,
        refs=body.refs,
    ).create()

    await Library(
        user_id=user.id, title="Reading List", default=True, private=True
    ).create()

    return user


def request_verification_email(email: str) -> None:
    try:
        verification_link: str = auth.generate_email_verification_link(email)

    except (auth.UserNotFoundError, auth.EmailNotFoundError):
        raise HTTPException(status.HTTP_404_NOT_FOUND, "User not found")

    except auth.TooManyAttemptsTryLaterError:
        raise HTTPException(
            status.HTTP_429_TOO_MANY_REQUESTS, "Too many attempts, try again later"
        )

    except Exception as e:
        __logger.error(f"Failed to generate email verification link: {e}")
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR)

    send_mail(
        [email],
        EMAIL_VERIFICATION_SUBJECT,
        EMAIL_VERIFICATION_TEMPLATE.format(
            verification_url=verification_link,
        ),
    )


def request_password_reset_email(email: str) -> None:
    try:
        password_reset_link = auth.generate_password_reset_link(email)

    except (auth.UserNotFoundError, auth.EmailNotFoundError):
        raise HTTPException(status.HTTP_404_NOT_FOUND, "User not found")

    except auth.TooManyAttemptsTryLaterError:
        raise HTTPException(
            status.HTTP_429_TOO_MANY_REQUESTS, "Too many attempts, try again later"
        )

    except Exception as e:
        __logger.error(f"Failed to generate password reset link: {e}")
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR)

    send_mail(
        [email],
        PASSWORD_RESET_SUBJECT,
        PASSWORD_RESET_TEMPLATE.format(
            password_reset_url=password_reset_link,
        ),
    )


async def get_by_id(uid: str) -> User:
    user = await User.get(uid)

    if user is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "User not found")

    return user


async def update(body: UserUpdateInput, uid: str) -> User:
    user = await User.get(uid)

    if user is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "User not found")

    if body.first_name is not None or body.last_name is not None:
        display_name = (
            f"{body.first_name or user.first_name} {body.last_name or user.last_name}"
        )
        auth.update_user(uid, display_name=display_name)

    user = await user.set(body.model_dump(exclude_unset=True))

    return user


async def delete(uid: str):
    user = await User.get(uid)

    if user is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "User not found")

    await user.delete()
    auth.delete_user(uid)
