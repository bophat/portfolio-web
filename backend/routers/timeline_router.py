from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .. import models, schemas, auth
from ..database import get_db

router = APIRouter(prefix="/api/timeline", tags=["Timeline"])


@router.get("/", response_model=List[schemas.TimelineItemResponse])
async def get_timeline_items(db: Session = Depends(get_db)):
    """Get all timeline items (public)"""
    items = db.query(models.TimelineItem).order_by(models.TimelineItem.sort_order.desc(), models.TimelineItem.id.desc()).all()
    return items


@router.post("/", response_model=schemas.TimelineItemResponse)
async def create_timeline_item(
    item: schemas.TimelineItemCreate,
    db: Session = Depends(get_db),
    current_user = Depends(auth.require_admin)
):
    """Create a timeline item (admin only)"""
    db_item = models.TimelineItem(**item.model_dump())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


@router.put("/{item_id}", response_model=schemas.TimelineItemResponse)
async def update_timeline_item(
    item_id: int,
    item_update: schemas.TimelineItemUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(auth.require_admin)
):
    """Update a timeline item (admin only)"""
    db_item = db.query(models.TimelineItem).filter(models.TimelineItem.id == item_id).first()
    if not db_item:
        raise HTTPException(status_code=404, detail="Timeline item not found")
    
    update_data = item_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_item, field, value)
    
    db.commit()
    db.refresh(db_item)
    return db_item


@router.delete("/{item_id}")
async def delete_timeline_item(
    item_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(auth.require_admin)
):
    """Delete a timeline item (admin only)"""
    db_item = db.query(models.TimelineItem).filter(models.TimelineItem.id == item_id).first()
    if not db_item:
        raise HTTPException(status_code=404, detail="Timeline item not found")
    
    db.delete(db_item)
    db.commit()
    return {"message": "Timeline item deleted"}
