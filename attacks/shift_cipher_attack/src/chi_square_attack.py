"""
Statistical Cryptanalysis of Shift Cipher using Chi-Square Goodness-of-Fit
"""

from collections import Counter
from shift_cipher import decrypt

ENGLISH_FREQ = {
    'A': 0.08167, 'B': 0.01492, 'C': 0.02782, 'D': 0.04253, 'E': 0.12702,
    'F': 0.02228, 'G': 0.02015, 'H': 0.06094, 'I': 0.06966, 'J': 0.00153,
    'K': 0.00772, 'L': 0.04025, 'M': 0.02406, 'N': 0.06749, 'O': 0.07507,
    'P': 0.01929, 'Q': 0.00095, 'R': 0.05987, 'S': 0.06327, 'T': 0.09056,
    'U': 0.02758, 'V': 0.00978, 'W': 0.02360, 'X': 0.00150, 'Y': 0.01974,
    'Z': 0.00074
}


def attack_chi_square(ciphertext: str) -> dict:
    best_key = 0
    min_chi = float("inf")
    best_text = ""
    chi_values = {}

    for k in range(26):
        decrypted = decrypt(ciphertext, k)
        letters = [c.upper() for c in decrypted if c.isalpha()]
        n = len(letters)

        if n == 0:
            chi_values[k] = float("inf")
            continue

        observed_counts = Counter(letters)
        chi_stat = 0.0

        for char, prob in ENGLISH_FREQ.items():
            expected = n * prob
            observed = observed_counts.get(char, 0)
            chi_stat += ((observed - expected) ** 2) / expected

        chi_values[k] = chi_stat
        if chi_stat < min_chi:
            min_chi = chi_stat
            best_key = k
            best_text = decrypted

    return {
        "predicted_key": best_key,
        "predicted_plaintext": best_text,
        "chi_square_stat": min_chi,
        "all_chi": chi_values
    }