import os
from dotenv import load_dotenv
from typing import Optional
from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext

from fastapi import Depends
from fastapi import HTTPException, status
from fastapi.security import OAuth2PasswordBearer


from app.core.utils.db import neo4j_driver
from app.model import UserInDB, User
from app.api.v1.schemas import TokenData
from .user import get_current_active_user, get_user

load_dotenv('.env')
SECRET_KEY = os.environ.get('SECRET_KEY')
ALGORITHM = os.environ.get('ALGORITHM')
ACCESS_TOKEN_EXPIRE_MINUTES = os.environ.get('ACCESS_TOKEN_EXPIRE_MINUTES')
ACCESS_TOKEN_EXPIRE_MINUTES = int(ACCESS_TOKEN_EXPIRE_MINUTES)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
app_password = os.environ.get('APP_PASSWORD')
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")

def create_password_hash(password):
    return pwd_context.hash(password)

def verify_password(plain_password, password_hash):
    return pwd_context.verify(plain_password, password_hash)

async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user(username=token_data.username)
    if user is None:
        raise credentials_exception
    return user

def authenticate_user(username, password):
    user = get_user(username)
    if not user:
        return False
    
    password_hash = user.hashed_password
    username = user.username
    
    if not verify_password(password, password_hash):
        return False
    return user

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def create_user(attributes: dict):
    cypher_search = 'MATCH (user:User) WHERE user.username = $username RETURN user'
    cypher_create = 'CREATE (user:User $params) RETURN user'

    with neo4j_driver.session() as session:
        # First, run a search of users to determine if username is already in use
        check_users = session.run(query=cypher_search, parameters={'username':attributes['username']})
        
        # Return error message if username is already in the database
        if check_users.data():
            raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Operation not permitted, user with username {attributes['username']} already exists.",
            headers={"WWW-Authenticate": "Bearer"})

        response = session.run(query=cypher_create, parameters={'params':attributes})
        user_data = response.data()[0]['user']
        return user_data