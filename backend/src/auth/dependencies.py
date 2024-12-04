from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from firebase_admin import auth


def current_user_id(
    cred: HTTPAuthorizationCredentials = Depends(HTTPBearer(auto_error=False)),
) -> str:
    """Validates and decodes a users access token.

    Args:
        cred (HTTPAuthorizationCredentials): The users access token.

    Returns:
        str: The user ID.

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

    return decoded_token["uid"]
