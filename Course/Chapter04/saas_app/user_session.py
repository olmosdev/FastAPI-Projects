from fastapi import APIRouter, Depends, Response
from sqlalchemy.orm import Session

from db_connection import get_session
from operations import get_user
from rbac import get_current_user
from responses import UserCreateResponse

router = APIRouter(tags=["User Session Management"])


# Endpoint to simulate a login session by setting a cookie.
# Note: The user must already be authenticated via the 'get_current_user' dependency.
@router.post("/login")
async def login(
    response: Response,
    user: UserCreateResponse = Depends(
        get_current_user
    ),
    session: Session = Depends(get_session),
):
    # Retrieve the full user record from the database using the username from the token.
    user = get_user(session, user.username)

    # Set a cookie named "fakesession" with the user's ID.
    # In a real application, this would be a secure, signed session ID.
    response.set_cookie(
        key="fakesession", value=f"{user.id}"
    )
    return {"message": "User logged in successfully"}


# Endpoint to log out the user by clearing the session cookie.
@router.post("/logout")
async def logout(
    response: Response,
    user: UserCreateResponse = Depends(
        get_current_user
    ),
):
    # Delete the "fakesession" cookie to invalidate the session.
    response.delete_cookie(
        "fakesession"
    )  # Clear session data
    return {"message": "User logged out successfully"}