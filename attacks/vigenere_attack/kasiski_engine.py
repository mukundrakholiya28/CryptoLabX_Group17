"""
Kasiski Examination and Index of Coincidence (IC) Module
Author: Mukund Rakholiya (2024UCP1163) - Group 17

This module implements key length estimation for Vigenère cipher cryptanalysis
using repeated sequence pattern recognition, distance factorization, and
Index of Coincidence (IC) analysis.
"""

import re
from collections import Counter, defaultdict
from typing import Dict, List, Tuple


import unicodedata

def clean_ciphertext(raw_text: str) -> str:
    """
    Remove spaces, numbers, punctuation, normalize accents (e.g. é -> e),
    and normalize the ciphertext to uppercase A-Z.
    """
    if not raw_text:
        return ""
    # Normalize unicode accents to standard base letters (e.g. 'è' -> 'e')
    normalized = unicodedata.normalize("NFKD", raw_text).encode("ASCII", "ignore").decode("utf-8")
    # Retain only alphabetic characters and convert to uppercase
    return re.sub(r"[^A-Za-z]", "", normalized).upper()



def find_repeated_patterns(text: str, min_len: int = 3, max_len: int = 5) -> Dict[str, List[int]]:
    """
    Identify repeated sequences in the ciphertext of lengths between min_len and max_len.
    Returns a dictionary mapping each repeated pattern to a list of its 0-indexed starting positions.
    """
    cleaned = clean_ciphertext(text)
    pattern_positions = defaultdict(list)
    n = len(cleaned)

    for length in range(min_len, max_len + 1):
        for i in range(n - length + 1):
            pattern = cleaned[i:i + length]
            pattern_positions[pattern].append(i)

    # Filter to retain only patterns that appear more than once
    return {pat: positions for pat, positions in pattern_positions.items() if len(positions) > 1}


def calculate_distances(pattern_positions: Dict[str, List[int]]) -> Dict[str, List[int]]:
    """
    Find distances between successive occurrences of each repeated pattern.
    """
    distances = {}
    for pattern, positions in pattern_positions.items():
        if len(positions) > 1:
            diffs = [positions[i] - positions[i - 1] for i in range(1, len(positions))]
            distances[pattern] = diffs
    return distances


def find_factors(number: int, max_factor: int = 16) -> List[int]:
    """
    Find all integer factors/divisors of a given distance between 2 and max_factor.
    Key lengths for classical Vigenère ciphers typically fall within [2, 16].
    """
    if number <= 1:
        return []
    factors = []
    for d in range(2, min(number + 1, max_factor + 1)):
        if number % d == 0:
            factors.append(d)
    return factors


def kasiski_analysis(ciphertext: str, top_n: int = 5, max_factor: int = 16) -> List[Tuple[int, int]]:
    """
    Use repeated patterns and their distances to suggest candidate key lengths.
    Tallies factor counts across all repeated pattern distances and returns
    a list of (candidate_key_length, vote_count) tuples sorted in descending order of votes.
    """
    cleaned = clean_ciphertext(ciphertext)
    if len(cleaned) < 4:
        return []

    patterns = find_repeated_patterns(cleaned, min_len=3, max_len=5)
    distances_dict = calculate_distances(patterns)

    factor_counts = Counter()
    for _, diffs in distances_dict.items():
        for dist in diffs:
            for factor in find_factors(dist, max_factor=max_factor):
                factor_counts[factor] += 1

    return factor_counts.most_common(top_n)


def calculate_ic(text: str) -> float:
    """
    Calculate the Index of Coincidence (IC) for a given text string.
    Formula: IC = sum(f_i * (f_i - 1)) / (N * (N - 1))
    Expected values:
      - Random text / high key-length polyalphabetic: ~0.0385
      - Standard English plaintext / monoalphabetic: ~0.0650 to 0.0685
    """
    cleaned = clean_ciphertext(text)
    n = len(cleaned)
    if n <= 1:
        return 0.0

    counts = Counter(cleaned)
    numerator = sum(f * (f - 1) for f in counts.values())
    denominator = n * (n - 1)

    return numerator / denominator


def estimate_key_length_by_average_ic(ciphertext: str, max_key_len: int = 16) -> List[Tuple[int, float]]:
    """
    Companion helper to corroborate Kasiski results:
    For candidate key lengths k in [1, max_key_len], split into k cosets,
    calculate the average IC of each coset, and sort candidate key lengths by closeness to 0.068.
    """
    cleaned = clean_ciphertext(ciphertext)
    results = []

    for k in range(1, min(max_key_len + 1, len(cleaned))):
        coset_ics = []
        for i in range(k):
            coset = cleaned[i::k]
            if len(coset) > 1:
                coset_ics.append(calculate_ic(coset))
        if coset_ics:
            avg_ic = sum(coset_ics) / len(coset_ics)
            results.append((k, avg_ic))

    # Sort candidates by descending average IC (closest to monoalphabetic English ~0.068)
    results.sort(key=lambda x: x[1], reverse=True)
    return results
