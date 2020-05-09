from fastapi import APIRouter
from app.user import views as user
from app.helo import views as helo
from app.rest_jwt import views as jwt

router = APIRouter()
router.include_router(helo.router, tags=["Hello"], prefix="/helo")
router.include_router(user.router, tags=["User"], prefix="/user")
router.include_router(jwt.router, tags=["Jwt"], prefix="/jwt")
