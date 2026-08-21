import os
from utils.logger import write_log
from utils.file_analysis import analyze_file

MENU = """
========== CryptoLabX ==========
1. Encrypt
2. Decrypt
3. Attack
4. Analyze Dataset
5. Exit
================================
"""

while True:
    print(MENU)

    choice = input("Enter your choice: ")

    if choice == "1":
        print("\nEncrypt Module Coming Soon...\n")
        write_log("Encrypt")

    elif choice == "2":
        print("\nDecrypt Module Coming Soon...\n")
        write_log("Decrypt")

    elif choice == "3":
        print("\nAttack Module Coming Soon...\n")
        write_log("Attack")

    elif choice == "4":
        write_log("Analyze")

        filename = input("Enter filename from datasets folder: ")

        filepath = os.path.join("datasets", filename)

        if os.path.exists(filepath):
            analyze_file(filepath)
        else:
            print("File not found.")

    elif choice == "5":
        write_log("Exit")
        print("Goodbye!")
        break

    else:
        print("Invalid Choice")