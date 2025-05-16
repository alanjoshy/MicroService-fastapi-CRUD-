from fastapi import APIRouter, Request, Response, HTTPException
import httpx
from app.config import settings

router = APIRouter()


async def proxy_request(target_url: str, request: Request):
    """
    Generic function to proxy requests to microservices
    """
    # Get the path parameters from the request
    path = request.url.path
    
    # Create the target URL
    url = f"{target_url}{path}"
    
    # Get request body if it exists
    body = await request.body()
    
    # Get request headers (excluding host)
    headers = dict(request.headers)
    if "host" in headers:
        del headers["host"]
    
    # Create httpx client
    async with httpx.AsyncClient() as client:
        # Forward the request with the same method, headers, and body
        response = await client.request(
            method=request.method,
            url=url,
            headers=headers,
            content=body,
            params=request.query_params,
            follow_redirects=True
        )
        
        # Return the response
        return Response(
            content=response.content,
            status_code=response.status_code,
            headers=dict(response.headers)
        )


# Routes for User Service
@router.api_route("/api/users/{path:path}", methods=["GET", "POST", "PUT", "DELETE"])
async def user_service_route(request: Request, path: str):
    """Route requests to User Service"""
    return await proxy_request(settings.USER_SERVICE_URL, request)


# Routes for Admin Service
@router.api_route("/api/admin/{path:path}", methods=["GET", "POST", "PUT", "DELETE"])
async def admin_service_route(request: Request, path: str):
    """Route requests to Admin Service"""
    return await proxy_request(settings.ADMIN_SERVICE_URL, request)


# Routes for Auth Service
@router.api_route("/api/auth/{path:path}", methods=["GET", "POST", "PUT", "DELETE"])
async def auth_service_route(request: Request, path: str):
    """Route requests to Auth Service"""
    return await proxy_request(settings.AUTH_SERVICE_URL, request)


# Routes for Product Service
@router.api_route("/api/products/{path:path}", methods=["GET", "POST", "PUT", "DELETE"])
async def product_service_route(request: Request, path: str):
    """Route requests to Product Service"""
    return await proxy_request(settings.PRODUCT_SERVICE_URL, request)


# Health check endpoint
@router.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}