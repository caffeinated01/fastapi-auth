from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.routers import auth, users
from app.db.database import create_db_and_tables


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield

app = FastAPI(lifespan=lifespan)


@app.get("/")
async def root():
    return {"message": "Hello, World!"}


app.include_router(auth.router)
app.include_router(users.router)
