from fastapi import APIRouter
from db import get_db

app = APIRouter(
	tags=["authentication"]
)


db = get_db()


@app.get("/validate")
async def validate_user(username: str, password: str):
	users = db["users"]

	result = users.find_one({"username": username}, projection={"_id": 0})

	if result:
		if result["password"] == password:
			if result.get("suspended"):
				return {"message": "User suspended by admin", "access": False}
			else:
				print("user logged")
				print(result)
				return {"message": "Success", "type": result["type"], "access": True}

		else:
			return {"message": f"Password for {username} is wrong", "access": False}

	else:
		return {"message": "User not found", "access": False}
