from typing import List, Union

from beanie import PydanticObjectId

from models.building import Building

building_collection = Building


async def add_building(new_building: Building) -> Building:
    building = await new_building.create()
    return building


async def retrieve_buildings() -> List[Building]:
    buildings = await building_collection.all().to_list()
    return buildings


async def retrieve_building(id: PydanticObjectId) -> Building:
    building = await building_collection.get(id)
    return building


async def delete_building(id: PydanticObjectId) -> bool:
    building = await building_collection.get(id)
    if building:
        await building.delete()
        return True
    return False
