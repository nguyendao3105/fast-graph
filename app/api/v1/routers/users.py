# Import required base modules
#from neo4j import GraphDatabase, Query
from datetime import datetime
import os
from dotenv import load_dotenv
from typing import Optional

# Import modules from FastAPI
from fastapi import APIRouter, Depends, HTTPException, status


from app.model import User
from app.api.v1.services import get_current_active_user, create_password_hash, create_user
from app.api.v1.services.user import get_user_with_username

# Load environment variables
load_dotenv('.env')

# Set the API Router
router = APIRouter()

# GET Current user's information
@router.get("/me", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user

# GET Specified user's information by username
@router.get('/{username}', response_model=User)
async def read_user(username: str):
    user_data = {"a": "a"}

    return User(**user_data)

# CREATE User
@router.post("/create", response_model=User)
async def create_user(username: str, password: str, 
                      full_name: Optional[str] = None,
                      disabled: Optional[bool] = None):

    # Create dictionary of new user attributes
    attributes = {'username':username,
                  'full_name':full_name,
                  'hashed_password':create_password_hash(password),
                  'joined':str(datetime.utcnow()),
                  'disabled':disabled}

    # Write Cypher query and run against the database
    cypher_search = 'MATCH (user:User) WHERE user.username = $username RETURN user'
    cypher_create = 'CREATE (user:User $params) RETURN user'

    # Create dictionary of new user attributes
    attributes = {'username':username,
                  'full_name':full_name,
                  'hashed_password':create_password_hash(password),
                  'joined':str(datetime.utcnow()),
                  'disabled':False}
    user_data = await create_user(attributes)
    # Write Cypher query and run against the database
   
    user = User(**user_data)
    return user