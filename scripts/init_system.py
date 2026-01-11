#!/usr/bin/env python3
"""
Initialization script for BEAST system
Demonstrates how to set up and use the framework
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from beast.core.factory import create_beast
from beast.core.models.user import User
from beast.core.models.hierarchy import HierarchyManager


def main():
    """Initialize and demonstrate the system"""
    print("=" * 60)
    print("BEAST Framework - Initialization")
    print("=" * 60)
    
    # Create and initialize the system
    print("\n[1] Initializing BEAST system...")
    beast = create_beast()
    
    # Get system information
    info = beast.get_system_info()
    print(f"\n[2] System initialized successfully!")
    print(f"    Departments: {', '.join(info['departments'])}")
    print(f"    Hierarchy ranks: {', '.join(info['hierarchy_ranks'])}")
    
    # Example: Create a user
    print("\n[3] Creating example users...")
    
    # Create a MAKS
    maks = User(
        id_number="123456789",
        full_name="יוסי כהן",
        rank_name="maks",
        department="hadracha",
        class_name="יא-1",
        hierarchy_manager=beast.hierarchy_manager
    )
    print(f"    Created: {maks.full_name} - {maks.display_rank}")
    
    # Create a student
    student = User(
        id_number="987654321",
        full_name="דני ישראלי",
        rank_name="shocher",
        class_name="יא-1",
        hierarchy_manager=beast.hierarchy_manager
    )
    print(f"    Created: {student.full_name} - {student.display_rank}")
    
    # Example: Use Hadracha department
    print("\n[4] Using הדרכה department...")
    hadracha = beast.registry.get_department("hadracha")
    if hadracha:
        # Create a class
        classroom = hadracha.create_class("יא-1", maks)
        print(f"    Created class: {classroom.class_name}")
        
        # Add student to class
        hadracha.add_student_to_class("יא-1", student)
        print(f"    Added student to class")
        print(f"    Class now has {classroom.get_student_count()} students")
    
    # Example: List automations
    print("\n[5] Available automations:")
    automations = beast.registry.list_automations()
    for dept, autos in automations.items():
        if autos:
            print(f"    {dept}: {', '.join(autos)}")
    
    print("\n" + "=" * 60)
    print("Initialization complete!")
    print("=" * 60)


if __name__ == "__main__":
    main()
