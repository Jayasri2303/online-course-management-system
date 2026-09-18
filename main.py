# ============================================================
# ONLINE COURSE MANAGEMENT SYSTEM
# Python + MySQL
# ============================================================

import mysql.connector
from datetime import date


# ============================================================
# DATABASE CONNECTION
# ============================================================

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="jsri2004",
        database="course_management_system"
    )


# ============================================================
# STUDENT REGISTRATION
# ============================================================

def student_register():

    print("\n--- Student Registration ---")

    name = input("Enter name: ")
    email = input("Enter email: ")
    password = input("Enter password: ")

    connection = get_connection()
    cursor = connection.cursor()

    query = """
    INSERT INTO users (name, email, password, role)
    VALUES (%s, %s, %s, %s)
    """

    try:
        cursor.execute(query, (name, email, password, "student"))
        connection.commit()

        print("Student registration successful!")

    except Exception as e:
        connection.rollback()
        print("Registration failed:", e)

    finally:
        cursor.close()
        connection.close()


# ============================================================
# STUDENT LOGIN
# ============================================================

def student_login():

    print("\n--- Student Login ---")

    email = input("Enter email: ")
    password = input("Enter password: ")

    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    query = """
    SELECT user_id, name, email, role
    FROM users
    WHERE email = %s
    AND password = %s
    AND role = 'student'
    """

    cursor.execute(query, (email, password))

    student = cursor.fetchone()

    if student:

        print("\nLogin successful!")
        print("Welcome", student["name"])

        cursor.close()
        connection.close()

        student_menu(student)

    else:

        print("Invalid email or password")

        cursor.close()
        connection.close()


# ============================================================
# VIEW COURSES
# ============================================================

def view_courses():

    print("\n--- Available Courses ---")

    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    query = """
    SELECT
        c.course_id,
        c.title,
        c.description,
        u.name AS instructor
    FROM courses c
    JOIN users u
        ON c.instructor_id = u.user_id
    """

    cursor.execute(query)

    courses = cursor.fetchall()

    if len(courses) == 0:

        print("No courses available")

    else:

        for course in courses:

            print("\nCourse ID:", course["course_id"])
            print("Title:", course["title"])
            print("Description:", course["description"])
            print("Instructor:", course["instructor"])

    cursor.close()
    connection.close()


# ============================================================
# ENROLL COURSE
# ============================================================

def enroll_course(student):

    view_courses()

    try:
        course_id = int(input("\nEnter Course ID: "))
    except ValueError:
        print("Please enter a valid Course ID")
        return

    connection = get_connection()
    cursor = connection.cursor()

    try:

        # Check course exists
        query = """
        SELECT course_id
        FROM courses
        WHERE course_id = %s
        """

        cursor.execute(query, (course_id,))

        course = cursor.fetchone()

        if course is None:

            print("Course not found")

            cursor.close()
            connection.close()

            return

        # Enroll student
        query = """
        INSERT INTO enrollments
        (student_id, course_id, enrollment_date)
        VALUES (%s, %s, %s)
        """

        cursor.execute(
            query,
            (
                student["user_id"],
                course_id,
                date.today()
            )
        )

        # Create progress record
        query = """
        INSERT INTO progress
        (student_id, course_id, progress_percentage)
        VALUES (%s, %s, %s)
        """

        cursor.execute(
            query,
            (
                student["user_id"],
                course_id,
                0
            )
        )

        connection.commit()

        print("Course enrollment successful!")

    except Exception as e:

        connection.rollback()

        print("Enrollment failed:", e)

    finally:

        cursor.close()
        connection.close()


# ============================================================
# VIEW MATERIALS
# ============================================================

def view_materials(student):

    print("\n--- Course Materials ---")

    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    query = """
    SELECT
        c.title AS course_title,
        m.title AS material_title,
        m.content
    FROM enrollments e
    JOIN courses c
        ON e.course_id = c.course_id
    JOIN materials m
        ON c.course_id = m.course_id
    WHERE e.student_id = %s
    """

    cursor.execute(query, (student["user_id"],))

    materials = cursor.fetchall()

    if len(materials) == 0:

        print("No materials available")

    else:

        for material in materials:

            print("\nCourse:", material["course_title"])
            print("Material:", material["material_title"])
            print("Content:", material["content"])

    cursor.close()
    connection.close()


# ============================================================
# UPDATE PROGRESS
# ============================================================

def update_progress(student):

    print("\n--- Update Progress ---")

    try:

        course_id = int(input("Enter Course ID: "))
        new_progress = int(
            input("Enter progress percentage: ")
        )

    except ValueError:

        print("Please enter numbers only")
        return

    if new_progress < 0 or new_progress > 100:

        print("Enter progress between 0 and 100")
        return

    connection = get_connection()
    cursor = connection.cursor()

    query = """
    UPDATE progress
    SET progress_percentage = %s
    WHERE student_id = %s
    AND course_id = %s
    """

    cursor.execute(
        query,
        (
            new_progress,
            student["user_id"],
            course_id
        )
    )

    connection.commit()

    if cursor.rowcount > 0:

        print("Progress updated successfully!")

    else:

        print("No progress record found.")

    cursor.close()
    connection.close()


# ============================================================
# VIEW PROGRESS
# ============================================================

def view_progress(student):

    print("\n--- My Progress ---")

    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    query = """
    SELECT
        c.title,
        p.progress_percentage
    FROM progress p
    JOIN courses c
        ON p.course_id = c.course_id
    WHERE p.student_id = %s
    """

    cursor.execute(query, (student["user_id"],))

    results = cursor.fetchall()

    if len(results) == 0:

        print("No progress available")

    else:

        for result in results:

            print("\nCourse:", result["title"])
            print(
                "Progress:",
                result["progress_percentage"],
                "%"
            )

    cursor.close()
    connection.close()


# ============================================================
# STUDENT MENU
# ============================================================

def student_menu(student):

    while True:

        print("\n==============================")
        print("       STUDENT MENU")
        print("==============================")

        print("1. View Courses")
        print("2. Enroll Course")
        print("3. View Materials")
        print("4. Update Progress")
        print("5. View Progress")
        print("6. Logout")

        choice = input("Enter your choice: ")

        if choice == "1":

            view_courses()

        elif choice == "2":

            enroll_course(student)

        elif choice == "3":

            view_materials(student)

        elif choice == "4":

            update_progress(student)

        elif choice == "5":

            view_progress(student)

        elif choice == "6":

            print("Student logged out")
            break

        else:

            print("Invalid choice")


# ============================================================
# INSTRUCTOR REGISTRATION
# ============================================================

def instructor_register():

    print("\n--- Instructor Registration ---")

    name = input("Enter name: ")
    email = input("Enter email: ")
    password = input("Enter password: ")

    connection = get_connection()
    cursor = connection.cursor()

    query = """
    INSERT INTO users (name, email, password, role)
    VALUES (%s, %s, %s, %s)
    """

    try:

        cursor.execute(
            query,
            (
                name,
                email,
                password,
                "instructor"
            )
        )

        connection.commit()

        print("Instructor registration successful!")

    except Exception as e:

        connection.rollback()

        print("Registration failed:", e)

    finally:

        cursor.close()
        connection.close()


# ============================================================
# INSTRUCTOR LOGIN
# ============================================================

def instructor_login():

    print("\n--- Instructor Login ---")

    email = input("Enter email: ")
    password = input("Enter password: ")

    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    query = """
    SELECT user_id, name, email, role
    FROM users
    WHERE email = %s
    AND password = %s
    AND role = 'instructor'
    """

    cursor.execute(query, (email, password))

    instructor = cursor.fetchone()

    if instructor:

        print("\nLogin successful!")
        print("Welcome", instructor["name"])

        cursor.close()
        connection.close()

        instructor_menu(instructor)

    else:

        print("Invalid email or password")

        cursor.close()
        connection.close()


# ============================================================
# CREATE COURSE
# ============================================================

def create_course(instructor):

    print("\n--- Create Course ---")

    title = input("Enter course title: ")
    description = input("Enter course description: ")

    connection = get_connection()
    cursor = connection.cursor()

    query = """
    INSERT INTO courses
    (title, description, instructor_id)
    VALUES (%s, %s, %s)
    """

    try:

        cursor.execute(
            query,
            (
                title,
                description,
                instructor["user_id"]
            )
        )

        connection.commit()

        print("Course created successfully!")
        print("Course ID:", cursor.lastrowid)

    except Exception as e:

        connection.rollback()

        print("Course creation failed:", e)

    finally:

        cursor.close()
        connection.close()


# ============================================================
# VIEW MY COURSES
# ============================================================

def view_my_courses(instructor):

    print("\n--- My Courses ---")

    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    query = """
    SELECT
        course_id,
        title,
        description
    FROM courses
    WHERE instructor_id = %s
    """

    cursor.execute(
        query,
        (instructor["user_id"],)
    )

    courses = cursor.fetchall()

    if len(courses) == 0:

        print("No courses created")

    else:

        for course in courses:

            print("\nCourse ID:", course["course_id"])
            print("Title:", course["title"])
            print("Description:", course["description"])

    cursor.close()
    connection.close()


# ============================================================
# UPDATE COURSE
# ============================================================

def update_course(instructor):

    view_my_courses(instructor)

    try:

        course_id = int(
            input("\nEnter Course ID to update: ")
        )

    except ValueError:

        print("Invalid Course ID")
        return

    new_title = input("Enter new title: ")
    new_description = input(
        "Enter new description: "
    )

    connection = get_connection()
    cursor = connection.cursor()

    query = """
    UPDATE courses
    SET title = %s,
        description = %s
    WHERE course_id = %s
    AND instructor_id = %s
    """

    cursor.execute(
        query,
        (
            new_title,
            new_description,
            course_id,
            instructor["user_id"]
        )
    )

    connection.commit()

    if cursor.rowcount > 0:

        print("Course updated successfully!")

    else:

        print("Course not found")

    cursor.close()
    connection.close()


# ============================================================
# DELETE COURSE
# ============================================================

def delete_course(instructor):

    view_my_courses(instructor)

    try:

        course_id = int(
            input("\nEnter Course ID to delete: ")
        )

    except ValueError:

        print("Invalid Course ID")
        return

    connection = get_connection()
    cursor = connection.cursor()

    try:

        # Delete progress records
        cursor.execute(
            """
            DELETE FROM progress
            WHERE course_id = %s
            """,
            (course_id,)
        )

        # Delete enrollment records
        cursor.execute(
            """
            DELETE FROM enrollments
            WHERE course_id = %s
            """,
            (course_id,)
        )

        # Delete materials
        cursor.execute(
            """
            DELETE FROM materials
            WHERE course_id = %s
            """,
            (course_id,)
        )

        # Delete course
        cursor.execute(
            """
            DELETE FROM courses
            WHERE course_id = %s
            AND instructor_id = %s
            """,
            (
                course_id,
                instructor["user_id"]
            )
        )

        if cursor.rowcount > 0:

            connection.commit()

            print("Course deleted successfully!")

        else:

            connection.rollback()

            print("Course not found")

    except Exception as e:

        connection.rollback()

        print("Delete failed:", e)

    finally:

        cursor.close()
        connection.close()


# ============================================================
# ADD MATERIAL
# ============================================================

def add_material(instructor):

    view_my_courses(instructor)

    try:

        course_id = int(
            input("\nEnter Course ID: ")
        )

    except ValueError:

        print("Invalid Course ID")
        return

    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    # Check course belongs to instructor
    query = """
    SELECT course_id
    FROM courses
    WHERE course_id = %s
    AND instructor_id = %s
    """

    cursor.execute(
        query,
        (
            course_id,
            instructor["user_id"]
        )
    )

    course = cursor.fetchone()

    if course is None:

        print("Course not found")

        cursor.close()
        connection.close()

        return

    title = input("Enter material title: ")
    content = input("Enter material content: ")

    cursor = connection.cursor()

    query = """
    INSERT INTO materials
    (course_id, title, content)
    VALUES (%s, %s, %s)
    """

    try:

        cursor.execute(
            query,
            (
                course_id,
                title,
                content
            )
        )

        connection.commit()

        print(
            "Learning material added successfully!"
        )

    except Exception as e:

        connection.rollback()

        print("Material addition failed:", e)

    finally:

        cursor.close()
        connection.close()


# ============================================================
# VIEW ENROLLED STUDENTS
# ============================================================

def view_enrolled_students(instructor):

    print("\n--- Enrolled Students ---")

    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    query = """
    SELECT
        c.title AS course_title,
        u.name AS student_name,
        u.email AS student_email
    FROM enrollments e

    JOIN courses c
        ON e.course_id = c.course_id

    JOIN users u
        ON e.student_id = u.user_id

    WHERE c.instructor_id = %s
    """

    cursor.execute(
        query,
        (instructor["user_id"],)
    )

    students = cursor.fetchall()

    if len(students) == 0:

        print("No students enrolled")

    else:

        for student in students:

            print(
                "\nCourse:",
                student["course_title"]
            )

            print(
                "Student:",
                student["student_name"]
            )

            print(
                "Email:",
                student["student_email"]
            )

    cursor.close()
    connection.close()


# ============================================================
# INSTRUCTOR MENU
# ============================================================

def instructor_menu(instructor):

    while True:

        print("\n==============================")
        print("      INSTRUCTOR MENU")
        print("==============================")

        print("1. Create Course")
        print("2. View My Courses")
        print("3. Update Course")
        print("4. Delete Course")
        print("5. Add Learning Material")
        print("6. View Enrolled Students")
        print("7. Logout")

        choice = input("Enter your choice: ")

        if choice == "1":

            create_course(instructor)

        elif choice == "2":

            view_my_courses(instructor)

        elif choice == "3":

            update_course(instructor)

        elif choice == "4":

            delete_course(instructor)

        elif choice == "5":

            add_material(instructor)

        elif choice == "6":

            view_enrolled_students(instructor)

        elif choice == "7":

            print("Instructor logged out")
            break

        else:

            print("Invalid choice")


# ============================================================
# MAIN MENU
# ============================================================

def main():

    while True:

        print("\n======================================")
        print("   ONLINE COURSE MANAGEMENT SYSTEM")
        print("======================================")

        print("1. Student")
        print("2. Instructor")
        print("3. Exit")

        choice = input("Enter your choice: ")

        # ---------------- STUDENT ----------------

        if choice == "1":

            print("\n--- STUDENT ---")

            print("1. Register")
            print("2. Login")

            student_choice = input(
                "Enter your choice: "
            )

            if student_choice == "1":

                student_register()

            elif student_choice == "2":

                student_login()

            else:

                print("Invalid choice")

        # ---------------- INSTRUCTOR ----------------

        elif choice == "2":

            print("\n--- INSTRUCTOR ---")

            print("1. Register")
            print("2. Login")

            instructor_choice = input(
                "Enter your choice: "
            )

            if instructor_choice == "1":

                instructor_register()

            elif instructor_choice == "2":

                instructor_login()

            else:

                print("Invalid choice")

        # ---------------- EXIT ----------------

        elif choice == "3":

            print(
                "\nThank you for using "
                "Online Course Management System!"
            )

            break

        else:

            print("Invalid choice")


# ============================================================
# PROGRAM START
# ============================================================

if __name__ == "__main__":

    try:

        connection = get_connection()

        if connection.is_connected():

            print("Database connected successfully!")

        connection.close()

        main()

    except Exception as e:

        print("\nDatabase connection failed!")
        print("Error:", e)
