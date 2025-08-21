from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Text, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class School(Base):
    __tablename__ = "schools"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    board = Column(String)  # CBSE, ICSE, State Board
    region = Column(String)
    regional_language = Column(String)
    
    # Timings stored as JSON
    primary_timings = Column(JSON)
    secondary_timings = Column(JSON)
    senior_secondary_timings = Column(JSON)
    
    working_days = Column(JSON)  # List of working days
    extra_class_enabled = Column(Boolean, default=False)
    extra_class_timing = Column(String)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    classes = relationship("Class", back_populates="school")
    teachers = relationship("Teacher", back_populates="school")

class Class(Base):
    __tablename__ = "classes"
    
    id = Column(Integer, primary_key=True, index=True)
    school_id = Column(Integer, ForeignKey("schools.id"))
    class_number = Column(Integer)
    sections = Column(JSON)  # List of sections like ["A", "B", "C"]
    no_sections = Column(Boolean, default=False)
    
    # For classes 11-12
    stream = Column(String)  # Science, Commerce, Arts/Humanities
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    school = relationship("School", back_populates="classes")
    subjects = relationship("ClassSubject", back_populates="class_obj")
    timetables = relationship("Timetable", back_populates="class_obj")

class Subject(Base):
    __tablename__ = "subjects"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    subject_type = Column(String)  # core, optional, lab
    stream = Column(String)  # For stream-specific subjects
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    class_subjects = relationship("ClassSubject", back_populates="subject")
    teacher_subjects = relationship("TeacherSubject", back_populates="subject")

class ClassSubject(Base):
    __tablename__ = "class_subjects"
    
    id = Column(Integer, primary_key=True, index=True)
    class_id = Column(Integer, ForeignKey("classes.id"))
    subject_id = Column(Integer, ForeignKey("subjects.id"))
    is_required = Column(Boolean, default=True)
    
    # Relationships
    class_obj = relationship("Class", back_populates="subjects")
    subject = relationship("Subject", back_populates="class_subjects")

class Teacher(Base):
    __tablename__ = "teachers"
    
    id = Column(Integer, primary_key=True, index=True)
    school_id = Column(Integer, ForeignKey("schools.id"))
    name = Column(String, index=True)
    employee_id = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    qualification = Column(String)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    school = relationship("School", back_populates="teachers")
    teacher_subjects = relationship("TeacherSubject", back_populates="teacher")
    teacher_classes = relationship("TeacherClass", back_populates="teacher")

class TeacherSubject(Base):
    __tablename__ = "teacher_subjects"
    
    id = Column(Integer, primary_key=True, index=True)
    teacher_id = Column(Integer, ForeignKey("teachers.id"))
    subject_id = Column(Integer, ForeignKey("subjects.id"))
    
    # Relationships
    teacher = relationship("Teacher", back_populates="teacher_subjects")
    subject = relationship("Subject", back_populates="teacher_subjects")

class TeacherClass(Base):
    __tablename__ = "teacher_classes"
    
    id = Column(Integer, primary_key=True, index=True)
    teacher_id = Column(Integer, ForeignKey("teachers.id"))
    class_id = Column(Integer, ForeignKey("classes.id"))
    
    # Relationships
    teacher = relationship("Teacher", back_populates="teacher_classes")
    class_obj = relationship("Class")

class Timetable(Base):
    __tablename__ = "timetables"
    
    id = Column(Integer, primary_key=True, index=True)
    class_id = Column(Integer, ForeignKey("classes.id"))
    day = Column(String)  # Monday, Tuesday, etc.
    time_slot = Column(String)  # 9:00-9:40
    subject_id = Column(Integer, ForeignKey("subjects.id"))
    teacher_id = Column(Integer, ForeignKey("teachers.id"))
    slot_type = Column(String)  # period, break, eca, lab, extra_class
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    class_obj = relationship("Class", back_populates="timetables")
    subject = relationship("Subject")
    teacher = relationship("Teacher")

class ECA(Base):
    __tablename__ = "ecas"
    
    id = Column(Integer, primary_key=True, index=True)
    class_id = Column(Integer, ForeignKey("classes.id"))
    day = Column(String)
    time = Column(String)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    class_obj = relationship("Class")

class Lab(Base):
    __tablename__ = "labs"
    
    id = Column(Integer, primary_key=True, index=True)
    class_id = Column(Integer, ForeignKey("classes.id"))
    days = Column(JSON)  # List of days
    time = Column(String)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    class_obj = relationship("Class")

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
