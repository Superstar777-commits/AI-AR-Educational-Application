from fastapi import Header, HTTPException, Depends, status
from starlette.concurrency import run_in_threadpool
from typing import Optional, Dict, Any
from src.api.schemas.auth_schema import FirebaseUser
from src.services.user_service import UserService
from .common import get_user_service
from firebase_admin import auth

# Note: The Firebase Admin SDK is initialized in src/core/firebase_config.py
# which is imported in main.py, ensuring its ready.

async def verify_firebase_token(id_token: str = Header(alias="Authorization")) -> FirebaseUser:
    """
    Verifies a Firebase ID token sent in the Authorization header.
    Returns the authenticated user's details if valid
    """
    if not id_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authorization header is missing."
        )

    # extract the token (assuming "Bearer token_string")
    token_str = id_token.split("Bearer ")[-1]
    if token_str == id_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Authorization header format. Expected 'Bearer <token>'"
        )

    try:
        # Firebase Admin SDK's verify_id_token is a synchronous call
        # Must wrap it in run_in_threadpool to not block the event loop
        decoded_token = await run_in_threadpool(auth.verify_id_token, token_str)
        print(decoded_token)
        uid = decoded_token.get("uid")
        email = decoded_token.get("email")

        if not uid:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not retrieve user UID from token"
            )

        return FirebaseUser(uid=uid, email=email)
    except Exception as e:
        # Admin SDK raises various exceptions for invalid/expired tokens
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid or expired Firebase ID token: {e}"
        )

async def validate_current_user(
        firebase_user: FirebaseUser = Depends(verify_firebase_token),
        user_service: UserService = Depends(get_user_service)
) -> Optional[Dict[str, Any]]:
    """
    Dependency to validate that the authenticated user exists in the database and has the 'admin' role
    """
    # Look up the user in your database using the email from the Firebase token
    db_user = await user_service.get_user_by_email(firebase_user.email)

    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User not found in database"
        )
    print(db_user)
    return db_user
