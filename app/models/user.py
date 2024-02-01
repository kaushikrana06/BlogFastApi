from bson import ObjectId
from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional

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

class UserModel(BaseModel):
    id: Optional[PyObjectId] = Field(alias='_id')
    email: EmailStr
    hashed_password: str
    tags: List[str] = []

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {
            ObjectId: str
        }
        schema_extra = {
            "example": {
                "email": "user@example.com",
                "hashed_password": "hashed_password_example",
                "tags": ["coding", "photography"]
            }
        }
