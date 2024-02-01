from pydantic import BaseModel, EmailStr
from typing import List
from typing import Optional
class TagMeta(BaseModel):
    like: int  # 1 indicates liked, 0 otherwise
    name: str
class UserBase(BaseModel):
    email: EmailStr

class UserCreate(UserBase):
    password: str

class UserUpdate(UserBase):
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    tags: Optional[List[TagMeta]] = None


class UserInDB(UserBase):
    hashed_password: str
    tags: List[TagMeta] = []
   

class User(UserBase):
    id: str
    tags: List[TagMeta] = []

class TagsUpdate(BaseModel):
    tags: List[TagMeta]
