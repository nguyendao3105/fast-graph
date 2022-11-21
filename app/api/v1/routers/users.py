from dotenv import load_dotenv

from fastapi import APIRouter
load_dotenv('.env')

# Set the API Router
users_router = APIRouter()

# GET Current user's information
@users_router.get("/")
async def read_users_me():
    return {"msg": "User router"}

@users_router.get("/me")
async def read_users_me():
    return {"msg": "User router"}