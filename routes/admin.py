from fastapi import APIRouter
from pymongo import MongoClient
from bson import ObjectId
from db import get_db
from schemas import createUserBody

app = APIRouter(
    tags=["Admin"]
)


db = get_db()


@app.post("/{admin_id}/create")
async def create_user(admin_id: str, body: createUserBody):
    details = {1: ["admins", {
        "username": body.username,
        "name":body.name
    }],
    2:
    ["doctors",{
        "username": body.username,
        "name": body.name
    }],
    3:[
        "parents",{
            "username": body.username,
            "name": body.name,
            "age": body.age,
            "height":body.height,
            "weight":body.weight,
            "gender":body.gender,
            "bloodGroup":body.bloodGroup,
            "guardianName":body.guardianName,
            "occupation":body.guardianName,
            "phoneNumber":body.phoneNumber,
            "address":body.address,
            "dob":body.dob

        }
    ]}
    newUser = {
        "username": body.username,
        "password": body.password,
        "type": body.type,
        "createdBy": admin_id,
        "suspended": False,
    }

    if await user_exists(body.username):
        return {"message": "User already exists"}

    users = db["users"]
    result = users.insert_one(newUser)
    if result.acknowledged:
        collection = db[details.get(body.type)[0]]
        details["_id"] = id
        res2 = collection.insert_one(details.get(body.type)[1])
        if res2.acknowledged:
            return "User created successfully"
        else:
            return "Error inserting details"
    else:
        return "User not created"


@app.post("/{admin_id}/suspend")
async def suspend_user(admin_id: str, username: str):
    if await user_exists(username):
        users = db["users"]
        result = users.update_one(
            {"username": username},
            {"$set": {"suspended": True, "suspendedBy": admin_id}}
        )
        if result.acknowledged:
            return {"message": "User suspended", "success": True}
        else:
            return {"message": "Internal server error", "success": False}
    else:
        return {"message": "User not found", "success": False}


@app.post("/{admin_id}/reinstate")
async def reinstate_user(admin_id: str, username: str):
    if await user_exists(username):
        users = db["users"]
        result = users.update_one(
            {"username": username},
            {"$set": {"suspended": False, "reinstatedBy": admin_id}}
        )
        if result.acknowledged:
            return {"message": "User reinstated", "success": True}
        else:
            return {"message": "Internal server error", "success": False}
    else:
        return {"message": "User not found", "success": False}


async def user_exists(username: str) -> bool:
    users = db["users"]
    result = users.find_one({"username": username}, projection={"username": 1})
    return result is not None