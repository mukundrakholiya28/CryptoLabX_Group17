from database import get_connection


def view_grades(student_id):
    conn = get_connection()
    cursor = conn.cursor()

    # INTENTIONALLY VULNERABLE:
    # User-controlled input is directly inserted into SQL.
    query = f"""
        SELECT subject, grade
        FROM grades
        WHERE student_id = {student_id}
    """

    cursor.execute(query)
    results = cursor.fetchall()

    conn.close()

    if not results:
        print("\nNo grades found.")
        return

    print("\n========== STUDENT GRADES ==========")

    for subject, grade in results:
        print(f"{subject:<25} {grade}")

    print("====================================")