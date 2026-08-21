"""
Brute-Force Cryptanalysis with Dictionary Scoring
"""

import string
from shift_cipher import decrypt


def load_dictionary(filepath: str) -> set:
    """Load English words into a set for fast lookup."""
    
    with open(filepath, "r", encoding="utf-8") as f:
        return {
            line.strip().lower()
            for line in f
            if line.strip()
        }


def attack_dictionary(ciphertext: str, dictionary: set) -> dict:
    """Try all 26 Shift Cipher keys and select the best plaintext."""

    best_key = 0
    best_score = -1.0
    best_text = ""
    scores = {}

    # Try every possible key
    for key in range(26):

        # Decrypt using the current key
        decrypted = decrypt(ciphertext, key)

        # Remove punctuation
        clean_text = decrypted.translate(
            str.maketrans("", "", string.punctuation)
        )

        # Split plaintext into words
        tokens = [
            word.lower()
            for word in clean_text.split()
            if word.isalpha()
        ]

        # Calculate dictionary score
        if not tokens:
            score = 0.0
        else:
            valid_words = sum(
                1 for word in tokens
                if word in dictionary
            )

            score = valid_words / len(tokens)

        # Store score for this key
        scores[key] = score

        # Update best result
        if score > best_score:
            best_score = score
            best_key = key
            best_text = decrypted

    return {
        "predicted_key": best_key,
        "predicted_plaintext": best_text,
        "score": best_score,
        "all_scores": scores
    }


if __name__ == "__main__":

    # Load English dictionary
    dictionary_path = (
        "dictionary\\english_words.txt"
    )

    dictionary = load_dictionary(dictionary_path)

    # Ciphertext to attack
    ciphertext = "KHOOR ZRUOG"

    # Perform brute-force dictionary attack
    result = attack_dictionary(ciphertext, dictionary)

    # Display result
    print("Predicted Key:", result["predicted_key"])
    print("Plaintext:", result["predicted_plaintext"])
    print("Dictionary Score:", result["score"])

    print("\nScores for all keys:")

    for key, score in result["all_scores"].items():
        print(f"Key {key:2}: {score:.3f}")