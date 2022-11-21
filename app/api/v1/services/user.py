from fastapi import Depends, HTTPException, status
from app.core.utils.db import neo4j_driver
from app.model import UserInDB, User

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
