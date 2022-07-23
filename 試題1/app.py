from fastapi import FastAPI
from config.config import initiate_database
from routes.building import router as BuildingRouter

app = FastAPI()


@app.on_event("startup")
async def start_db():
    await initiate_database()


@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Welcome to this fantastic app, sighs."}

app.include_router(BuildingRouter, tags=["Buildings"], prefix="/building")
