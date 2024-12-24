from typing import Annotated

from fastapi import APIRouter, Depends, status
from firebase_admin import auth

from src.auth.dependencies import current_user_id, current_user
from src.users.models import User, UserCreateInput, UserUpdateInput
from src.users import database as users_db


router = APIRouter(prefix="/users", tags=["User"])


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_user(
    body: UserCreateInput, user: Annotated[auth.UserRecord, Depends(current_user)]
) -> User:
    """Create a new user. This supposes that the user is already authenticated by Firebase.

    Args:
        body (UserCreateInput): User registration fields.
        user (auth.UserRecord): Firebase user record.

    Returns:
        User: The created user.

    Raises:
        HTTPException: If the user already exists.
    """
    return await users_db.create(body, user)


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
