from bson import ObjectId
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")

class BlogModel(BaseModel):
    id: Optional[PyObjectId] = Field(alias='_id')
    title: str
    content: str
    created_at: Optional[datetime] = None
    owner_id: PyObjectId
    tags: List[str] = []

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {
            ObjectId: str
        }
        schema_extra = {
            "example": {
                "title": "Example Blog Title",
                "content": "This is blog content",
                "created_at": datetime.now(),
                "owner_id": "owner_object_id",
                "tags": ["tech", "python"]
            }
        }
