import random
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from sqlalchemy.orm import Session
from app.models import School, Class, Subject, Teacher, Timetable, ECA, Lab
from app.schemas import TeacherWorkload, SubstituteTeacherResponse

class TimetableService:
    def __init__(self):
        # Board curricula with stream-based subjects for 11-12
        self.board_subjects = {
            "CBSE": {
                1: ["English", "Hindi", "Mathematics", "EVS", "Art", "Physical Education", "REGIONAL_LANGUAGE"],
                2: ["English", "Hindi", "Mathematics", "EVS", "Art", "Physical Education", "REGIONAL_LANGUAGE"],
                3: ["English", "Hindi", "Mathematics", "EVS", "Art", "Physical Education", "REGIONAL_LANGUAGE"],
                4: ["English", "Hindi", "Mathematics", "EVS", "Art", "Physical Education", "REGIONAL_LANGUAGE"],
                5: ["English", "Hindi", "Mathematics", "EVS", "Art", "Physical Education", "REGIONAL_LANGUAGE"],
                6: ["English", "Hindi", "Mathematics", "Science", "Social Science", "Art", "Physical Education", "REGIONAL_LANGUAGE"],
                7: ["English", "Hindi", "Mathematics", "Science", "Social Science", "Art", "Physical Education", "REGIONAL_LANGUAGE"],
                8: ["English", "Hindi", "Mathematics", "Science", "Social Science", "Art", "Physical Education", "REGIONAL_LANGUAGE"],
                9: ["English", "Hindi", "Mathematics", "Science", "Social Science", "Physical Education", "Computer Science", "REGIONAL_LANGUAGE"],
                10: ["English", "Hindi", "Mathematics", "Science", "Social Science", "Physical Education", "Computer Science", "REGIONAL_LANGUAGE"],
            },
            "ICSE": {
                1: ["English", "Hindi", "Mathematics", "EVS", "Art", "Physical Education", "REGIONAL_LANGUAGE"],
                2: ["English", "Hindi", "Mathematics", "EVS", "Art", "Physical Education", "REGIONAL_LANGUAGE"],
                3: ["English", "Hindi", "Mathematics", "EVS", "Art", "Physical Education", "REGIONAL_LANGUAGE"],
                4: ["English", "Hindi", "Mathematics", "EVS", "Art", "Physical Education", "REGIONAL_LANGUAGE"],
                5: ["English", "Hindi", "Mathematics", "EVS", "Art", "Physical Education", "REGIONAL_LANGUAGE"],
                6: ["English", "Hindi", "Mathematics", "Science", "History", "Geography", "Art", "Physical Education", "REGIONAL_LANGUAGE"],
                7: ["English", "Hindi", "Mathematics", "Science", "History", "Geography", "Art", "Physical Education", "REGIONAL_LANGUAGE"],
                8: ["English", "Hindi", "Mathematics", "Science", "History", "Geography", "Art", "Physical Education", "REGIONAL_LANGUAGE"],
                9: ["English", "Hindi", "Mathematics", "Physics", "Chemistry", "Biology", "History", "Geography", "Computer Applications", "REGIONAL_LANGUAGE"],
                10: ["English", "Hindi", "Mathematics", "Physics", "Chemistry", "Biology", "History", "Geography", "Computer Applications", "REGIONAL_LANGUAGE"],
            },
            "State Board": {
                1: ["English", "Regional Language", "Mathematics", "EVS", "Art", "Physical Education", "REGIONAL_LANGUAGE"],
                2: ["English", "Regional Language", "Mathematics", "EVS", "Art", "Physical Education", "REGIONAL_LANGUAGE"],
                3: ["English", "Regional Language", "Mathematics", "EVS", "Art", "Physical Education", "REGIONAL_LANGUAGE"],
                4: ["English", "Regional Language", "Mathematics", "EVS", "Art", "Physical Education", "REGIONAL_LANGUAGE"],
                5: ["English", "Regional Language", "Mathematics", "EVS", "Art", "Physical Education", "REGIONAL_LANGUAGE"],
                6: ["English", "Regional Language", "Mathematics", "Science", "Social Science", "Art", "Physical Education", "REGIONAL_LANGUAGE"],
                7: ["English", "Regional Language", "Mathematics", "Science", "Social Science", "Art", "Physical Education", "REGIONAL_LANGUAGE"],
                8: ["English", "Regional Language", "Mathematics", "Science", "Social Science", "Art", "Physical Education", "REGIONAL_LANGUAGE"],
                9: ["English", "Regional Language", "Mathematics", "Science", "Social Science", "Physical Education", "REGIONAL_LANGUAGE"],
                10: ["English", "Regional Language", "Mathematics", "Science", "Social Science", "Physical Education", "REGIONAL_LANGUAGE"],
            }
        }

        # Stream-based subjects for classes 11-12
        self.stream_subjects = {
            "Science": {
                "core": ["English", "Physics", "Chemistry", "Mathematics", "REGIONAL_LANGUAGE"],
                "optional": ["Biology", "Computer Science", "Physical Education"],
                "labs": ["Physics Lab", "Chemistry Lab", "Biology Lab", "Computer Lab"]
            },
            "Commerce": {
                "core": ["English", "Accountancy", "Business Studies", "Economics", "REGIONAL_LANGUAGE"],
                "optional": ["Mathematics", "Computer Science", "Physical Education", "Entrepreneurship"],
                "labs": ["Computer Lab", "Business Lab"]
            },
            "Arts/Humanities": {
                "core": ["English", "History", "Political Science", "Geography", "REGIONAL_LANGUAGE"],
                "optional": ["Psychology", "Sociology", "Economics", "Philosophy", "Physical Education"],
                "labs": ["Computer Lab", "Geography Lab"]
            }
        }

    def generate_timetables(self, db: Session, school_id: int, class_ids: List[int] = None) -> Dict[str, Any]:
        """Generate timetables for specified classes"""
        # Get school data
        school = db.query(School).filter(School.id == school_id).first()
        if not school:
            raise ValueError("School not found")
        
        # Get classes to generate timetables for
        if class_ids:
            classes = db.query(Class).filter(Class.id.in_(class_ids), Class.school_id == school_id).all()
        else:
            classes = db.query(Class).filter(Class.school_id == school_id).all()
        
        if not classes:
            raise ValueError("No classes found")
        
        # Clear existing timetables for these classes
        for class_obj in classes:
            db.query(Timetable).filter(Timetable.class_id == class_obj.id).delete()
        
        generated_timetables = {}
        
        for class_obj in classes:
            timetable = self._create_class_timetable(db, class_obj, school)
            generated_timetables[f"Class {class_obj.class_number}"] = timetable
            
            # Save to database
            self._save_timetable_to_db(db, class_obj.id, timetable)
        
        db.commit()
        return generated_timetables

    def _create_class_timetable(self, db: Session, class_obj: Class, school: School) -> Dict[str, List[Dict]]:
        """Create timetable for a specific class"""
        class_num = class_obj.class_number
        working_days = school.working_days
        
        # Determine timings based on class level
        if class_num <= 5:
            timings = school.primary_timings or {}
        elif class_num <= 10:
            timings = school.secondary_timings or {}
        else:  # 11-12
            timings = school.senior_secondary_timings or {}
        
        # Get subjects for this class
        subjects = self._get_class_subjects(db, class_obj, school)
        
        # Get teachers for this class
        class_teachers = self._get_class_teachers(db, class_obj.id, subjects)
        
        if not class_teachers:
            return {}
        
        # Create time slots
        time_slots = self._create_time_slots(timings)
        
        # Generate timetable for each day
        timetable = {}
        pe_periods_assigned = 0
        
        for day_idx, day in enumerate(working_days):
            timetable[day] = []
            
            # Create varied subject list for this day
            daily_subjects = [s for s in subjects if s != 'Physical Education']
            random.shuffle(daily_subjects)
            
            # Add PE with limitation (max 2 periods per week)
            if 'Physical Education' in subjects and pe_periods_assigned < 2:
                if day in ['Tuesday', 'Thursday'] or (pe_periods_assigned == 0 and day_idx >= len(working_days) - 2):
                    if len(time_slots) > 2:
                        pe_position = random.randint(1, min(len(time_slots) - 2, 4))
                        daily_subjects.insert(pe_position, 'Physical Education')
                        pe_periods_assigned += 1
            
            # Extend subject list to cover all periods
            while len(daily_subjects) < len(time_slots):
                daily_subjects.extend([s for s in subjects if s != 'Physical Education'])
            
            subject_index = 0
            
            for slot in time_slots:
                if slot['type'] == 'break':
                    timetable[day].append({
                        'time': f"{slot['start']}-{slot['end']}",
                        'subject': slot['period'],
                        'type': 'break'
                    })
                else:
                    if subject_index < len(daily_subjects):
                        subject = daily_subjects[subject_index]
                        teacher = class_teachers.get(subject, 'TBD')
                        timetable[day].append({
                            'time': f"{slot['start']}-{slot['end']}",
                            'subject': subject,
                            'teacher': teacher,
                            'type': 'period'
                        })
                        subject_index += 1
                    else:
                        timetable[day].append({
                            'time': f"{slot['start']}-{slot['end']}",
                            'subject': 'Free Period',
                            'type': 'period'
                        })
        
        # Add ECA if present
        eca = db.query(ECA).filter(ECA.class_id == class_obj.id).first()
        if eca:
            if eca.day in timetable:
                timetable[eca.day].append({
                    'time': eca.time,
                    'subject': 'ECA',
                    'type': 'eca'
                })
        
        # Add Lab Activities for higher secondary classes
        lab = db.query(Lab).filter(Lab.class_id == class_obj.id).first()
        if lab:
            stream = class_obj.stream or 'Science'
            lab_subjects = self.stream_subjects.get(stream, {}).get('labs', ['Lab'])
            
            for day in lab.days:
                if day in timetable:
                    lab_subject = random.choice(lab_subjects)
                    timetable[day].append({
                        'time': lab.time,
                        'subject': lab_subject,
                        'type': 'lab'
                    })
        
        # Add extra class for senior secondary
        if class_num >= 11 and school.extra_class_enabled and school.extra_class_timing:
            for day in working_days:
                timetable[day].append({
                    'time': school.extra_class_timing,
                    'subject': 'Extra Class',
                    'type': 'extra_class'
                })
        
        return timetable

    def _get_class_subjects(self, db: Session, class_obj: Class, school: School) -> List[str]:
        """Get subjects for a specific class"""
        if class_obj.class_number >= 11:
            # For classes 11-12, use stream-based subjects
            stream = class_obj.stream or 'Science'
            stream_data = self.stream_subjects.get(stream, {})
            return stream_data.get('core', []) + stream_data.get('optional', [])
        else:
            # For classes 1-10, use board-based subjects
            board = school.board
            if board in self.board_subjects and class_obj.class_number in self.board_subjects[board]:
                subjects = self.board_subjects[board][class_obj.class_number].copy()
                # Replace REGIONAL_LANGUAGE placeholder
                if "REGIONAL_LANGUAGE" in subjects:
                    idx = subjects.index("REGIONAL_LANGUAGE")
                    subjects[idx] = school.regional_language
                return subjects
            return []

    def _get_class_teachers(self, db: Session, class_id: int, subjects: List[str]) -> Dict[str, str]:
        """Get teachers for a specific class and subjects"""
        teachers = {}
        for subject in subjects:
            # Find teacher who can teach this subject and this class
            teacher = db.query(Teacher).join(TeacherSubject).join(Subject).join(TeacherClass).filter(
                Subject.name == subject,
                TeacherClass.class_id == class_id
            ).first()
            
            if teacher:
                teachers[subject] = teacher.name
        
        return teachers

    def _create_time_slots(self, timings: Dict[str, Any]) -> List[Dict]:
        """Create time slots based on school timings"""
        try:
            start_time = datetime.strptime(timings.get('start_time', '9:00'), '%H:%M')
            period_duration = int(timings.get('period_duration', '40'))
            
            periods_per_day = 8  # Default
            time_slots = []
            current_time = start_time
            
            for period in range(1, periods_per_day + 1):
                end_time = current_time + timedelta(minutes=period_duration)
                time_slots.append({
                    'period': period,
                    'start': current_time.strftime('%H:%M'),
                    'end': end_time.strftime('%H:%M'),
                    'type': 'period'
                })
                current_time = end_time
                
                # Add breaks
                if period == int(timings.get('break1_after', '2')):
                    break_duration = int(timings.get('break1_duration', '15'))
                    current_time += timedelta(minutes=break_duration)
                    time_slots.append({
                        'period': f"Break 1",
                        'start': (current_time - timedelta(minutes=break_duration)).strftime('%H:%M'),
                        'end': current_time.strftime('%H:%M'),
                        'type': 'break'
                    })
                elif period == int(timings.get('lunch_after', '4')):
                    lunch_duration = int(timings.get('lunch_duration', '30'))
                    current_time += timedelta(minutes=lunch_duration)
                    time_slots.append({
                        'period': f"Lunch",
                        'start': (current_time - timedelta(minutes=lunch_duration)).strftime('%H:%M'),
                        'end': current_time.strftime('%H:%M'),
                        'type': 'break'
                    })
                elif period == int(timings.get('break2_after', '6')):
                    break_duration = int(timings.get('break2_duration', '15'))
                    current_time += timedelta(minutes=break_duration)
                    time_slots.append({
                        'period': f"Break 2",
                        'start': (current_time - timedelta(minutes=break_duration)).strftime('%H:%M'),
                        'end': current_time.strftime('%H:%M'),
                        'type': 'break'
                    })
        except:
            # Fallback to simple time slots
            time_slots = [
                {'period': 1, 'start': '9:00', 'end': '9:40', 'type': 'period'},
                {'period': 2, 'start': '9:40', 'end': '10:20', 'type': 'period'},
                {'period': 'Break 1', 'start': '10:20', 'end': '10:35', 'type': 'break'},
                {'period': 3, 'start': '10:35', 'end': '11:15', 'type': 'period'},
                {'period': 4, 'start': '11:15', 'end': '11:55', 'type': 'period'},
                {'period': 'Lunch', 'start': '11:55', 'end': '12:25', 'type': 'break'},
                {'period': 5, 'start': '12:25', 'end': '13:05', 'type': 'period'},
                {'period': 6, 'start': '13:05', 'end': '13:45', 'type': 'period'},
            ]
        
        return time_slots

    def _save_timetable_to_db(self, db: Session, class_id: int, timetable: Dict[str, List[Dict]]):
        """Save timetable to database"""
        for day, slots in timetable.items():
            for slot in slots:
                if slot['type'] == 'period':
                    db_timetable = Timetable(
                        class_id=class_id,
                        day=day,
                        time_slot=slot['time'],
                        subject_id=None,  # Will be updated when subjects are properly linked
                        teacher_id=None,  # Will be updated when teachers are properly linked
                        slot_type='period'
                    )
                    db.add(db_timetable)

    def calculate_teacher_workload(self, db: Session, teacher_id: int) -> TeacherWorkload:
        """Calculate workload analysis for a teacher"""
        teacher = db.query(Teacher).filter(Teacher.id == teacher_id).first()
        if not teacher:
            raise ValueError("Teacher not found")
        
        # Get teacher's timetable
        timetables = db.query(Timetable).filter(Timetable.teacher_id == teacher_id).all()
        
        if not timetables:
            return TeacherWorkload(
                teacher_id=teacher_id,
                teacher_name=teacher.name,
                total_periods=0,
                avg_periods_per_day=0.0,
                workload_status="No Data",
                daily_breakdown={}
            )
        
        # Count periods by day
        daily_breakdown = {}
        total_periods = 0
        
        for timetable in timetables:
            day = timetable.day
            if day not in daily_breakdown:
                daily_breakdown[day] = 0
            daily_breakdown[day] += 1
            total_periods += 1
        
        # Calculate average
        working_days = len(daily_breakdown)
        avg_periods = total_periods / working_days if working_days > 0 else 0
        
        # Determine workload status
        if avg_periods >= 6:
            status = "Heavy"
        elif avg_periods >= 4:
            status = "Moderate"
        else:
            status = "Light"
        
        return TeacherWorkload(
            teacher_id=teacher_id,
            teacher_name=teacher.name,
            total_periods=total_periods,
            avg_periods_per_day=avg_periods,
            workload_status=status,
            daily_breakdown=daily_breakdown
        )

    def find_substitute_teachers(self, db: Session, absent_teacher_id: int, day: str) -> List[SubstituteTeacherResponse]:
        """Find substitute teachers for an absent teacher on a specific day"""
        absent_teacher = db.query(Teacher).filter(Teacher.id == absent_teacher_id).first()
        if not absent_teacher:
            raise ValueError("Absent teacher not found")
        
        # Get absent teacher's schedule for the day
        absent_schedule = db.query(Timetable).filter(
            Timetable.teacher_id == absent_teacher_id,
            Timetable.day == day
        ).all()
        
        if not absent_schedule:
            return []
        
        substitute_responses = []
        
        for period in absent_schedule:
            # Find available substitute teachers for this period
            available_substitutes = []
            
            # Get all teachers who can teach the same subjects
            potential_substitutes = db.query(Teacher).join(TeacherSubject).join(Subject).filter(
                Subject.name == period.subject.name if period.subject else "Unknown"
            ).all()
            
            for substitute in potential_substitutes:
                if substitute.id == absent_teacher_id:
                    continue
                
                # Check if substitute is free at this time
                is_free = not db.query(Timetable).filter(
                    Timetable.teacher_id == substitute.id,
                    Timetable.day == day,
                    Timetable.time_slot == period.time_slot
                ).first()
                
                if is_free:
                    workload = self.calculate_teacher_workload(db, substitute.id)
                    available_substitutes.append(workload)
            
            # Sort by workload (lighter workload first)
            available_substitutes.sort(key=lambda x: x.avg_periods_per_day)
            
            substitute_responses.append(SubstituteTeacherResponse(
                period_time=period.time_slot,
                subject=period.subject.name if period.subject else "Unknown",
                class_name=f"Class {period.class_obj.class_number}",
                available_substitutes=available_substitutes[:5]  # Top 5 substitutes
            ))
        
        return substitute_responses
