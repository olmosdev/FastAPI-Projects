import pyotp
from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
)
from sqlalchemy.orm import Session

from db_connection import get_session
from operations import get_user
from rbac import get_current_user
from responses import UserCreateResponse

def generate_totp_secret():
    # Generate a random base32 secret string.
    return pyotp.random_base32()


def generate_totp_uri(secret, user_email):
    # Create the provisioning URI.
    # This URI is typically converted into a QR code on the frontend
    # so the user can scan it with an authenticator app (e.g., Google Authenticator).
    return pyotp.totp.TOTP(secret).provisioning_uri(
        name=user_email, issuer_name="SaasFastAPIapp"
    )


router = APIRouter(tags=["Multi-Factor Authentication (MFA)"])


# Endpoint to enable Multi-Factor Authentication (MFA) for the currently logged-in user.
@router.post("/user/enable-mfa")
def enable_mfa(
    user: UserCreateResponse = Depends(
        get_current_user
    ),
    db_session: Session = Depends(get_session),
):
    # 1. Generate a new random secret for this user.
    secret = generate_totp_secret()
    # 2. Retrieve the user record from the database to update it.
    db_user = get_user(db_session, user.username)
    # 3. Store the generated secret in the user's record.
    db_user.totp_secret = secret
    db_session.add(db_user)
    db_session.commit()
    # 4. Generate the URI needed for the authenticator app.
    totp_uri = generate_totp_uri(secret, user.email)

    # Return the TOTP URI
    # for QR code generation in the frontend
    return {
        "totp_uri": totp_uri,
        "secret_numbers": pyotp.TOTP(secret).now(),
    }


# Endpoint to verify a TOTP code provided by the user.
# This is used to confirm that the user has correctly set up their authenticator app
# or to grant access during a login flow requiring 2FA.
@router.post("/verify-totp")
def verify_totp(
    code: str,
    username: str,
    session: Session = Depends(get_session),
):
    # 1. Retrieve the user from the database.
    user = get_user(session, username)
    # 2. Check if MFA is actually enabled for this user (i.e., they have a secret stored).
    if not user.totp_secret:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="MFA not activated",
        )

    # 3. Initialize the TOTP object with the user's stored secret.
    totp = pyotp.TOTP(user.totp_secret)
    # 4. Verify the provided code against the generated code for the current time.
    if not totp.verify(code):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid TOTP token",
        )
    # 5. Proceed with granting access
    # or performing the sensitive operation
    return {
        "message": "TOTP token verified successfully"
    }
