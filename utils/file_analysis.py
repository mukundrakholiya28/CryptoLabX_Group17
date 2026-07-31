from collections import Counter
import string


def analyze_file(filepath):

    with open(filepath, "r", encoding="utf-8") as file:
        text = file.read()

    characters = len(text)

    words = len(text.split())

    lines = len(text.splitlines())

    unique_characters = len(set(text))

    letters = [c.lower() for c in text if c.isalpha()]

    frequency = Counter(letters)

    print("\n========== File Analysis ==========")

    print(f"Characters       : {characters}")
    print(f"Words            : {words}")
    print(f"Lines            : {lines}")
    print(f"Unique Characters: {unique_characters}")

    print("\nLetter Frequency")

    for letter in string.ascii_lowercase:
        print(f"{letter} : {frequency.get(letter,0)}")

    print("===================================\n")