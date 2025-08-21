from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models import Class, School
from app.schemas import ClassCreate, ClassUpdate, Class as ClassSchema

router = APIRouter()

@router.post("/", response_model=ClassSchema, status_code=status.HTTP_201_CREATED)
def create_class(class_data: ClassCreate, db: Session = Depends(get_db)):
    """Create a new class"""
    # Check if school exists
    school = db.query(School).filter(School.id == class_data.school_id).first()
    if not school:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="School not found"
        )
    
    # Check if class already exists in this school
    existing_class = db.query(Class).filter(
        Class.school_id == class_data.school_id,
        Class.class_number == class_data.class_number
    ).first()
    
    if existing_class:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Class already exists in this school"
        )
    
    db_class = Class(**class_data.dict())
    db.add(db_class)
    db.commit()
    db.refresh(db_class)
    return db_class

@router.get("/", response_model=List[ClassSchema])
def get_classes(school_id: int = None, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get all classes, optionally filtered by school"""
    query = db.query(Class)
    if school_id:
        query = query.filter(Class.school_id == school_id)
    
    classes = query.offset(skip).limit(limit).all()
    return classes

@router.get("/{class_id}", response_model=ClassSchema)
def get_class(class_id: int, db: Session = Depends(get_db)):
    """Get a specific class by ID"""
    class_obj = db.query(Class).filter(Class.id == class_id).first()
    if class_obj is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Class not found"
        )
    return class_obj

@router.put("/{class_id}", response_model=ClassSchema)
def update_class(class_id: int, class_data: ClassUpdate, db: Session = Depends(get_db)):
    """Update a class"""
    db_class = db.query(Class).filter(Class.id == class_id).first()
    if db_class is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Class not found"
        )
    
    # Update fields
    for field, value in class_data.dict(exclude_unset=True).items():
        setattr(db_class, field, value)
    
    db.commit()
    db.refresh(db_class)
    return db_class

@router.delete("/{class_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_class(class_id: int, db: Session = Depends(get_db)):
    """Delete a class"""
    db_class = db.query(Class).filter(Class.id == class_id).first()
    if db_class is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Class not found"
        )
    
    db.delete(db_class)
    db.commit()
    return None
