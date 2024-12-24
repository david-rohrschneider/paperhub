from fastapi import HTTPException, status
from firebase_admin import auth

from src.libraries.models import Library
from src.users.models import User, UserCreateInput, UserUpdateInput


async def create(body: UserCreateInput, firebase_user: auth.UserRecord) -> User:
    db_user = await User.get(firebase_user.uid)

    if db_user is not None:
        raise HTTPException(status.HTTP_409_CONFLICT, "User already exists")

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

    # TODO: Implement Firebase User Creation

    await Library(user_id=user.id, title="Default", default=True, private=True).create()

    return user


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
