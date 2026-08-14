from database import initialize_database
from registration import register_student
from login import login_student
from grades import view_grades
from profile import update_profile


def student_dashboard(student_id):
    while True:

        print("\n========== STUDENT DASHBOARD ==========")
        print("1. View Grades")
        print("2. Update Profile")
        print("3. Logout")
        print("=======================================")

        choice = input("Enter your choice: ")

        if choice == "1":
            # INTENTIONALLY VULNERABLE: IDOR
            target_id = input(
                "Enter student ID whose grades you want to view: "
            )

            view_grades(target_id)

        elif choice == "2":
            # INTENTIONALLY VULNERABLE:
            # Allows authenticated user to modify another student's profile.
            target_id = input(
                "Enter student ID whose profile you want to update: "
            )

            update_profile(target_id)

        elif choice == "3":
            print("\nLogged out successfully.")
            break

        else:
            print("\nInvalid choice.")


def main():
    initialize_database()

    while True:

        print("\n====================================")
        print("          STUDENT PORTAL")
        print("====================================")
        print("1. Register")
        print("2. Login")
        print("3. Exit")
        print("====================================")

        choice = input("Enter your choice: ")

        if choice == "1":
            register_student()

        elif choice == "2":
            student_id = login_student()

            if student_id is not None:
                student_dashboard(student_id)

        elif choice == "3":
            print("\nThank you for using Student Portal.")
            break

        else:
            print("\nInvalid choice.")


if __name__ == "__main__":
    main()