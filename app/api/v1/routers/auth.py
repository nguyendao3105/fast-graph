import os
from dotenv import load_dotenv
from datetime import datetime, timedelta
from typing import Optional
import time

from fastapi import Depends, APIRouter, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from app.api.v1.services import authenticate_user, create_access_token, create_password_hash, create_user
from app.api.v1.schemas import Token
from app.model import User

auth_router = APIRouter()
load_dotenv('.env')
ACCESS_TOKEN_EXPIRE_MINUTES = os.environ.get('ACCESS_TOKEN_EXPIRE_MINUTES')
ACCESS_TOKEN_EXPIRE_MINUTES = int(ACCESS_TOKEN_EXPIRE_MINUTES)
app_password = os.environ.get('APP_PASSWORD')

@auth_router.post("/get-token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@auth_router.post('/launch_user')
async def first_user(username: str, 
                     password: str, 
                     application_password: str,
                     full_name: Optional[str] = None):
    if not application_password == app_password:
        denial = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect application password, please try again.",
            headers={"WWW-Authenticate": "Bearer"},
        )
        time.sleep(1)
        return denial

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