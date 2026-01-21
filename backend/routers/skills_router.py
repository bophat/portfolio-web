from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .. import models, schemas, auth
from ..database import get_db

router = APIRouter(prefix="/api/skills", tags=["Skills"])


@router.get("/", response_model=List[schemas.SkillResponse])
async def get_skills(db: Session = Depends(get_db)):
    """Get all skills (public)"""
    skills = db.query(models.Skill).order_by(models.Skill.category, models.Skill.sort_order).all()
    return skills


@router.get("/categories")
async def get_skill_categories(db: Session = Depends(get_db)):
    """Get skills grouped by category (public)"""
    skills = db.query(models.Skill).order_by(models.Skill.category, models.Skill.sort_order).all()
    
    categories = {}
    for skill in skills:
        if skill.category not in categories:
            categories[skill.category] = {
                "name": skill.category,
                "icon": skill.category_icon,
                "skills": []
            }
        categories[skill.category]["skills"].append({
            "id": skill.id,
            "name": skill.name,
            "level": skill.level,
            "is_learning": skill.is_learning
        })
    
    return list(categories.values())


@router.post("/", response_model=schemas.SkillResponse)
async def create_skill(
    skill: schemas.SkillCreate,
    db: Session = Depends(get_db),
    current_user = Depends(auth.require_admin)
):
    """Create a skill (admin only)"""
    db_skill = models.Skill(**skill.model_dump())
    db.add(db_skill)
    db.commit()
    db.refresh(db_skill)
    return db_skill


@router.put("/{skill_id}", response_model=schemas.SkillResponse)
async def update_skill(
    skill_id: int,
    skill_update: schemas.SkillUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(auth.require_admin)
):
    """Update a skill (admin only)"""
    db_skill = db.query(models.Skill).filter(models.Skill.id == skill_id).first()
    if not db_skill:
        raise HTTPException(status_code=404, detail="Skill not found")
    
    update_data = skill_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_skill, field, value)
    
    db.commit()
    db.refresh(db_skill)
    return db_skill


@router.delete("/{skill_id}")
async def delete_skill(
    skill_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(auth.require_admin)
):
    """Delete a skill (admin only)"""
    db_skill = db.query(models.Skill).filter(models.Skill.id == skill_id).first()
    if not db_skill:
        raise HTTPException(status_code=404, detail="Skill not found")
    
    db.delete(db_skill)
    db.commit()
    return {"message": "Skill deleted"}
