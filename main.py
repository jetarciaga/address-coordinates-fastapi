from fastapi import FastAPI
from database import Base, engine

from routers import address
from routers import distance

app = FastAPI()
Base.metadata.create_all(bind=engine)  # initialize database

app.include_router(address.router)
app.include_router(distance.router)