from typing import Optional, Any

from beanie import Document
from pydantic import BaseModel


class Building(Document):
    city_area: str
    area_id: str
    road: str
    use_license: str
    construction_license: str
    applicant: str
    designer: str
    address: str
    date: str


class UpdateStudentModel(BaseModel):
    city_area: Optional[str]
    area_id: Optional[str]
    road: Optional[str]
    use_license: Optional[str]
    construction_license: Optional[str]
    applicant: Optional[str]
    designer: Optional[str]
    address: Optional[str]
    date: Optional[str]

    class Collection:
        name = "building"


class Response(BaseModel):
    status_code: int
    response_type: str
    description: str
    data: Optional[Any]

    class Config:
        schema_extra = {
            "example": {
                "status_code": 200,
                "response_type": "success",
                "description": "Operation successful",
                "data": "Sample data"
            }
        }
