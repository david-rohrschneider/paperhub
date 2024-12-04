from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from firebase_admin import auth

from src.auth.dependencies import current_user_id
from src.users.models import User, UserCreateInput, UserUpdateInput


router = APIRouter(prefix="/users", tags=["User"])


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_user(
    body: UserCreateInput, uid: Annotated[str, Depends(current_user_id)]
) -> User:
    """Create a new user. This supposes that the user is already authenticated by Firebase.

    Args:
        body (UserCreateInput): User registration fields.
        uid (str): Firebase user ID.

    Returns:
        User: The created user.

    Raises:
        HTTPException: If the user already exists.
    """
    user = await User.find_one(uid)

    if user is not None:
        raise HTTPException(status.HTTP_409_CONFLICT, "User already exists")

    user = await User(
        id=uid,
        email=body.email,
        first_name=body.first_name,
        last_name=body.last_name,
        affiliation=body.affiliation,
        title=body.title,
        bday=body.bday,
        bio=body.bio,
        links=body.links,
    ).create()

    return user


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
    user = await User.find_one(uid)

    if user is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "User not found")

    return user


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
    user = await User.find_one(uid)

    if user is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "User not found")

    if body.first_name is not None or body.last_name is not None:
        display_name = (
            f"{body.first_name or user.first_name} {body.last_name or user.last_name}"
        )
        auth.update_user(uid, display_name=display_name)

    user = await user.set(body.model_dump(exclude_unset=True))

    return user


@router.delete("", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(uid: Annotated[str, Depends(current_user_id)]) -> None:
    """Delete current user.

    Args:
        uid (str): Firebase user ID.

    Raises:
        HTTPException: If the user is not found.
    """
    user = await User.find_one(uid)

    if user is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "User not found")

    await user.delete()
    auth.delete_user(uid)
