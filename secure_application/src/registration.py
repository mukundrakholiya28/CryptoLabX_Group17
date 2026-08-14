from database import get_connection


def register_student():
    print("\n========== STUDENT REGISTRATION ==========")

    try:
        student_id = int(input("Enter Student ID: "))
    except ValueError:
        print("Invalid Student ID.")
        return

    name = input("Enter Name: ")
    email = input("Enter Email: ")
    phone = input("Enter Phone: ")
    address = input("Enter Address: ")
    password = input("Enter Password: ")

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT student_id FROM students WHERE student_id = ?",
        (student_id,)
    )

    if cursor.fetchone():
        print("\nStudent ID already exists.")
        conn.close()
        return

    cursor.execute("""
        INSERT INTO students
        (student_id, name, email, phone, address, password)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (student_id, name, email, phone, address, password))

    conn.commit()
    conn.close()

    print("\nRegistration successful!")