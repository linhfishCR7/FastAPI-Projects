from fastapi import FastAPI, Request
from strawberry.fastapi import GraphQLRouter
from db import engine, Base
from schema import schema
from auth import get_user_from_token
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield

app = FastAPI(lifespan=lifespan)

async def get_context(request: Request):
    """
    This function extracts the JWT token from the Authorization header,
    decodes it to get the current user, and adds the user to the context.
    """     
    token = None
    auth_header = request.headers.get("authorization")
    if auth_header:
        scheme, _, param = auth_header.partition(" ")
        if scheme.lower() == "bearer":
            token = param
    current_user = None
    if token:
        current_user = await get_user_from_token(token)
    return {"request": request, "current_user": current_user}


graphql_app = GraphQLRouter(schema, context_getter=get_context)

app.include_router(graphql_app, prefix="/graphql")