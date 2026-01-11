"""
הדרכה - Education Department
Manages classes, MAKS, and students
"""

from typing import Dict, Any, List, Optional
from beast.departments.base_department import BaseDepartment
from beast.core.models.user import User
from beast.core.models.hierarchy import HierarchyManager


class ClassRoom:
    """Represents a classroom"""
    
    def __init__(self, class_name: str, maks: Optional[User] = None):
        self.class_name = class_name
        self.maks = maks
        self.students: List[User] = []
    
    def add_student(self, student: User):
        """Add a student to the class"""
        if not student.is_student():
            raise ValueError("רק תלמידים יכולים להיות מוספים לכיתה")
        self.students.append(student)
    
    def set_maks(self, maks: User):
        """Set the MAKS for this class"""
        if not maks.is_maks():
            raise ValueError("רק מק\"ס יכול להיות מפקד כיתה")
        self.maks = maks
    
    def get_student_count(self) -> int:
        """Get number of students in class"""
        return len(self.students)


class HadrachaDepartment(BaseDepartment):
    """מחלקת הדרכה - Education Department"""
    
    @property
    def name(self) -> str:
        return "הדרכה"
    
    @property
    def name_en(self) -> str:
        return "hadracha"
    
    def __init__(self, registry=None, event_system=None, 
                 hierarchy_manager: Optional[HierarchyManager] = None):
        super().__init__(registry, event_system)
        self.hierarchy_manager = hierarchy_manager
        self.classes: Dict[str, ClassRoom] = {}
    
    def initialize(self):
        """Initialize the department"""
        super().initialize()
        # Load existing classes if needed
        # In production, this would load from database
    
    def create_class(self, class_name: str, maks: User) -> ClassRoom:
        """
        Create a new class with a MAKS
        
        Args:
            class_name: Name of the class
            maks: User who is the MAKS
        
        Returns:
            Created ClassRoom instance
        """
        if class_name in self.classes:
            raise ValueError(f"הכיתה {class_name} כבר קיימת")
        
        if not maks.is_maks():
            raise ValueError("רק מק\"ס יכול לנהל כיתה")
        
        classroom = ClassRoom(class_name, maks)
        self.classes[class_name] = classroom
        
        # Emit event
        self.emit_event("class_created", {
            "class_name": class_name,
            "maks_id": maks.id_number,
            "maks_name": maks.full_name
        })
        
        return classroom
    
    def get_class(self, class_name: str) -> Optional[ClassRoom]:
        """Get a class by name"""
        return self.classes.get(class_name)
    
    def add_student_to_class(self, class_name: str, student: User):
        """Add a student to a class"""
        classroom = self.get_class(class_name)
        if not classroom:
            raise ValueError(f"הכיתה {class_name} לא נמצאה")
        
        classroom.add_student(student)
        student.class_name = class_name
        
        # Emit event
        self.emit_event("student_added_to_class", {
            "class_name": class_name,
            "student_id": student.id_number,
            "student_name": student.full_name
        })
    
    def get_available_automations(self) -> Dict[str, Any]:
        """Get available automations"""
        from beast.automation.jobs.daily_attendance import DailyAttendanceAutomation
        from beast.automation.jobs.grades_report import GradesReportAutomation
        
        return {
            "daily_attendance": DailyAttendanceAutomation(self),
            "grades_report": GradesReportAutomation(self),
            "class_schedule": None  # To be implemented
        }
    
    def _subscribe_to_events(self):
        """Subscribe to relevant events"""
        if self.event_system:
            # Subscribe to user creation to automatically assign to classes
            self.event_system.subscribe("user_created", self._on_user_created)
    
    def _on_user_created(self, event):
        """Handle user created event"""
        # If user is a student and has a class, add them
        user_data = event.data
        if user_data.get('rank_name') == 'shocher' and user_data.get('class_name'):
            # This would require user instance, so we'll handle it differently
            pass
