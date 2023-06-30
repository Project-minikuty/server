from fastapi import APIRouter
from db import c2j, d2j, get_db

app = APIRouter(
	tags=["authentication"]
)


db = get_db()


@app.get("/validate")
async def validate_user(username: str, password: str):
	users = db["users"]

	result = users.find_one({"username": username})
	print(result)
	if result:
		if result["password"] == password:
			if result.get("suspended"):
				return {"message": "User suspended by admin", "access": False}
			else:
				print("user logged")
				return {"message": "Success", "details":d2j(result), "access": True}

		else:
			return {"message": f"Password for {username} is wrong", "access": False}

	else:
		return {"message": "User not found", "access": False}
