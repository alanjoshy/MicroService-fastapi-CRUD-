from fastapi import APIRouter
from app.api.endpoints import auth
from app.config import settings

router = APIRouter()

# Include router for auth endpoints with prefix
router.include_router(auth.router, prefix=settings.API_PREFIX)