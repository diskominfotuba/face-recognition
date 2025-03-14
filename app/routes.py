from fastapi import APIRouter, UploadFile, File,  Depends
import shutil
import os
from .face_utils import register_face, recognize_face

router = APIRouter()

UPLOAD_DIR = "images/"

@router.post("/register-face/")
async def register_face_api(user_id: str, file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return register_face(file_path, user_id)

@router.post("/recognize-face/")
async def recognize_face_api(user_id: str, file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return recognize_face(user_id, file_path)
