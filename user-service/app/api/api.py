from fastapi import APIRouter
from app.api.endpoints import users
from app.config import settings

router = APIRouter()

# Include router for user endpoints with prefix
router.include_router(users.router, prefix=settings.API_PREFIX)