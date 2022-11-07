from fastapi import Depends, HTTPException, status
from app.core.utils.db import neo4j_driver
from app.model import UserInDB, User
from app.api.v1.services.authorization import get_current_user

async def get_user_with_username(username: str):
    query = 'MATCH (user:User) WHERE user.username = $username RETURN user'

    with neo4j_driver.session() as session:
        user_in_db = session.run(query=query, parameters={'username':username})
        user_data = user_in_db.data()[0]['user']
        return user_data

def get_user(username: str):
    query = f'MATCH (a:User) WHERE a.username = \'{username}\' RETURN a'

    with neo4j_driver.session() as session:
        user_in_db = session.run(query)
        user_data = user_in_db.data()[0]['a']
        return UserInDB(**user_data)

async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user