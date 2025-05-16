from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import timedelta
import requests
from jose import JWTError
from pydantic import EmailStr

from app.schemas.auth import Token, TokenData, HashPassword, ValidateToken
from app.utils.security import verify_password, get_password_hash, create_access_token, decode_token
from app.config import settings

router = APIRouter()


@router.post("/login", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    # Call user service to get user data
    response = requests.get(
        f"{settings.USER_SERVICE_URL}/api/users/by-username/{form_data.username}"
    )
    
    if response.status_code != 200:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    user = response.json()
    
    if not verify_password(form_data.password, user["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user["email"], "user_id": user["id"]},
        expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/hash-password")
async def hash_password(data: HashPassword):
    """Hash a password - used by other services."""
    return {"hashed_password": get_password_hash(data.password)}


@router.post("/validate-token")
async def validate_token(data: ValidateToken):
    """Validate a JWT token - used by other services."""
    try:
        payload = decode_token(data.token)
        email: str = payload.get("sub")
        user_id: int = payload.get("user_id")
        
        if email is None or user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        token_data = TokenData(email=email, user_id=user_id)
        return {"email": token_data.email, "user_id": token_data.user_id}
    
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )