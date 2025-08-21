from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models import Teacher, School, TeacherSubject, TeacherClass, Subject, Class
from app.schemas import TeacherCreate, TeacherUpdate, Teacher as TeacherSchema

router = APIRouter()

@router.post("/", response_model=TeacherSchema, status_code=status.HTTP_201_CREATED)
def create_teacher(teacher: TeacherCreate, db: Session = Depends(get_db)):
    """Create a new teacher"""
    # Check if school exists
    school = db.query(School).filter(School.id == teacher.school_id).first()
    if not school:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="School not found"
        )
    
    # Check if employee ID already exists
    existing_teacher = db.query(Teacher).filter(Teacher.employee_id == teacher.employee_id).first()
    if existing_teacher:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Employee ID already exists"
        )
    
    # Create teacher
    db_teacher = Teacher(
        name=teacher.name,
        employee_id=teacher.employee_id,
        email=teacher.email,
        qualification=teacher.qualification,
        school_id=teacher.school_id
    )
    db.add(db_teacher)
    db.flush()  # Get the ID without committing
    
    # Add teacher-subject relationships
    for subject_id in teacher.subjects:
        teacher_subject = TeacherSubject(
            teacher_id=db_teacher.id,
            subject_id=subject_id
        )
        db.add(teacher_subject)
    
    # Add teacher-class relationships
    for class_id in teacher.classes:
        teacher_class = TeacherClass(
            teacher_id=db_teacher.id,
            class_id=class_id
        )
        db.add(teacher_class)
    
    db.commit()
    db.refresh(db_teacher)
    return db_teacher

@router.get("/", response_model=List[TeacherSchema])
def get_teachers(school_id: int = None, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get all teachers, optionally filtered by school"""
    query = db.query(Teacher)
    if school_id:
        query = query.filter(Teacher.school_id == school_id)
    
    teachers = query.offset(skip).limit(limit).all()
    return teachers

@router.get("/{teacher_id}", response_model=TeacherSchema)
def get_teacher(teacher_id: int, db: Session = Depends(get_db)):
    """Get a specific teacher by ID"""
    teacher = db.query(Teacher).filter(Teacher.id == teacher_id).first()
    if teacher is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Teacher not found"
        )
    return teacher

@router.put("/{teacher_id}", response_model=TeacherSchema)
def update_teacher(teacher_id: int, teacher_data: TeacherUpdate, db: Session = Depends(get_db)):
    """Update a teacher"""
    db_teacher = db.query(Teacher).filter(Teacher.id == teacher_id).first()
    if db_teacher is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Teacher not found"
        )
    
    # Update basic fields
    for field, value in teacher_data.dict(exclude_unset=True).items():
        if field not in ['subjects', 'classes']:
            setattr(db_teacher, field, value)
    
    # Update subjects if provided
    if teacher_data.subjects is not None:
        # Remove existing subject relationships
        db.query(TeacherSubject).filter(TeacherSubject.teacher_id == teacher_id).delete()
        
        # Add new subject relationships
        for subject_id in teacher_data.subjects:
            teacher_subject = TeacherSubject(
                teacher_id=teacher_id,
                subject_id=subject_id
            )
            db.add(teacher_subject)
    
    # Update classes if provided
    if teacher_data.classes is not None:
        # Remove existing class relationships
        db.query(TeacherClass).filter(TeacherClass.teacher_id == teacher_id).delete()
        
        # Add new class relationships
        for class_id in teacher_data.classes:
            teacher_class = TeacherClass(
                teacher_id=teacher_id,
                class_id=class_id
            )
            db.add(teacher_class)
    
    db.commit()
    db.refresh(db_teacher)
    return db_teacher

@router.delete("/{teacher_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_teacher(teacher_id: int, db: Session = Depends(get_db)):
    """Delete a teacher"""
    db_teacher = db.query(Teacher).filter(Teacher.id == teacher_id).first()
    if db_teacher is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Teacher not found"
        )
    
    # Remove relationships
    db.query(TeacherSubject).filter(TeacherSubject.teacher_id == teacher_id).delete()
    db.query(TeacherClass).filter(TeacherClass.teacher_id == teacher_id).delete()
    
    db.delete(db_teacher)
    db.commit()
    return None

@router.get("/{teacher_id}/details")
def get_teacher_details(teacher_id: int, db: Session = Depends(get_db)):
    """Get detailed information about a teacher including subjects and classes"""
    teacher = db.query(Teacher).filter(Teacher.id == teacher_id).first()
    if teacher is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Teacher not found"
        )
    
    # Get subjects
    subjects = db.query(Subject).join(TeacherSubject).filter(
        TeacherSubject.teacher_id == teacher_id
    ).all()
    
    # Get classes
    classes = db.query(Class).join(TeacherClass).filter(
        TeacherClass.teacher_id == teacher_id
    ).all()
    
    return {
        "teacher": {
            "id": teacher.id,
            "name": teacher.name,
            "employee_id": teacher.employee_id,
            "email": teacher.email,
            "qualification": teacher.qualification,
            "school_id": teacher.school_id
        },
        "subjects": [{"id": s.id, "name": s.name} for s in subjects],
        "classes": [{"id": c.id, "class_number": c.class_number, "stream": c.stream} for c in classes]
    }
