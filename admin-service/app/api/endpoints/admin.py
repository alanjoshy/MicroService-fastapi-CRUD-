from fastapi import APIRouter, Depends, HTTPException, status, Header
from sqlalchemy.orm import Session
from typing import List, Optional
import requests

from app.database import get_db
from app.config import settings

router = APIRouter()


@router.get("/users")
def get_all_users(
    skip: int = 0, 
    limit: int = 100, 
    search: Optional[str] = None,
    is_active: Optional[bool] = None,
    authorization: Optional[str] = Header(None),
    db: Session = Depends(get_db)
):
    """Get all users with optional filtering"""
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials"
        )
    
    token = authorization.replace("Bearer ", "")
    
    # Validate admin token
    response = requests.post(
        f"{settings.AUTH_SERVICE_URL}/api/auth/validate-token",
        json={"token": token}
    )
    
    if response.status_code != 200:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials"
        )
    
    # Verify admin role
    token_data = response.json()
    admin_check_response = requests.get(
        f"{settings.USER_SERVICE_URL}/api/users/{token_data['user_id']}",
        headers={"Authorization": authorization}
    )
    
    if admin_check_response.status_code != 200 or not admin_check_response.json().get("is_admin", False):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access admin resources"
        )
    
    # Get users with filtering
    params = {"skip": skip, "limit": limit}
    if search:
        params["search"] = search
    if is_active is not None:
        params["is_active"] = is_active
    
    user_response = requests.get(
        f"{settings.USER_SERVICE_URL}/api/users/",
        params=params,
        headers={"Authorization": authorization}
    )
    
    if user_response.status_code != 200:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch users"
        )
    
    return user_response.json()


@router.put("/users/{user_id}/block")
def block_user(
    user_id: int, 
    authorization: Optional[str] = Header(None),
    db: Session = Depends(get_db)
):
    """Block a user"""
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials"
        )
    
    token = authorization.replace("Bearer ", "")
    
    # Validate admin token (same as above)
    # ...
    
    # Block user
    response = requests.put(
        f"{settings.USER_SERVICE_URL}/api/users/{user_id}",
        json={"is_active": False},
        headers={"Authorization": authorization}
    )
    
    if response.status_code != 200:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to block user"
        )
    
    return {"message": "User blocked successfully"}


@router.put("/users/{user_id}/unblock")
def unblock_user(
    user_id: int,
    authorization: Optional[str] = Header(None),
    db: Session = Depends(get_db)
):
    """Unblock a user"""
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials"
        )
    
    token = authorization.replace("Bearer ", "")
    
    # Validate admin token (same as above)
    # ...
    
    # Unblock user
    response = requests.put(
        f"{settings.USER_SERVICE_URL}/api/users/{user_id}",
        json={"is_active": True},
        headers={"Authorization": authorization}
    )
    
    if response.status_code != 200:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to unblock user"
        )
    
    return {"message": "User unblocked successfully"}