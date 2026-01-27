"""
File upload router for images and videos.
"""
import os
import uuid
import shutil
from typing import List
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from .. import models, auth
from ..database import get_db

router = APIRouter(prefix="/api/upload", tags=["Upload"])

# Configuration
UPLOAD_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "static", "uploads")
MAX_IMAGE_SIZE = 5 * 1024 * 1024  # 5MB
MAX_VIDEO_SIZE = 50 * 1024 * 1024  # 50MB
ALLOWED_IMAGE_TYPES = {"image/jpeg", "image/png", "image/gif", "image/webp"}
ALLOWED_VIDEO_TYPES = {"video/mp4", "video/webm", "video/quicktime"}


def ensure_upload_dir(user_id: int) -> str:
    """Ensure upload directory exists for user"""
    user_dir = os.path.join(UPLOAD_DIR, str(user_id))
    os.makedirs(user_dir, exist_ok=True)
    return user_dir


@router.post("/image")
async def upload_image(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.require_current_user)
):
    """Upload an image file"""
    # Validate content type
    if file.content_type not in ALLOWED_IMAGE_TYPES:
        raise HTTPException(
            status_code=400, 
            detail=f"Invalid file type. Allowed: {', '.join(ALLOWED_IMAGE_TYPES)}"
        )
    
    # Read and check size
    contents = await file.read()
    if len(contents) > MAX_IMAGE_SIZE:
        raise HTTPException(
            status_code=400,
            detail=f"File too large. Maximum size: {MAX_IMAGE_SIZE // (1024*1024)}MB"
        )
    
    # Generate unique filename
    ext = file.filename.split(".")[-1] if "." in file.filename else "jpg"
    filename = f"{uuid.uuid4().hex}.{ext}"
    
    # Save file
    user_dir = ensure_upload_dir(current_user.id)
    file_path = os.path.join(user_dir, filename)
    
    with open(file_path, "wb") as f:
        f.write(contents)
    
    # Return URL path
    url = f"/static/uploads/{current_user.id}/{filename}"
    return {"url": url, "filename": filename}


@router.post("/video")
async def upload_video(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.require_current_user)
):
    """Upload a video file"""
    # Validate content type
    if file.content_type not in ALLOWED_VIDEO_TYPES:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid file type. Allowed: {', '.join(ALLOWED_VIDEO_TYPES)}"
        )
    
    # Read and check size
    contents = await file.read()
    if len(contents) > MAX_VIDEO_SIZE:
        raise HTTPException(
            status_code=400,
            detail=f"File too large. Maximum size: {MAX_VIDEO_SIZE // (1024*1024)}MB"
        )
    
    # Generate unique filename
    ext = file.filename.split(".")[-1] if "." in file.filename else "mp4"
    filename = f"{uuid.uuid4().hex}.{ext}"
    
    # Save file
    user_dir = ensure_upload_dir(current_user.id)
    file_path = os.path.join(user_dir, filename)
    
    with open(file_path, "wb") as f:
        f.write(contents)
    
    # Return URL path
    url = f"/static/uploads/{current_user.id}/{filename}"
    return {"url": url, "filename": filename}


@router.delete("/{filename}")
async def delete_upload(
    filename: str,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.require_current_user)
):
    """Delete an uploaded file"""
    user_dir = os.path.join(UPLOAD_DIR, str(current_user.id))
    file_path = os.path.join(user_dir, filename)
    
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")
    
    os.remove(file_path)
    return {"message": "File deleted"}
