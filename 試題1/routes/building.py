from fastapi import APIRouter, Body
from database.database import *
from models.building import *

router = APIRouter()


@router.get("/", response_description="Buildings retrieved", response_model=Response)
async def get_buildings():
    buildings = await retrieve_buildings()
    return Response(status_code=200, response_type="success", description="Buildings data retrieved successfully",
                    data=buildings)
