from database import get_connection


def view_grades(student_id):
    conn = get_connection()
    cursor = conn.cursor()

    query = f"""
        SELECT subject, grade
        FROM grades
        WHERE student_id = {student_id}
    """

    cursor.execute(query)

    results = cursor.fetchall()

    conn.close()

    if not results:
        print("No grades found.")
        return

    print("\n===== Student Grades =====")

    for subject, grade in results:
        print(f"{subject}: {grade}")