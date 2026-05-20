import csv
import os
from datetime import datetime

# ===== BASIC DATA STRUCTURES =====

# ----- Introduction to list -----#
students = ['Marta','Antonio']
std_marks = [20, 15]
print("=== LISTS ===")
print("Hello", students[1], "Your marks is: ", std_marks[1])
print("Hello", students[0], "Your marks is: ", std_marks[0])

# ----- Introduction to tuples -----#
print("\n=== TUPLES (Immutable) ===")
students_tuple = ('Marta', 'Antonio')
std_marks_tuple = (12, 40)
print("Hello", students_tuple[1], "Your marks is: ", std_marks_tuple[1])
print("Hello", students_tuple[0], "Your marks is: ", std_marks_tuple[0])    

# ----- Introduction to dictionary -----#
print("\n=== DICTIONARY ===")
students_dict = {
    "name": "Miguel",
    "marks": 90,
    "age": 20,
}
print(students_dict)

# ===== CRUD OPERATIONS WITH IN-MEMORY DATA =====

class StudentManager:
    """Class to manage student data with CRUD operations"""
    
    def __init__(self):
        """Initialize with empty student list"""
        self.students = []
        self.csv_file = "students_data.csv"
    
    # CREATE - Add new student
    def add_student(self, name, marks, age):
        """Add a new student to the list"""
        student = {
            "id": len(self.students) + 1,
            "name": name,
            "marks": marks,
            "age": age,
            "date_added": datetime.now().strftime("%Y-%m-%d")
        }
        self.students.append(student)
        print(f"✓ Student {name} added successfully!")
        return student
    
    # READ - Get all students
    def get_all_students(self):
        """Retrieve all students"""
        return self.students
    
    # READ - Get student by ID
    def get_student(self, student_id):
        """Retrieve a specific student by ID"""
        for student in self.students:
            if student["id"] == student_id:
                return student
        return None
    
    # UPDATE - Modify student data
    def update_student(self, student_id, **kwargs):
        """Update student information"""
        student = self.get_student(student_id)
        if student:
            for key, value in kwargs.items():
                if key in student:
                    student[key] = value
            print(f"✓ Student ID {student_id} updated successfully!")
            return student
        print(f"✗ Student ID {student_id} not found!")
        return None
    
    # DELETE - Remove student
    def delete_student(self, student_id):
        """Remove a student from the list"""
        for i, student in enumerate(self.students):
            if student["id"] == student_id:
                removed = self.students.pop(i)
                print(f"✓ Student {removed['name']} deleted successfully!")
                return removed
        print(f"✗ Student ID {student_id} not found!")
        return None
    
    # Display all students
    def display_students(self):
        """Display all students in a formatted way"""
        if not self.students:
            print("No students in the database.")
            return
        
        print("\n" + "="*60)
        print(f"{'ID':<5} {'Name':<20} {'Marks':<8} {'Age':<5}")
        print("="*60)
        for student in self.students:
            print(f"{student['id']:<5} {student['name']:<20} {student['marks']:<8} {student['age']:<5}")
        print("="*60)
    
    # Save to CSV
    def save_to_csv(self):
        """Persist student data to CSV file"""
        if not self.students:
            print("No data to save.")
            return
        
        try:
            with open(self.csv_file, 'w', newline='') as file:
                fieldnames = ['id', 'name', 'marks', 'age', 'date_added']
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(self.students)
            print(f"✓ Data saved to {self.csv_file}")
        except Exception as e:
            print(f"✗ Error saving to CSV: {e}")
    
    # Load from CSV
    def load_from_csv(self):
        """Load student data from CSV file"""
        if not os.path.exists(self.csv_file):
            print(f"✗ File {self.csv_file} not found.")
            return
        
        try:
            with open(self.csv_file, 'r') as file:
                reader = csv.DictReader(file)
                self.students = []
                for row in reader:
                    row['id'] = int(row['id'])
                    row['marks'] = int(row['marks'])
                    row['age'] = int(row['age'])
                    self.students.append(row)
            print(f"✓ Data loaded from {self.csv_file}")
        except Exception as e:
            print(f"✗ Error loading from CSV: {e}")

# ===== DEMONSTRATION =====

print("\n" + "="*60)
print("STUDENT MANAGEMENT SYSTEM - CRUD OPERATIONS")
print("="*60)

# Create manager instance
manager = StudentManager()

# CREATE operations
print("\n--- CREATE Operations ---")
manager.add_student("Alice", 95, 20)
manager.add_student("Bob", 87, 21)
manager.add_student("Charlie", 92, 20)
manager.add_student("Diana", 88, 22)

# READ operations
print("\n--- READ Operations ---")
manager.display_students()

print("\nGet specific student (ID=2):")
student = manager.get_student(2)
print(student)

# UPDATE operation
print("\n--- UPDATE Operations ---")
manager.update_student(2, marks=90, age=22)
manager.display_students()

# DELETE operation
print("\n--- DELETE Operations ---")
manager.delete_student(3)
manager.display_students()

# Save to CSV
print("\n--- SAVE TO CSV ---")
manager.save_to_csv()