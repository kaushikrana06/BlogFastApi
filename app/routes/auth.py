from fastapi import APIRouter, HTTPException, Depends
from ..schemas.user import UserCreate, UserUpdate, User, TagsUpdate
from ..utils.security import create_access_token, get_password_hash, verify_password
from ..utils.database import get_database
from bson import ObjectId

router = APIRouter()

@router.post("/register", response_model=User)
async def register_user(user: UserCreate, db=Depends(get_database)):
    user_collection = db.get_collection("users")
    existing_user = await user_collection.find_one({"email": user.email})
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed_password = get_password_hash(user.password)
    new_user = await user_collection.insert_one(
        {"email": user.email, "hashed_password": hashed_password, "tags": []}
    )
    return {"id": str(new_user.inserted_id), "email": user.email, "tags": []}

@router.post("/login")
async def login(user: UserCreate, db=Depends(get_database)):
    user_collection = db.get_collection("users")
    db_user = await user_collection.find_one({"email": user.email})

    if not db_user or not verify_password(user.password, db_user["hashed_password"]):
        raise HTTPException(status_code=401, detail="Incorrect email or password")
    
    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}

@router.put("/users/{user_id}", response_model=User)
async def update_user(user_id: str, user: UserUpdate, db=Depends(get_database)):
    user_collection = db.get_collection("users")
    update_data = user.dict(exclude_unset=True)

    if "password" in update_data:
        hashed_password = get_password_hash(update_data["password"])
        update_data["hashed_password"] = hashed_password
        del update_data["password"]

    if update_data:
        await user_collection.update_one(
            {"_id": ObjectId(user_id)}, {"$set": update_data}
        )
        updated_user = await user_collection.find_one({"_id": ObjectId(user_id)})
        if updated_user:
            updated_user["id"] = str(updated_user["_id"])
            del updated_user["_id"]
            return updated_user
        else:
            raise HTTPException(status_code=404, detail="User not found")
    else:
        raise HTTPException(status_code=400, detail="No update data provided")


@router.post("/users/{user_id}/tags", response_model=User)
async def add_tags(user_id: str, tags_update: TagsUpdate, db=Depends(get_database)):
    user_collection = db.get_collection("users")

    # Convert each TagMeta instance in tags_update.tags to a dictionary
    tags_dicts = [tag.dict() for tag in tags_update.tags]

    await user_collection.update_one(
        {"_id": ObjectId(user_id)}, 
        {"$addToSet": {"tags": {"$each": tags_dicts}}}
    )

    updated_user = await user_collection.find_one({"_id": ObjectId(user_id)})
    if updated_user:
        updated_user["id"] = str(updated_user["_id"])
        del updated_user["_id"]
        return User(**updated_user)
    else:
        raise HTTPException(status_code=404, detail="User not found")



@router.delete("/users/{user_id}/tags", response_model=User)
async def remove_tags(user_id: str, tags_update: TagsUpdate, db=Depends(get_database)):
    user_collection = db.get_collection("users")

    # Build a condition for $pull that matches the structure of TagMeta objects
    # Assuming you want to remove tags based on matching 'name' field
    tags_names = [tag.name for tag in tags_update.tags]
    remove_condition = {"name": {"$in": tags_names}}

    await user_collection.update_one(
        {"_id": ObjectId(user_id)}, 
        {"$pull": {"tags": remove_condition}}
    )

    updated_user = await user_collection.find_one({"_id": ObjectId(user_id)})
    if updated_user:
        updated_user["id"] = str(updated_user["_id"])
        del updated_user["_id"]
        return User(**updated_user)
    else:
        raise HTTPException(status_code=404, detail="Tag not found")
