from fastapi import APIRouter, HTTPException, Depends, status
from ..schemas.blog import BlogCreate, BlogUpdate, Blog
from ..utils.database import get_database
from bson import ObjectId
from typing import List
from bson import ObjectId
from pydantic import BaseModel, Field
from datetime import datetime
from pymongo import MongoClient


class CustomValidationError(HTTPException):
    def __init__(self):
        detail = "Validation error: One or more fields are missing."
        super().__init__(status_code=400, detail=detail)

router = APIRouter()



@router.post("/", response_model=Blog)
async def create_blog(blog: BlogCreate, db=Depends(get_database)):
    if not blog.owner_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Validation error: owner_id is missing."
        )
    
    current_time = datetime.utcnow()  # Capture the current time
    
    blog_data = blog.dict()
    blog_data["created_at"] = current_time  # Assign the creation time
    # blog_data["id"] = str(ObjectId())  # Generate a unique ID for the blog
    
    # Add an 'updated_at' field with a default value of None
    blog_data["updated_at"] = current_time
    
    blog_collection = db.get_collection("blogs")
    new_blog = await blog_collection.insert_one(blog_data)
    
    # Return the created blog with the updated fields
    created_blog = await blog_collection.find_one({"_id": new_blog.inserted_id})
    created_blog["id"] = str(created_blog["_id"])

    return created_blog

@router.get("/", response_model=List[Blog])
async def get_blogs(skip: int = 0, limit: int = 10, db: MongoClient = Depends(get_database)):
    blog_collection = db.get_collection("blogs")

    # Fetch blogs with pagination
    blogs_cursor = blog_collection.find().skip(skip).limit(limit)
    blogs = await blogs_cursor.to_list(length=limit)
    
    # Transform the blogs to include 'id' and remove '_id'
    blogs_with_required_fields = []
    for blog in blogs:
        blog_with_required_fields = {
            "id": str(blog["_id"]),
            "title": blog["title"],
            "content": blog["content"],
            "owner_id": blog["owner_id"],
            "created_at": blog["created_at"],
            "updated_at": blog.get("updated_at", None),  # Handle None for updated_at
            "tags": blog.get("tags", [])
        }
    
        blogs_with_required_fields.append(blog_with_required_fields)
    
    return blogs_with_required_fields

@router.get("/{blog_id}", response_model=Blog)
async def get_blog(blog_id: str, db=Depends(get_database)):
    # Validate the blog_id format
    if not ObjectId.is_valid(blog_id):
        raise HTTPException(status_code=400, detail="Invalid ObjectId format for blog_id")
    
    blog_collection = db.get_collection("blogs")
    blog = await blog_collection.find_one({"_id": ObjectId(blog_id)})

    # Handle case where blog is not found
    if blog is None:
        raise HTTPException(status_code=404, detail=f"Blog with id {blog_id} not found")

    # Construct response with correct 'id' field
    return {
        "id": str(blog["_id"]),
        "title": blog["title"],
        "content": blog["content"],
        "owner_id": blog["owner_id"],
        "created_at": blog["created_at"],
        "updated_at": blog.get("updated_at", None),
        "tags": blog.get("tags", [])
    }


@router.put("/{blog_id}", response_model=Blog)
async def update_blog(blog_id: str, blog: BlogUpdate, db=Depends(get_database)):
    blog_collection = db.get_collection("blogs")
   

    update_result = await blog_collection.update_one({"_id": ObjectId(blog_id)}, {"$set": blog.dict(exclude_unset=True)})
    
    if update_result.modified_count == 0:
        raise HTTPException(status_code=404, detail=f"Blog with id {blog_id} is not found or no updates are provided")
    
    updated_blog = await blog_collection.find_one({"_id": ObjectId(blog_id)})
    updated_blog["id"] = str(updated_blog["_id"])
    del updated_blog["_id"]
    return updated_blog

@router.delete("/{blog_id}")
async def delete_blog(blog_id: str, db=Depends(get_database)):
    if not ObjectId.is_valid(blog_id):
        raise HTTPException(status_code=400, detail="Invalid ObjectId format for blog_id")
   
    blog_collection = db.get_collection("blogs")
    delete_result = await blog_collection.delete_one({"_id": ObjectId(blog_id)})
    
    if delete_result.deleted_count == 0:
        raise HTTPException(status_code=404, detail=f"Blog with id {blog_id} not found")
    
    return {"message": "Blog deleted successfully"}
