from bson import ObjectId


from db import get_db


from fastapi import APIRouter


from schemas import createUserBody, updateUserBody



app = APIRouter(tags=["Admin"])




db = get_db()





@app.post("/{admin_id}/create")
async def create_user(admin_id: str, body: createUserBody):
    type_ = int(body.type)
    details = {
        1: [
            "admins",
            {"username": body.username, "name": body.name, "email": body.email or body.age},
        ],
        2: [
            "doctors",
            {"username": body.username, "name": body.name, "email": body.email or body.age},
        ],
        3: [
            "parents",
            {
                "username": body.username,
                "name": body.name,
                "email": body.email or body.age,
                "height": body.height,
                "weight": body.weight,
                "gender": body.gender,
                "bloodGroup": body.bloodGroup,
                "guardianName": body.guardianName,
                "occupation": body.guardianName,
                "phoneNumber": body.phoneNumber,
                "address": body.address,
                "dob": body.dob,
    },],}
    new_user = {
        "username": body.username,
        "password": body.password,
        "type": type_,
        "createdBy": admin_id,
        "suspended": False,
        "name": body.name,
        "email": body.email or body.age,
    }


    if await user_exists(body.username):
        return {"message": "User already exists", "success": False}
    users = db["users"]
    result = users.insert_one(new_user)
    if not result.acknowledged:
        return {"message": "Error inserting details", "success": False}

    details[3][1]["_id"] = ObjectId(result.inserted_id)
    details[2][1]["_id"] = ObjectId(result.inserted_id)
    details[1][1]["_id"] = ObjectId(result.inserted_id)
    collection = db[details[body.type][0]]
    res2 = collection.insert_one(details[type_][1])
    if res2.acknowledged:
        return {"message": "User created successfully", "success": True}
    return {"message": "Error inserting details", "success": False}


@app.patch("/{admin_id}/update")
async def update_user(admin_id: str, user_id: str, body: updateUserBody):
    type_ = int(body.type)
    details = {
        1: [
            "admins",
            {
                "name": body.name,
                "username": body.username,
                "email": body.email or body.age,
        },],
        2: [
            "doctors",
            {
                "name": body.name,
                "username": body.username,
                "email": body.email or body.age,
        },],
        3: [
            "parents",
            {
                "name": body.name,
                "username": body.username,
                "email": body.email or body.age,
                "height": body.height,
                "weight": body.weight,
                "gender": body.gender,
                "bloodGroup": body.bloodGroup,
                "guardianName": body.guardianName,
                "occupation": body.occupation,
                "phoneNumber": body.phoneNumber,
                "address": body.address,
                "dob": body.dob,
    },],}

    user_collection = db["users"]
    user = user_collection.find_one({"_id": ObjectId(user_id)}, {"_id": 0})
    if not user:
        return {"message": "User not found"}
    if await user_exists(body.username):
        if user["username"] != body.username:
            return {"message": "Username already taken", "name": user}
    update_data = {
        "$set": {
            "username": body.username,
            "type": type_,
            "name": body.name,
            "email": body.email or body.age,
    }}
    user_collection.update_one({"_id": ObjectId(user_id)}, update_data)

    collection = db[details[type_][0]]
    update_data = {"$set": details[type_][1]}
    collection.update_one({"_id": ObjectId(user_id)}, update_data)

    return {"message": "User updated successfully"}






@app.patch("/{admin_id}/suspend")
async def suspend_user(admin_id: str, username: str):
    if not await user_exists(username):
        return {"message": "User not found", "success": False}

    users = db["users"]
    result = users.update_one(
        {"username": username}, {"$set": {"suspended": True, "suspendedBy": admin_id}}
    )
    if result.acknowledged:
        return {"message": "User suspended", "success": True}
    return {"message": "Internal server error", "success": False}




@app.patch("/{admin_id}/reinstate")
async def reinstate_user(admin_id: str, username: str):
    if not await user_exists(username):
        return {"message": "User not found", "success": False}

    users = db["users"]
    result = users.update_one(
        {"username": username}, {"$set": {"suspended": False, "reinstatedBy": admin_id}}
    )
    if result.acknowledged:
        return {"message": "User reinstated", "success": True}
    return {"message": "Internal server error", "success": False}




async def user_exists(username: str) -> bool:

    users = db["users"]

    result = users.find_one({"username": username}, projection={"username": 1})

    return result is not None