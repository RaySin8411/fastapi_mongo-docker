from fastapi import APIRouter, Body
from database.database import *
from models.building import *

router = APIRouter()


@router.get("/", response_description="Buildings retrieved", response_model=Response)
async def get_buildings():
    buildings = await retrieve_buildings()
    return Response(
        status_code=200, response_type="success",
        description="Buildings data retrieved successfully", data=buildings)


@router.get("/{id}", response_description="Building data retrieved", response_model=Response)
async def get_building_data(id: PydanticObjectId):
    building = await retrieve_building(id)
    if building:
        return Response(
            status_code=200, response_type="success",
            description="Building data retrieved successfully", data=building)

    return Response(status_code=404, response_type="error", description="Building doesn't exist")


@router.post("/", response_description="Building data added into the database", response_model=Response)
async def add_building_data(building: Building = Body(...)):
    new_building = await add_building(building)
    return Response(
        status_code=200, response_type="success",
        description="Building created successfully", data=new_building)


@router.delete("/{id}", response_description="Building data deleted from the database")
async def delete_building_data(id: PydanticObjectId):
    deleted_building = await delete_building(id)
    if deleted_building:
        return Response(
            status_code=200, response_type="success",
            description="Student with ID: {} removed".format(id), data=deleted_building)
    return Response(
        status_code=404, response_type="error",
        description="Student with id {0} doesn't exist".format(id), data=False)
