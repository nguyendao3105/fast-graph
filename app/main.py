# Import main FastAPI modules
from fastapi import FastAPI

from app.api.v1.routers import auth_router, users_router

app = FastAPI(title='Fast-graph',
              description='API built for Neo4j with FastAPI',
              version=0.1,
              docs_url='/docs',
              redoc_url='/redoc')

app.include_router(
    auth_router,
    prefix='/auth',
    tags=['Authorisation']
)
app.include_router(
    users_router,
    prefix='/users',
    tags=['Users']
)
