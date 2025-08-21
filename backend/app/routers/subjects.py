from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models import Subject
from app.schemas import SubjectCreate, SubjectUpdate, Subject as SubjectSchema

router = APIRouter()

@router.post("/", response_model=SubjectSchema, status_code=status.HTTP_201_CREATED)
def create_subject(subject: SubjectCreate, db: Session = Depends(get_db)):
    """Create a new subject"""
    # Check if subject with same name already exists
    existing_subject = db.query(Subject).filter(Subject.name == subject.name).first()
    if existing_subject:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Subject with this name already exists"
        )
    
    db_subject = Subject(**subject.dict())
    db.add(db_subject)
    db.commit()
    db.refresh(db_subject)
    return db_subject

@router.get("/", response_model=List[SubjectSchema])
def get_subjects(subject_type: str = None, stream: str = None, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get all subjects, optionally filtered by type or stream"""
    query = db.query(Subject)
    
    if subject_type:
        query = query.filter(Subject.subject_type == subject_type)
    
    if stream:
        query = query.filter(Subject.stream == stream)
    
    subjects = query.offset(skip).limit(limit).all()
    return subjects

@router.get("/{subject_id}", response_model=SubjectSchema)
def get_subject(subject_id: int, db: Session = Depends(get_db)):
    """Get a specific subject by ID"""
    subject = db.query(Subject).filter(Subject.id == subject_id).first()
    if subject is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Subject not found"
        )
    return subject

@router.put("/{subject_id}", response_model=SubjectSchema)
def update_subject(subject_id: int, subject_data: SubjectUpdate, db: Session = Depends(get_db)):
    """Update a subject"""
    db_subject = db.query(Subject).filter(Subject.id == subject_id).first()
    if db_subject is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Subject not found"
        )
    
    # Update fields
    for field, value in subject_data.dict(exclude_unset=True).items():
        setattr(db_subject, field, value)
    
    db.commit()
    db.refresh(db_subject)
    return db_subject

@router.delete("/{subject_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_subject(subject_id: int, db: Session = Depends(get_db)):
    """Delete a subject"""
    db_subject = db.query(Subject).filter(Subject.id == subject_id).first()
    if db_subject is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Subject not found"
        )
    
    db.delete(db_subject)
    db.commit()
    return None

@router.get("/types/list")
def get_subject_types():
    """Get list of available subject types"""
    return {
        "types": ["core", "optional", "lab"],
        "streams": ["Science", "Commerce", "Arts/Humanities"]
    }
