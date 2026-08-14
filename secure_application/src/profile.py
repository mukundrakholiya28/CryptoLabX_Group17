from database import get_connection


def update_profile(target_student_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT name, email, phone, address
        FROM students
        WHERE student_id = ?
    """, (target_student_id,))

    student = cursor.fetchone()

    if not student:
        print("Student not found.")
        conn.close()
        return

    name, email, phone, address = student

    print("\n===== Current Profile =====")
    print(f"Student ID: {target_student_id}")
    print(f"Name: {name}")
    print(f"Email: {email}")
    print(f"Phone: {phone}")
    print(f"Address: {address}")

    print("\nEnter new information:")

    new_email = input("Email: ")
    new_phone = input("Phone: ")
    new_address = input("Address: ")

    cursor.execute("""
        UPDATE students
        SET email = ?, phone = ?, address = ?
        WHERE student_id = ?
    """, (new_email, new_phone, new_address, target_student_id))

    conn.commit()
    conn.close()

    print("\nProfile updated successfully.")