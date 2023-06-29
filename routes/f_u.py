
from db import get_db
from fastapi import APIRouter, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse, StreamingResponse
from pymongo import MongoClient
from gridfs import GridFS
from bson.objectid import ObjectId


db = get_db()
app = APIRouter(
    tags=["File Upload"],
)

fs = GridFS(db)
fs_collection = db.fs.files

# Create indexes for GridFS
fs_collection.create_index("filename")
fs_collection.create_index("uploadDate")


@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    try:
        # Save the file to GridFS
        file_id = fs.put(file.file, filename=file.filename)

        # Optionally, you can store additional metadata
        # fs.put(file.file, filename=file.filename, metadata={"user_id": user_id})

        return JSONResponse({"message": "File uploaded successfully.", "file_id": str(file_id)})
    except Exception as e:
        return JSONResponse({"message": "Failed to upload file.", "error": str(e)}, status_code=500)


@app.get("/file/{file_id}")
async def get_file(file_id: str):
    try:
        file = fs.get(ObjectId(file_id))
        
        if file is not None:
            filename = file.filename
            return StreamingResponse(file, media_type="application/octet-stream", headers={"Content-Disposition": f"attachment; filename={filename}"})

        return JSONResponse({"message": "File not found."}, status_code=404)
    except Exception as e:
        return JSONResponse({"message": "Failed to retrieve file.", "error": str(e)}, status_code=500)

@app.delete("/file/{file_id}")
async def delete_file(file_id: str):
    try:
        # Delete the fs and chunks files
        fs.delete(ObjectId(file_id))

        return {"message": "File deleted successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))