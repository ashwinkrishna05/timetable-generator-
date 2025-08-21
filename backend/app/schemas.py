from pydantic import BaseModel, EmailStr
from typing import Optional, List, Dict, Any
from datetime import datetime

# Base schemas
class SchoolBase(BaseModel):
    name: str
    board: str
    region: str
    regional_language: Optional[str] = None
    primary_timings: Optional[Dict[str, Any]] = None
    secondary_timings: Optional[Dict[str, Any]] = None
    senior_secondary_timings: Optional[Dict[str, Any]] = None
    working_days: List[str]
    extra_class_enabled: bool = False
    extra_class_timing: Optional[str] = None

class SchoolCreate(SchoolBase):
    pass

class SchoolUpdate(SchoolBase):
    pass

class School(SchoolBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

# Class schemas
class ClassBase(BaseModel):
    class_number: int
    sections: Optional[List[str]] = None
    no_sections: bool = False
    stream: Optional[str] = None

class ClassCreate(ClassBase):
    school_id: int

class ClassUpdate(ClassBase):
    pass

class Class(ClassBase):
    id: int
    school_id: int
    created_at: datetime

    class Config:
        from_attributes = True

# Subject schemas
class SubjectBase(BaseModel):
    name: str
    subject_type: str
    stream: Optional[str] = None

class SubjectCreate(SubjectBase):
    pass

class SubjectUpdate(SubjectBase):
    pass

class Subject(SubjectBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

# Teacher schemas
class TeacherBase(BaseModel):
    name: str
    employee_id: str
    email: Optional[EmailStr] = None
    qualification: Optional[str] = None

class TeacherCreate(TeacherBase):
    school_id: int
    subjects: List[int]  # List of subject IDs
    classes: List[int]   # List of class IDs

class TeacherUpdate(TeacherBase):
    subjects: Optional[List[int]] = None
    classes: Optional[List[int]] = None

class Teacher(TeacherBase):
    id: int
    school_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

# Timetable schemas
class TimetableBase(BaseModel):
    class_id: int
    day: str
    time_slot: str
    subject_id: Optional[int] = None
    teacher_id: Optional[int] = None
    slot_type: str

class TimetableCreate(TimetableBase):
    pass

class TimetableUpdate(TimetableBase):
    pass

class Timetable(TimetableBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

# ECA schemas
class ECABase(BaseModel):
    class_id: int
    day: str
    time: str

class ECACreate(ECABase):
    pass

class ECA(ECABase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

# Lab schemas
class LabBase(BaseModel):
    class_id: int
    days: List[str]
    time: str

class LabCreate(LabBase):
    pass

class Lab(LabBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

# User schemas
class UserBase(BaseModel):
    username: str
    email: EmailStr
    is_active: bool = True
    is_superuser: bool = False

class UserCreate(UserBase):
    password: str

class UserUpdate(UserBase):
    password: Optional[str] = None

class User(UserBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

# Authentication schemas
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

class UserLogin(BaseModel):
    username: str
    password: str

# Response schemas
class Message(BaseModel):
    message: str

class TimetableGenerationRequest(BaseModel):
    class_ids: List[int]
    regenerate: bool = False

class TeacherWorkload(BaseModel):
    teacher_id: int
    teacher_name: str
    total_periods: int
    avg_periods_per_day: float
    workload_status: str
    daily_breakdown: Dict[str, int]

class SubstituteTeacherRequest(BaseModel):
    absent_teacher_id: int
    day: str

class SubstituteTeacherResponse(BaseModel):
    period_time: str
    subject: str
    class_name: str
    available_substitutes: List[TeacherWorkload]
