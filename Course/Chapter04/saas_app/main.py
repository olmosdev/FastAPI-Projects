from typing import Annotated
from contextlib import asynccontextmanager

from sqlalchemy.orm import Session
from fastapi import (
    FastAPI, 
    Depends, 
    HTTPException, 
    status
)

import api_key
import security
import premium_access
import rbac
import mfa
import github_login
import user_session
from responses import ResponseCreateUser, UserCreateBody, UserCreateResponse
from db_connection import get_engine, get_session
from models import Base
from operations import add_user
from third_party_login import resolve_github_token

# This context manager handles the application's lifecycle (startup and shutdown events).
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Connect to the database and create tables defined in 'models.py'
    # if they do not exist yet.
    Base.metadata.create_all(bind=get_engine())
    # Yield control to FastAPI to start handling requests.
    yield

# Initialize the main FastAPI application.
# We pass the 'lifespan' context manager to handle the startup logic.
app = FastAPI(
    title="Saas application", lifespan=lifespan,
)

@app.post(
    "/register/user",
    status_code=status.HTTP_201_CREATED,
    response_model=ResponseCreateUser,
    responses = {
        status.HTTP_409_CONFLICT: {
            "description": "The user already exists"
        }
    },
    tags=["User Registration with Basic Access"],
)
def register(
    user: UserCreateBody,
    session: Session = Depends(get_session),
) -> dict[str, UserCreateResponse]:
    user = add_user(
        session=session, **user.model_dump()
    )
    if not user:
        raise HTTPException(
            status.HTTP_409_CONFLICT,
            "username or email already exists",
        )
    user_response = UserCreateResponse(
        username=user.username, email=user.email
    )
    return {
        "message": "user created",
        "user": user_response,
    }    

app.include_router(security.router)
app.include_router(premium_access.router)
app.include_router(rbac.router)
app.include_router(github_login.router)
app.include_router(mfa.router)
app.include_router(user_session.router)
app.include_router(api_key.router)


@app.get(
    "/home",
    responses={
        status.HTTP_403_FORBIDDEN: {
            "description": "token not valid"
        }
    },
    tags=["Homepage"],
)
def homepage(
    user: UserCreateResponse = Depends(
        resolve_github_token
    ),
):
    return {"message": f"logged in {user.username} !"}


