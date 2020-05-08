from fastapi import APIRouter, Body, Depends, HTTPException, FastAPI, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import secrets

router = APIRouter()
security = HTTPBasic()


@router.get("/users/me-test")
def read_current_user(credentials: HTTPBasicCredentials = Depends(security)):
    return {"username": credentials.username, "password": credentials.password}


def get_current_username(credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = secrets.compare_digest(credentials.username, "stanleyjobson")
    correct_password = secrets.compare_digest(credentials.password, "swordfish")
    # if not (credentials.username == "stanleyjobson") or not (credentials.password == "swordfish"):
    # 但是通过使用， secrets.compare_digest() 它将可以安全地防御称为“定时攻击”的攻击。
    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username


@router.get("/users/me")
async def read_current_user(username: str = Depends(get_current_username)):
    return {"username": username}


