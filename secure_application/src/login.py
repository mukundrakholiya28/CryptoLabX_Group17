from database import get_connection


def login_student():
    print("\n========== STUDENT LOGIN ==========")

    try:
        student_id = int(input("Student ID: "))
    except ValueError:
        print("Invalid Student ID.")
        return None

    password = input("Password: ")

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT student_id, name
        FROM students
        WHERE student_id = ? AND password = ?
    """, (student_id, password))

    student = cursor.fetchone()

    conn.close()

    if student:
        print(f"\nWelcome, {student[1]}!")
        return student[0]

    print("\nInvalid Student ID or Password.")
    return None