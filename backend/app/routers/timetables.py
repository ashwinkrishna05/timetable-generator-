from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Dict, Any
from app.database import get_db
from app.models import Timetable, Class, School, Teacher
from app.schemas import TimetableGenerationRequest, TeacherWorkload, SubstituteTeacherRequest, SubstituteTeacherResponse
from app.services.timetable_service import TimetableService

router = APIRouter()
timetable_service = TimetableService()

@router.post("/generate", response_model=Dict[str, Any])
def generate_timetables(request: TimetableGenerationRequest, db: Session = Depends(get_db)):
    """Generate timetables for specified classes"""
    try:
        # For now, assume school_id = 1 (you can modify this based on your needs)
        school_id = 1
        timetables = timetable_service.generate_timetables(
            db=db, 
            school_id=school_id, 
            class_ids=request.class_ids
        )
        return {
            "message": "Timetables generated successfully",
            "timetables": timetables,
            "note": "Physical Education limited to 2 periods per week"
        }
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate timetables: {str(e)}"
        )

@router.get("/class/{class_id}", response_model=Dict[str, Any])
def get_class_timetable(class_id: int, db: Session = Depends(get_db)):
    """Get timetable for a specific class"""
    # Get class details
    class_obj = db.query(Class).filter(Class.id == class_id).first()
    if not class_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Class not found"
        )
    
    # Get timetable data
    timetables = db.query(Timetable).filter(Timetable.class_id == class_id).all()
    
    if not timetables:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No timetable found for this class"
        )
    
    # Organize by day
    timetable_by_day = {}
    for tt in timetables:
        if tt.day not in timetable_by_day:
            timetable_by_day[tt.day] = []
        
        timetable_by_day[tt.day].append({
            "time": tt.time_slot,
            "subject": tt.subject.name if tt.subject else "Unknown",
            "teacher": tt.teacher.name if tt.teacher else "TBD",
            "type": tt.slot_type
        })
    
    return {
        "class_id": class_id,
        "class_number": class_obj.class_number,
        "stream": class_obj.stream,
        "timetable": timetable_by_day
    }

@router.get("/teacher/{teacher_id}/workload", response_model=TeacherWorkload)
def get_teacher_workload(teacher_id: int, db: Session = Depends(get_db)):
    """Get workload analysis for a specific teacher"""
    try:
        workload = timetable_service.calculate_teacher_workload(db, teacher_id)
        return workload
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )

@router.post("/substitute", response_model=List[SubstituteTeacherResponse])
def find_substitute_teachers(request: SubstituteTeacherRequest, db: Session = Depends(get_db)):
    """Find substitute teachers for an absent teacher"""
    try:
        substitutes = timetable_service.find_substitute_teachers(
            db, 
            request.absent_teacher_id, 
            request.day
        )
        return substitutes
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )

@router.get("/export/{class_id}")
def export_timetable(class_id: int, format: str = "json", db: Session = Depends(get_db)):
    """Export timetable in various formats"""
    # Get class details
    class_obj = db.query(Class).filter(Class.id == class_id).first()
    if not class_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Class not found"
        )
    
    # Get timetable data
    timetables = db.query(Timetable).filter(Timetable.class_id == class_id).all()
    
    if not timetables:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No timetable found for this class"
        )
    
    # Organize by day
    timetable_by_day = {}
    for tt in timetables:
        if tt.day not in timetable_by_day:
            timetable_by_day[tt.day] = []
        
        timetable_by_day[tt.day].append({
            "time": tt.time_slot,
            "subject": tt.subject.name if tt.subject else "Unknown",
            "teacher": tt.teacher.name if tt.teacher else "TBD",
            "type": tt.slot_type
        })
    
    if format.lower() == "json":
        return {
            "class_id": class_id,
            "class_number": class_obj.class_number,
            "stream": class_obj.stream,
            "timetable": timetable_by_day
        }
    elif format.lower() == "csv":
        # Generate CSV format
        csv_content = "Day,Time,Subject,Teacher,Type\n"
        for day, slots in timetable_by_day.items():
            for slot in slots:
                csv_content += f"{day},{slot['time']},{slot['subject']},{slot['teacher']},{slot['type']}\n"
        
        return {"csv": csv_content}
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Unsupported format. Use 'json' or 'csv'"
        )

@router.get("/school/{school_id}/summary")
def get_school_timetable_summary(school_id: int, db: Session = Depends(get_db)):
    """Get summary of all timetables for a school"""
    # Get school
    school = db.query(School).filter(School.id == school_id).first()
    if not school:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="School not found"
        )
    
    # Get all classes
    classes = db.query(Class).filter(Class.school_id == school_id).all()
    
    summary = {
        "school_name": school.name,
        "total_classes": len(classes),
        "classes_with_timetables": 0,
        "total_teachers": 0,
        "working_days": school.working_days
    }
    
    for class_obj in classes:
        timetable_count = db.query(Timetable).filter(Timetable.class_id == class_obj.id).count()
        if timetable_count > 0:
            summary["classes_with_timetables"] += 1
    
    # Count teachers
    summary["total_teachers"] = db.query(Teacher).filter(Teacher.school_id == school_id).count()
    
    return summary
