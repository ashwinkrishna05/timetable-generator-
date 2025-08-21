from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models import School
from app.schemas import SchoolCreate, SchoolUpdate, School as SchoolSchema

router = APIRouter()

@router.post("/", response_model=SchoolSchema, status_code=status.HTTP_201_CREATED)
def create_school(school: SchoolCreate, db: Session = Depends(get_db)):
    """Create a new school"""
    # Check if school with same name already exists
    existing_school = db.query(School).filter(School.name == school.name).first()
    if existing_school:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="School with this name already exists"
        )
    
    db_school = School(**school.dict())
    db.add(db_school)
    db.commit()
    db.refresh(db_school)
    return db_school

@router.get("/", response_model=List[SchoolSchema])
def get_schools(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get all schools"""
    schools = db.query(School).offset(skip).limit(limit).all()
    return schools

@router.get("/{school_id}", response_model=SchoolSchema)
def get_school(school_id: int, db: Session = Depends(get_db)):
    """Get a specific school by ID"""
    school = db.query(School).filter(School.id == school_id).first()
    if school is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="School not found"
        )
    return school

@router.put("/{school_id}", response_model=SchoolSchema)
def update_school(school_id: int, school: SchoolUpdate, db: Session = Depends(get_db)):
    """Update a school"""
    db_school = db.query(School).filter(School.id == school_id).first()
    if db_school is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="School not found"
        )
    
    # Update fields
    for field, value in school.dict(exclude_unset=True).items():
        setattr(db_school, field, value)
    
    db.commit()
    db.refresh(db_school)
    return db_school

@router.delete("/{school_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_school(school_id: int, db: Session = Depends(get_db)):
    """Delete a school"""
    db_school = db.query(School).filter(School.id == school_id).first()
    if db_school is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="School not found"
        )
    
    db.delete(db_school)
    db.commit()
    return None
