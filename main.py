import sqlite3


class Student:
    def __init__(self, name, age, course, grade):
        self.name = name
        self.age = age
        self.course = course
        self.grade = grade


class StudentManagementSystem:
    def __init__(self):
        self.connection = sqlite3.connect("students.db")
        self.cursor = self.connection.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS students (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                age INTEGER NOT NULL,
                course TEXT NOT NULL,
                grade REAL NOT NULL
            )
        """)

        self.connection.commit()

    def add_student(self):
        print("\n===== ADD STUDENT =====")

        name = input("Enter student name: ").strip()
        if not name:
            print("Name cannot be empty!")
            return

        try:
            age = int(input("Enter student age: "))

            if age <= 0:
                print("Age must be greater than zero!")
                return

            course = input("Enter course: ").strip()
            if not course:
                print("Course cannot be empty!")
                return

            grade = float(input("Enter student grade: "))

            if not 0 <= grade <= 100:
                print("Grade must be between 0 and 100!")
                return

            student = Student(name, age, course, grade)

            self.cursor.execute("""
                INSERT INTO students (name, age, course, grade)
                VALUES (?, ?, ?, ?)
            """, (
                student.name,
                student.age,
                student.course,
                student.grade
            ))

            self.connection.commit()
            print("\nStudent added successfully!")

        except ValueError:
            print("Please enter valid numerical values!")

    def view_students(self):
        print("\n===== ALL STUDENTS =====")

        self.cursor.execute("SELECT * FROM students")
        students = self.cursor.fetchall()

        if not students:
            print("No students found!")
            return

        for student in students:
            print(f"\nStudent ID: {student[0]}")
            print(f"Name: {student[1]}")
            print(f"Age: {student[2]}")
            print(f"Course: {student[3]}")
            print(f"Grade: {student[4]:.2f}")

    def search_student(self):
        print("\n===== SEARCH STUDENT =====")

        try:
            student_id = int(input("Enter student ID: "))

            self.cursor.execute(
                "SELECT * FROM students WHERE id = ?",
                (student_id,)
            )

            student = self.cursor.fetchone()

            if student:
                print("\nStudent found!")
                print(f"ID: {student[0]}")
                print(f"Name: {student[1]}")
                print(f"Age: {student[2]}")
                print(f"Course: {student[3]}")
                print(f"Grade: {student[4]:.2f}")
            else:
                print("Student not found!")

        except ValueError:
            print("Please enter a valid student ID!")

    def update_student(self):
        print("\n===== UPDATE STUDENT =====")

        try:
            student_id = int(input("Enter student ID to update: "))

            self.cursor.execute(
                "SELECT * FROM students WHERE id = ?",
                (student_id,)
            )

            student = self.cursor.fetchone()

            if not student:
                print("Student not found!")
                return

            print("\nLeave a field empty to keep its current value.")

            name = input(f"New name [{student[1]}]: ").strip()
            age_input = input(f"New age [{student[2]}]: ").strip()
            course = input(f"New course [{student[3]}]: ").strip()
            grade_input = input(f"New grade [{student[4]}]: ").strip()

            new_name = name if name else student[1]
            new_age = int(age_input) if age_input else student[2]
            new_course = course if course else student[3]
            new_grade = float(grade_input) if grade_input else student[4]

            if new_age <= 0:
                print("Age must be greater than zero!")
                return

            if not 0 <= new_grade <= 100:
                print("Grade must be between 0 and 100!")
                return

            self.cursor.execute("""
                UPDATE students
                SET name = ?, age = ?, course = ?, grade = ?
                WHERE id = ?
            """, (
                new_name,
                new_age,
                new_course,
                new_grade,
                student_id
            ))

            self.connection.commit()
            print("\nStudent updated successfully!")

        except ValueError:
            print("Please enter valid numerical values!")

    def delete_student(self):
        print("\n===== DELETE STUDENT =====")

        try:
            student_id = int(input("Enter student ID to delete: "))

            self.cursor.execute(
                "SELECT name FROM students WHERE id = ?",
                (student_id,)
            )

            student = self.cursor.fetchone()

            if not student:
                print("Student not found!")
                return

            confirmation = input(
                f"Delete {student[0]}? (yes/no): "
            ).strip().lower()

            if confirmation == "yes":
                self.cursor.execute(
                    "DELETE FROM students WHERE id = ?",
                    (student_id,)
                )

                self.connection.commit()
                print("Student deleted successfully!")

            else:
                print("Deletion cancelled.")

        except ValueError:
            print("Please enter a valid student ID!")

    def close(self):
        self.connection.close()


def main():
    system = StudentManagementSystem()

    while True:
        print("\n===== STUDENT MANAGEMENT SYSTEM =====")
        print("1. Add student")
        print("2. View all students")
        print("3. Search student")
        print("4. Update student")
        print("5. Delete student")
        print("6. Exit")

        choice = input("\nChoose an option (1-6): ").strip()

        if choice == "1":
            system.add_student()

        elif choice == "2":
            system.view_students()

        elif choice == "3":
            system.search_student()

        elif choice == "4":
            system.update_student()

        elif choice == "5":
            system.delete_student()

        elif choice == "6":
            system.close()
            print("\nThank you for using Student Management System!")
            break

        else:
            print("Invalid choice! Please select 1-6.")


if __name__ == "__main__":
    main()