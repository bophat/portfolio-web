from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .. import models, schemas, auth
from ..database import get_db

router = APIRouter(prefix="/api/contact", tags=["Contact Info"])


@router.get("/", response_model=List[schemas.ContactInfoResponse])
async def get_contact_info(db: Session = Depends(get_db)):
    """Get all contact info (public)"""
    contacts = db.query(models.ContactInfo).order_by(models.ContactInfo.sort_order).all()
    return contacts


@router.post("/", response_model=schemas.ContactInfoResponse)
async def create_contact_info(
    contact: schemas.ContactInfoCreate,
    db: Session = Depends(get_db),
    current_user = Depends(auth.require_admin)
):
    """Create contact info (admin only)"""
    db_contact = models.ContactInfo(**contact.model_dump())
    db.add(db_contact)
    db.commit()
    db.refresh(db_contact)
    return db_contact


@router.put("/{contact_id}", response_model=schemas.ContactInfoResponse)
async def update_contact_info(
    contact_id: int,
    contact_update: schemas.ContactInfoUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(auth.require_admin)
):
    """Update contact info (admin only)"""
    db_contact = db.query(models.ContactInfo).filter(models.ContactInfo.id == contact_id).first()
    if not db_contact:
        raise HTTPException(status_code=404, detail="Contact info not found")
    
    update_data = contact_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_contact, field, value)
    
    db.commit()
    db.refresh(db_contact)
    return db_contact


@router.delete("/{contact_id}")
async def delete_contact_info(
    contact_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(auth.require_admin)
):
    """Delete contact info (admin only)"""
    db_contact = db.query(models.ContactInfo).filter(models.ContactInfo.id == contact_id).first()
    if not db_contact:
        raise HTTPException(status_code=404, detail="Contact info not found")
    
    db.delete(db_contact)
    db.commit()
    return {"message": "Contact info deleted"}


# Quick Facts routes
@router.get("/quick-facts", response_model=List[schemas.QuickFactResponse])
async def get_quick_facts(db: Session = Depends(get_db)):
    """Get all quick facts (public)"""
    facts = db.query(models.QuickFact).order_by(models.QuickFact.sort_order).all()
    return facts


@router.post("/quick-facts", response_model=schemas.QuickFactResponse)
async def create_quick_fact(
    fact: schemas.QuickFactCreate,
    db: Session = Depends(get_db),
    current_user = Depends(auth.require_admin)
):
    """Create a quick fact (admin only)"""
    db_fact = models.QuickFact(**fact.model_dump())
    db.add(db_fact)
    db.commit()
    db.refresh(db_fact)
    return db_fact


@router.put("/quick-facts/{fact_id}", response_model=schemas.QuickFactResponse)
async def update_quick_fact(
    fact_id: int,
    fact_update: schemas.QuickFactUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(auth.require_admin)
):
    """Update a quick fact (admin only)"""
    db_fact = db.query(models.QuickFact).filter(models.QuickFact.id == fact_id).first()
    if not db_fact:
        raise HTTPException(status_code=404, detail="Quick fact not found")
    
    update_data = fact_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_fact, field, value)
    
    db.commit()
    db.refresh(db_fact)
    return db_fact


@router.delete("/quick-facts/{fact_id}")
async def delete_quick_fact(
    fact_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(auth.require_admin)
):
    """Delete a quick fact (admin only)"""
    db_fact = db.query(models.QuickFact).filter(models.QuickFact.id == fact_id).first()
    if not db_fact:
        raise HTTPException(status_code=404, detail="Quick fact not found")
    
    db.delete(db_fact)
    db.commit()
    return {"message": "Quick fact deleted"}


# About Info routes
@router.get("/about", response_model=schemas.AboutInfoResponse)
async def get_about_info(db: Session = Depends(get_db)):
    """Get about info (public)"""
    about = db.query(models.AboutInfo).first()
    if not about:
        about = models.AboutInfo()
        db.add(about)
        db.commit()
        db.refresh(about)
    return about


@router.put("/about", response_model=schemas.AboutInfoResponse)
async def update_about_info(
    about_update: schemas.AboutInfoUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(auth.require_admin)
):
    """Update about info (admin only)"""
    about = db.query(models.AboutInfo).first()
    if not about:
        about = models.AboutInfo()
        db.add(about)
    
    update_data = about_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(about, field, value)
    
    db.commit()
    db.refresh(about)
    return about
