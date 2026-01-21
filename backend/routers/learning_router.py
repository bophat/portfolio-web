from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .. import models, schemas, auth
from ..database import get_db

router = APIRouter(prefix="/api/learning", tags=["Learning Goals"])


@router.get("/", response_model=List[schemas.LearningGoalResponse])
async def get_learning_goals(db: Session = Depends(get_db)):
    """Get all learning goals (public)"""
    goals = db.query(models.LearningGoal).order_by(models.LearningGoal.sort_order).all()
    return goals


@router.post("/", response_model=schemas.LearningGoalResponse)
async def create_learning_goal(
    goal: schemas.LearningGoalCreate,
    db: Session = Depends(get_db),
    current_user = Depends(auth.require_admin)
):
    """Create a learning goal (admin only)"""
    db_goal = models.LearningGoal(**goal.model_dump())
    db.add(db_goal)
    db.commit()
    db.refresh(db_goal)
    return db_goal


@router.put("/{goal_id}", response_model=schemas.LearningGoalResponse)
async def update_learning_goal(
    goal_id: int,
    goal_update: schemas.LearningGoalUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(auth.require_admin)
):
    """Update a learning goal (admin only)"""
    db_goal = db.query(models.LearningGoal).filter(models.LearningGoal.id == goal_id).first()
    if not db_goal:
        raise HTTPException(status_code=404, detail="Learning goal not found")
    
    update_data = goal_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_goal, field, value)
    
    db.commit()
    db.refresh(db_goal)
    return db_goal


@router.delete("/{goal_id}")
async def delete_learning_goal(
    goal_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(auth.require_admin)
):
    """Delete a learning goal (admin only)"""
    db_goal = db.query(models.LearningGoal).filter(models.LearningGoal.id == goal_id).first()
    if not db_goal:
        raise HTTPException(status_code=404, detail="Learning goal not found")
    
    db.delete(db_goal)
    db.commit()
    return {"message": "Learning goal deleted"}
