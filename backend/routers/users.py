from fastapi import APIRouter, Depends, HTTPException, Body
router = APIRouter()
from schemas.user_schemas import CreateUserBase
from database. 

@router.post("/user")
async def create_user(
    user
)
