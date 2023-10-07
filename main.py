from fastapi import FastAPI
from database import Base, engine

from routers import address
from routers import distance

app = FastAPI()
Base.metadata.create_all(bind=engine)  # Initialize database

app.include_router(address.router)  # Load api for path /address
app.include_router(distance.router)  # Load api for path /distance