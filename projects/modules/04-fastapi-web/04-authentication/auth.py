# ============================================================================
# auth.py — Authentication utilities
# ============================================================================
# This file contains everything related to authentication:
# 1. Password hashing (bcrypt via passlib)
# 2. JWT token creation and verification (python-jose)
# 3. get_current_user dependency (extracts user from the Authorization header)
#
# Keeping auth logic in a separate file makes it reusable and testable.
# ============================================================================

from datetime import datetime, timedelta, timezone

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from database import SessionLocal
from models import User

# ----------------------------------------------------------------------------
# Configuration
# SECRET_KEY is used to sign JWT tokens. In production, this should be a
# long random string stored in an environment variable, never in source code.
# ALGORITHM is the signing algorithm. HS256 (HMAC with SHA-256) is standard.
# ACCESS_TOKEN_EXPIRE_MINUTES controls how long tokens are valid.
# ----------------------------------------------------------------------------
SECRET_KEY = "your-secret-key-change-in-production"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

# ----------------------------------------------------------------------------
# Password hashing
# CryptContext wraps bcrypt, a one-way hashing algorithm designed for
# passwords. "One-way" means you can hash a password but cannot reverse
# the hash to get the original password back.
#
# When a user registers, we hash their password and store the hash.
# When they log in, we hash their input and compare it to the stored hash.
# We never store or compare plaintext passwords.
# ----------------------------------------------------------------------------
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# ----------------------------------------------------------------------------
# HTTPBearer extracts the token from the "Authorization: Bearer <token>"
# header. FastAPI uses this to add a lock icon to protected endpoints in
# the /docs UI.
# ----------------------------------------------------------------------------
security = HTTPBearer()


def hash_password(password: str) -> str:
    """Hash a plaintext password using bcrypt.

    The hash includes a random salt, so hashing the same password twice
    produces different hashes. This prevents attackers from using precomputed
    hash tables (rainbow tables) to crack passwords.
    """
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Check if a plaintext password matches a stored hash.

    passlib extracts the salt from the stored hash, hashes the input with
    the same salt, and compares the results. Returns True if they match.
    """
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict) -> str:
    """Create a JWT token containing the given data.

    A JWT has three parts separated by dots:
    1. Header  — algorithm and token type ({"alg": "HS256", "typ": "JWT"})
    2. Payload — your data plus expiration time
    3. Signature — HMAC of header + payload using SECRET_KEY

    The payload is base64-encoded (not encrypted!). Anyone can decode it
    and read the contents. The signature proves the token was created by
    your server and has not been tampered with.
    """
    to_encode = data.copy()

    # Set expiration time. After this time, the token is invalid.
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    # jwt.encode() creates the three-part token string.
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


# ============================================================================
# Database session dependency (same pattern as Project 03)
# ============================================================================
def get_db():
    """Provide a database session for the duration of a request."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ============================================================================
# get_current_user dependency
# ============================================================================
# This is the core of the authentication system. Any endpoint that includes
# `current_user: User = Depends(get_current_user)` becomes a protected
# endpoint. FastAPI will:
# 1. Extract the Bearer token from the Authorization header
# 2. Decode and verify the JWT
# 3. Look up the user in the database
# 4. Pass the User object to the endpoint
#
# If any step fails, a 401 Unauthorized error is returned automatically.
# ============================================================================
def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db),
) -> User:
    """Extract and validate the current user from the JWT token.

    This function is used as a FastAPI dependency. Endpoints that need
    authentication add it as a parameter:
        def my_endpoint(user: User = Depends(get_current_user)):
    """
    # The credentials object contains the token string.
    token = credentials.credentials

    # Define the error we will raise if anything goes wrong.
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        # Decode the JWT. This verifies the signature and checks expiration.
        # If the token is invalid or expired, JWTError is raised.
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        # Extract the username from the token payload.
        # We stored it as "sub" (subject) when creating the token.
        username: str | None = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    # Look up the user in the database.
    user = db.query(User).filter(User.username == username).first()
    if user is None:
        raise credentials_exception

    return user
