import os

import httpx
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2
from sqlalchemy.orm import Session
from dotenv import load_dotenv

from db_connection import get_session
from models import User
from operations import get_user

# Load environment variables from a .env file.
load_dotenv()

# Retrieve GitHub OAuth credentials and configuration from environment variables.
GITHUB_CLIENT_ID = os.getenv("GITHUB_CLIENT_ID")
GITHUB_CLIENT_SECRET = os.getenv("GITHUB_CLIENT_SECRET")
# The URL where GitHub will redirect back to after authorization.
GITHUB_REDIRECT_URI = (
    "http://localhost:8000/github/auth/token"
)
# The GitHub URL to redirect users to for authorization.
GITHUB_AUTHORIZATION_URL = (
    "https://github.com/login/oauth/authorize"
)

# Dependency to resolve a user from a GitHub access token.
def resolve_github_token(
    # Depends(OAuth2()) is used here to extract the token from the request.
    access_token: str = Depends(OAuth2()),
    session: Session = Depends(get_session),
) -> User:
    # Query the GitHub API to get user details using the provided access token.
    user_response = httpx.get(
        "https://api.github.com/user",
        headers={"Authorization": access_token},
    ).json()
    # Attempt to find the user in the local database by their GitHub username (login).
    username = user_response.get("login", " ")
    user = get_user(session, username)
    # If not found by username, try to find the user by their email address.
    if not user:
        email = user_response.get("email", " ")
        user = get_user(session, email)
    # Process user_response to log
    # the user in or create a new account

    # If the user is still not found in the local DB, raise a 403 Forbidden error.
    if not user:
        raise HTTPException(
            status_code=403, detail="Token not valid"
        )
    return user
