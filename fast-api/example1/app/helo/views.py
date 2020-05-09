from fastapi import APIRouter, Body, Depends, HTTPException

router = APIRouter()


@router.get('/')
async def hello():
    return {"message": "Hello World"}
