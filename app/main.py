#app/main.py
from fastapi import FastAPI
from app.data.database import engine
from app.data.models import Base
from app.fastapi_routers import chat

# Create all tables
Base.metadata.create_all(bind=engine)

# Create the FastAPI instance
app = FastAPI()

# Include "chat" router
app.include_router(chat.router, tags=["chat"])

