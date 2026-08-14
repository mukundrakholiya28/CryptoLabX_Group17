import sqlite3


DB_NAME = "student_portal.db"


def get_connection():
    return sqlite3.connect(DB_NAME)


def initialize_database():
    conn = get_connection()
    cursor = conn.cursor()

    # Student profile information
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS students (
        student_id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        email TEXT,
        phone TEXT,
        address TEXT,
        password TEXT NOT NULL
    )
""")

    # Student grades
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS grades (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER,
            subject TEXT NOT NULL,
            grade TEXT NOT NULL,
            FOREIGN KEY (student_id) REFERENCES students(student_id)
        )
    """)

    # Add sample students
    students = [
    (101, "Lakshay", "lakshay@gmail.com", "9876543210", "Jaipur", "lakshay123"),
    (102, "Rahul", "rahul@gmail.com", "9876543211", "Delhi", "rahul123"),
    (103, "Aman", "aman@gmail.com", "9876543212", "Mumbai", "aman123")
]

    cursor.executemany("""
    INSERT OR IGNORE INTO students
    (student_id, name, email, phone, address, password)
    VALUES (?, ?, ?, ?, ?, ?)
""", students)

    # Add sample grades
    grades = [
        (101, "DSA", "A"),
        (101, "DBMS", "A+"),
        (101, "OS", "B+"),
        (101, "Computer Networks", "A"),

        (102, "DSA", "B"),
        (102, "DBMS", "A"),
        (102, "OS", "A-"),

        (103, "DSA", "A+"),
        (103, "DBMS", "B+"),
        (103, "OS", "A")
    ]

    cursor.executemany("""
        INSERT OR IGNORE INTO grades
        (student_id, subject, grade)
        VALUES (?, ?, ?)
    """, grades)

    conn.commit()
    conn.close()