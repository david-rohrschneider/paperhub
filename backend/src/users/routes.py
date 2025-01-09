from typing import Annotated

from fastapi import APIRouter, Depends, status

from src.auth.dependencies import current_user_id
from src.users.models import (
    User,
    UserCreateInput,
    UserEmailInput,
    UserUpdateInput,
)
from src.users import database as users_db


router = APIRouter(prefix="/users", tags=["User"])


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_user(body: UserCreateInput) -> User:
    """Create a new user. This supposes that the user is already authenticated by Firebase.

    Args:
        body (UserCreateInput): User registration fields.

    Returns:
        User: The created user.

    Raises:
        HTTPException: If the user already exists.
    """
    return await users_db.create(body)


@router.post("/request-verification-email", status_code=status.HTTP_201_CREATED)
def request_verification_email(body: UserEmailInput) -> None:
    """Request a new verification email given an email.

    Args:
        body (UserEmailInput): Request body with the email.

    Raises:
        HTTPException: If the user is already verified or the link generation fails.
    """
    users_db.request_verification_email(body.email)


@router.post("/request-password-reset-email", status_code=status.HTTP_201_CREATED)
def request_password_reset_email(body: UserEmailInput) -> None:
    """Request a new password reset email given an email.

    Args:
        body (UserEmailInput): Request body with the email.

    Raises:
        HTTPException: If the user is not found or the link generation fails.
    """
    users_db.request_password_reset_email(body.email)


@router.get("")
async def get_user(uid: Annotated[str, Depends(current_user_id)]) -> User:
    """Return the current user.

    Args:
        uid (str): Firebase user ID.

    Returns:
        User: The current user.

    Raises:
        HTTPException: If the user is not found.
    """
    return await users_db.get_by_id(uid)


@router.patch("")
async def update_user(
    body: UserUpdateInput, uid: Annotated[str, Depends(current_user_id)]
) -> User:
    """Update allowed user fields.

    Args:
        body (UserUpdateInput): User update fields.
        uid (str): Firebase user ID.

    Returns:
        User: The updated user.

    Raises:
        HTTPException: If the user is not found.
    """
    return await users_db.update(body, uid)


@router.delete("", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(uid: Annotated[str, Depends(current_user_id)]) -> None:
    """Delete current user.

    Args:
        uid (str): Firebase user ID.

    Raises:
        HTTPException: If the user is not found.
    """
    await users_db.delete(uid)
