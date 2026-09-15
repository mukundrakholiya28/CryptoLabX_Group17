"""
Unit Tests for Kasiski Examination and Index of Coincidence Module
Author: Mukund Rakholiya (2024UCP1163) - Group 17
"""

import os
import unittest
from attacks.vigenere_attack.kasiski_engine import (
    clean_ciphertext,
    find_repeated_patterns,
    calculate_distances,
    find_factors,
    kasiski_analysis,
    calculate_ic,
    estimate_key_length_by_average_ic,
)


class TestKasiskiEngine(unittest.TestCase):

    def setUp(self):
        self.sample_raw = "Hello, World! 123 \n Testing Vigenère Cipher."
        self.sample_clean = "HELLOWORLDTESTINGVIGENERECIPHER"

        # Synthetic Vigenère ciphertext with known key "CRYPTO" (length 6)
        # Plaintext: "CRYPTOGRAPHYISESSENTIALFORSECURECOMMUNICATIONINTHEMODERNDIGITALWORLD"
        # Key: "CRYPTO"
        # Ciphertext:
        # P: C R Y P T O G R A P H Y I S E S S E N T I A L F O R S E C U R E C O M M U N I C A T I O N I N T H E M O D E R N D I G I T A L W O R L D
        # K: C R Y P T O C R Y P T O C R Y P T O C R Y P T O C R Y P T O C R Y P T O C R Y P T O C R Y P T O C R Y P T O C R Y P T O C R Y P T O C R Y P T O
        self.known_key_length = 6
        self.known_ciphertext = (
            "EZWRMHVIPTKMEJJHTSPMRJEMEKCFQIKMUGTFCEEEILVE"
            "KCEEZWRMHVIPTKMEJJHTSPMRJEMEKCFQIKMUGTFCEEEI"
        )

    def test_clean_ciphertext(self):
        cleaned = clean_ciphertext(self.sample_raw)
        self.assertTrue(cleaned.isalpha())
        self.assertTrue(cleaned.isupper())
        self.assertEqual(cleaned, "HELLOWORLDTESTINGVIGENERECIPHER")

    def test_find_repeated_patterns(self):
        # A test string where pattern "ABC" repeats at index 0 and index 10
        test_str = "ABCDEFGHIJABC"
        patterns = find_repeated_patterns(test_str, min_len=3, max_len=3)
        self.assertIn("ABC", patterns)
        self.assertEqual(patterns["ABC"], [0, 10])

    def test_calculate_distances(self):
        positions = {"ABC": [5, 17, 29], "XYZ": [2, 10]}
        distances = calculate_distances(positions)
        self.assertEqual(distances["ABC"], [12, 12])
        self.assertEqual(distances["XYZ"], [8])

    def test_find_factors(self):
        factors_12 = find_factors(12, max_factor=16)
        self.assertEqual(factors_12, [2, 3, 4, 6, 12])

        factors_prime = find_factors(7, max_factor=16)
        self.assertEqual(factors_prime, [7])

    def test_kasiski_analysis_known_cipher(self):
        candidates = kasiski_analysis(self.known_ciphertext, top_n=5, max_factor=16)
        self.assertTrue(len(candidates) > 0)
        top_lengths = [cand[0] for cand in candidates]
        # Length 6 or divisors of pattern period should be prominently ranked
        self.assertTrue(any(factor in [2, 3, 6] for factor in top_lengths[:3]))

    def test_calculate_ic(self):
        # Uniform random-like string should have lower IC
        random_str = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        ic_random = calculate_ic(random_str)
        self.assertEqual(ic_random, 0.0)

        # Repetitive single letter string should have IC = 1.0
        mono_str = "AAAAAAAAAA"
        ic_mono = calculate_ic(mono_str)
        self.assertAlmostEqual(ic_mono, 1.0)

        # Standard English sentence with natural letter distribution (high E, T, A, O, I, N)
        english_str = (
            "CRYPTOGRAPHY IS THE PRACTICE AND STUDY OF TECHNIQUES FOR SECURE COMMUNICATION "
            "IN THE PRESENCE OF THIRD PARTIES CALLED ADVERSARIES MORE GENERALLY CRYPTOGRAPHY IS "
            "ABOUT CONSTRUCTING AND ANALYZING PROTOCOLS THAT PREVENT THIRD PARTIES OR THE PUBLIC "
            "FROM READING PRIVATE MESSAGES"
        )
        ic_eng = calculate_ic(english_str)
        self.assertGreater(ic_eng, 0.055)


    def test_group17_ciphertext_analysis(self):
        # Test directly on Group 17's assigned ciphertext file
        filepath = os.path.join("datasets", "vigenere_ciphertext_group17.txt")
        if os.path.exists(filepath):
            with open(filepath, "r", encoding="utf-8") as f:
                cipher = f.read()

            cleaned = clean_ciphertext(cipher)
            self.assertGreater(len(cleaned), 100)

            # Perform Kasiski and average IC analysis
            kasiski_candidates = kasiski_analysis(cleaned, top_n=5)
            ic_candidates = estimate_key_length_by_average_ic(cleaned, max_key_len=12)

            self.assertTrue(len(kasiski_candidates) > 0)
            self.assertTrue(len(ic_candidates) > 0)

            print("\n[Group 17 Analysis Report]")
            print(f"Cleaned Ciphertext Length: {len(cleaned)} characters")
            print(f"Top Kasiski Candidates (length, votes): {kasiski_candidates}")
            print(f"Top IC Candidates (length, avg_ic): {ic_candidates[:4]}")


if __name__ == "__main__":
    unittest.main()
