from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .. import models, schemas, auth
from ..database import get_db

router = APIRouter(prefix="/api/projects", tags=["Projects"])


@router.get("/", response_model=List[schemas.ProjectResponse])
async def get_projects(db: Session = Depends(get_db)):
    """Get all projects (public)"""
    projects = db.query(models.Project).order_by(models.Project.sort_order).all()
    return projects


@router.get("/{project_id}", response_model=schemas.ProjectResponse)
async def get_project(project_id: int, db: Session = Depends(get_db)):
    """Get a specific project (public)"""
    project = db.query(models.Project).filter(models.Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project


@router.post("/", response_model=schemas.ProjectResponse)
async def create_project(
    project: schemas.ProjectCreate,
    db: Session = Depends(get_db),
    current_user = Depends(auth.require_admin)
):
    """Create a project (admin only)"""
    db_project = models.Project(**project.model_dump())
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    return db_project


@router.put("/{project_id}", response_model=schemas.ProjectResponse)
async def update_project(
    project_id: int,
    project_update: schemas.ProjectUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(auth.require_admin)
):
    """Update a project (admin only)"""
    db_project = db.query(models.Project).filter(models.Project.id == project_id).first()
    if not db_project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    update_data = project_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_project, field, value)
    
    db.commit()
    db.refresh(db_project)
    return db_project


@router.delete("/{project_id}")
async def delete_project(
    project_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(auth.require_admin)
):
    """Delete a project (admin only)"""
    db_project = db.query(models.Project).filter(models.Project.id == project_id).first()
    if not db_project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    db.delete(db_project)
    db.commit()
    return {"message": "Project deleted"}
