from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from firebase_admin import auth


def current_user(
    cred: HTTPAuthorizationCredentials = Depends(HTTPBearer(auto_error=False)),
) -> auth.UserRecord:
    """Validates and decodes a users access token.

    Args:
        cred (HTTPAuthorizationCredentials): The users access token.

    Returns:
        auth.UserRecord: The user record.

    Raises:
        HTTPException: If the user is not authenticated or the token is invalid.
    """

    if cred is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Bearer authentication required",
        )

    try:
        decoded_token = auth.verify_id_token(cred.credentials, clock_skew_seconds=10)
    except Exception as err:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid authentication credentials. {err}",
        )

    if decoded_token["email_verified"] == False:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email is not verified",
        )

    decoded_token["localId"] = decoded_token["uid"]

    return auth.UserRecord(decoded_token)


def current_user_id(
    user: auth.UserRecord = Depends(current_user),
) -> str:
    """Get the current users ID.

    Args:
        user (auth.UserRecord): The current user.

    Returns:
        str: The users ID.
    """

    return user.uid
