"""
Brute-Force Cryptanalysis with Dictionary Scoring
"""

import string
from shift_cipher import decrypt


def load_dictionary(filepath: str) -> set:
    """Loads wordlist into a hash set for O(1) membership lookups."""
    with open(filepath, "r", encoding="utf-8") as f:
        return {line.strip().lower() for line in f if line.strip()}


def attack_dictionary(ciphertext: str, dictionary: set) -> dict:
    best_key = 0
    best_score = -1.0
    best_text = ""
    scores = {}

    for k in range(26):
        decrypted = decrypt(ciphertext, k)
        clean_text = decrypted.translate(str.maketrans("", "", string.punctuation))
        tokens = [w.lower() for w in clean_text.split() if w.isalpha()]

        if not tokens:
            score = 0.0
        else:
            valid_words = sum(1 for token in tokens if token in dictionary)
            score = valid_words / len(tokens)

        scores[k] = score
        if score > best_score:
            best_score = score
            best_key = k
            best_text = decrypted

    return {
        "predicted_key": best_key,
        "predicted_plaintext": best_text,
        "score": best_score,
        "all_scores": scores
    }