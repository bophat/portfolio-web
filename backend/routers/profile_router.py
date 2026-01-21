from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .. import models, schemas, auth
from ..database import get_db

router = APIRouter(prefix="/api/profile", tags=["Profile"])


@router.get("/", response_model=schemas.ProfileResponse)
async def get_profile(db: Session = Depends(get_db)):
    """Get profile (public)"""
    profile = db.query(models.Profile).first()
    if not profile:
        # Create default profile if none exists
        profile = models.Profile(
            name="Alex Chen",
            title="Junior Backend & Data Engineer",
            summary="Recent graduate with a strong foundation in Python and SQL. I enjoy building reliable data pipelines and backend services. Currently seeking my first full-time role where I can learn from experienced engineers and contribute to meaningful projects.",
            hero_badge="Open to opportunities"
        )
        db.add(profile)
        db.commit()
        db.refresh(profile)
    return profile


@router.put("/", response_model=schemas.ProfileResponse)
async def update_profile(
    profile_update: schemas.ProfileUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(auth.require_admin)
):
    """Update profile (admin only)"""
    profile = db.query(models.Profile).first()
    if not profile:
        profile = models.Profile()
        db.add(profile)
    
    update_data = profile_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(profile, field, value)
    
    db.commit()
    db.refresh(profile)
    return profile
