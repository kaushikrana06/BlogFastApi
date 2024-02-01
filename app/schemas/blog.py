from pydantic import BaseModel, EmailStr, validator
from bson import ObjectId
from datetime import datetime
from typing import Optional, List

class BlogBase(BaseModel):
    title: str
    content: str
# class BlogID(BaseModel):
#     id: str

#     @validator('id', pre=True)
#     def validate_id_format(cls, value):
#         if not ObjectId.is_valid(value):
#             raise ValueError("Invalid ObjectId format for blog_id")
#         return value
class BlogCreate(BaseModel):
    owner_id: str
    title: str
    content: str
    tags: (List[str]) = []

class BlogUpdate(BlogBase):
    title: Optional[str] = None
    tags: Optional[List[str]] = []
    content: Optional[str] = None
    updated_at: datetime = datetime.utcnow()
  

class Blog(BlogBase):
    id: str
    title: str
    content: str
    owner_id: str
    created_at: datetime
    updated_at: Optional[datetime] = None
    tags: List[str] = []
