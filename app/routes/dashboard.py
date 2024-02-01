from fastapi import APIRouter, Depends, HTTPException
from ..schemas.blog import Blog
from ..utils.database import get_database
from pymongo import MongoClient, DESCENDING
from bson import ObjectId

router = APIRouter()

@router.get("/user/{user_id}/blogs", response_model=list[Blog])
async def get_user_blogs(user_id: str, skip: int = 0, limit: int = 10, db: MongoClient = Depends(get_database)):
    users_collection = db.get_collection("users")
    user = await users_collection.find_one({"_id": ObjectId(user_id)})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Separate liked tags and followed tags
    liked_tags = [tag['name'] for tag in user.get("tags", []) if tag['like'] == 1]
    followed_tags = [tag['name'] for tag in user.get("tags", []) if tag['like'] == 0]

    blogs_collection = db.get_collection("blogs")

    # Use aggregation to calculate score based on liked tags
    pipeline = [
        {
            "$addFields": {
                "score": {
                    "$size": {
                        "$setIntersection": ["$tags", liked_tags]
                    }
                }
            }
        },
        {
            "$match": {
                "tags": {"$in": liked_tags + followed_tags}  # Include blogs with either liked or followed tags
            }
        },
        {"$sort": {"score": DESCENDING, "created_at": DESCENDING}},  # Sort by score, then by creation date
        {"$skip": skip},
        {"$limit": limit}
    ]

    cursor = blogs_collection.aggregate(pipeline)

    blogs_list = []
    async for blog in cursor:
        blogs_list.append(Blog(**blog))

    return blogs_list
