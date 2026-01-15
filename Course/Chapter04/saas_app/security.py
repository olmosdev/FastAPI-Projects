from datetime import datetime, timedelta

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
)
from fastapi.security import (
    OAuth2PasswordRequestForm,
    OAuth2PasswordBearer,
)
from pydantic import BaseModel
from sqlalchemy.orm import Session
from email_validator import (
    validate_email,
    EmailNotValidError,
)
from jose import jwt, JWTError

from db_connection import get_session
from models import User
from operations import get_user, pwd_context

def authenticate_user(
    session: Session,
    username_or_email: str,
    password: str,
) -> User | None:
    # Check if the input is a valid email address.
    # If it is, we will query by the 'email' column.
    # If not (EmailNotValidError), we assume it is a 'username'.
    try:
        validate_email(username_or_email)
        query_filter = User.email
    except EmailNotValidError:
        query_filter = User.username

    # Query the database for a user matching the filter (email or username).
    # .first() returns the user object or None if not found.
    user = (
        session.query(User)
        .filter(query_filter == username_or_email)
        .first()
    )

    # Verify the user exists and the password is correct.
    # pwd_context.verify() compares the plain text password with the hashed password in the DB.
    # It handles the hashing algorithm (bcrypt) automatically.
    if not user or not pwd_context.verify(
        password, user.hashed_password
    ):
        return
    # Return the authenticated user object.
    return user

# Secret key used to sign the JWT. In production, this should be stored in environment variables.
SECRET_KEY = "a_very_secret_key"
# Algorithm used for signing the token (HMAC SHA-256).
ALGORITHM = "HS256"
# Token validity duration in minutes.
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: dict) -> str:
    # Create a copy of the data to avoid mutating the original dictionary.
    to_encode = data.copy()
    # Calculate the expiration time based on the current UTC time.
    expire = datetime.utcnow() + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )
    # Add the 'exp' (expiration) claim to the payload. This is a standard JWT claim.
    to_encode.update({"exp": expire})
    # Encode the payload into a JWT string using the secret key and algorithm.
    encoded_jwt = jwt.encode(
        to_encode, SECRET_KEY, algorithm=ALGORITHM
    )
    return encoded_jwt

def decode_access_token(
    token: str, session: Session
) -> User | None:
    try:
        payload = jwt.decode(
            token, SECRET_KEY, algorithms=[ALGORITHM]
        )
        # Extract the 'sub' (subject) claim from the payload.
        # In this app, the subject is the username.
        username: str = payload.get("sub")
    except JWTError:
        return
    if not username:
        return
    user = get_user(session, username)
    return user

router = APIRouter(tags=["Security"])

# Pydantic model defining the response structure for the access token.
class Token(BaseModel):
    access_token: str
    token_type: str

@router.post(
    "/token",
    response_model=Token,
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            "description": "Invalid username or password"
        }
    },
)
def get_user_access_token(
    # OAuth2PasswordRequestForm is a built-in dependency to handle form fields (username, password).
    # OAuth2PasswordRequestForm requires the request body to be 'application/x-www-form-urlencoded'.
    # It does NOT accept JSON
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: Session = Depends(get_session),
):
    # Authenticate the user against the database.
    user = authenticate_user(
        session,
        form_data.username,
        form_data.password,
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )
    # Create a JWT access token with the user's username as the subject.
    access_token = create_access_token(
        data={"sub": user.username}
    )
    return {
        "access_token": access_token,
        "token_type": "bearer",
    }

# Defines the security scheme. Tells FastAPI that the token is obtained from the "/token" URL
# and should be sent as a Bearer token in the Authorization header.
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@router.get(
    "/users/me",
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            "description": "User not authorized"
        },
        status.HTTP_200_OK: {
            "description": "username authorized"
        },
    },
)
def read_user_me(
    # Extract the token from the request header using the OAuth2 scheme.
    token: str = Depends(oauth2_scheme),
    session: Session = Depends(get_session),
):
    # Decode the token to identify the current user.
    user = decode_access_token(token, session)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not authorized",
        )
    return {
        "description": f"{user.username} authorized",
    }








