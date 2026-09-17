import unittest

from attacks.vigenere_attack.frequency_engine import (
    split_into_groups,
    frequency_analysis,
    find_shift,
    find_key,
    vigenere_decrypt,
    vigenere_encrypt,
    verify,
)
from attacks.shift_cipher_attack.src.chi_square_attack import ENGLISH_FREQ


class TestVigenereFrequencyEngine(unittest.TestCase):

    def test_split_into_groups(self):
        result = split_into_groups("ABCDEFGHI", 3)

        self.assertEqual(result, ["ADG", "BEH", "CFI"])

    def test_frequency_analysis(self):
        result = frequency_analysis("AABC")

        self.assertAlmostEqual(result["A"], 50.0)
        self.assertAlmostEqual(result["B"], 25.0)
        self.assertAlmostEqual(result["C"], 25.0)
        self.assertAlmostEqual(result["Z"], 0.0)

    def test_find_shift(self):
        # Build a plaintext group whose frequency distribution
        # closely matches standard English frequencies.
        plaintext = ""

        for letter, probability in ENGLISH_FREQ.items():
            count = round(probability * 10000)
            plaintext += letter * count

        # Encrypt using Caesar shift 3.
        shift = 3
        ciphertext = ""

        for char in plaintext:
            value = (ord(char) - ord("A") + shift) % 26
            ciphertext += chr(ord("A") + value)

        self.assertEqual(find_shift(ciphertext), 3)

    def test_find_key(self):
        plaintext = (
            "THE QUICK BROWN FOX JUMPS OVER THE LAZY DOG. "
            "THIS IS A SIMPLE ENGLISH SENTENCE USED FOR TESTING "
            "VIGENERE FREQUENCY ANALYSIS. "
        ) * 100

        key = "KEY"

        ciphertext = vigenere_encrypt(plaintext, key)
        groups = split_into_groups(ciphertext, len(key))

        recovered_key = find_key(groups)

        self.assertEqual(recovered_key, key)

    def test_vigenere_encrypt(self):
        plaintext = "ATTACK AT DAWN"
        key = "LEMON"

        ciphertext = vigenere_encrypt(plaintext, key)

        self.assertEqual(ciphertext, "LXFOPV EF RNHR")

    def test_vigenere_decrypt(self):
        ciphertext = "LXFOPV EF RNHR"
        key = "LEMON"

        plaintext = vigenere_decrypt(ciphertext, key)

        self.assertEqual(plaintext, "ATTACK AT DAWN")

    def test_verify(self):
        plaintext = "ATTACK AT DAWN"
        key = "LEMON"

        ciphertext = vigenere_encrypt(plaintext, key)

        self.assertTrue(
            verify(ciphertext, vigenere_encrypt(plaintext, key))
        )

        self.assertFalse(
            verify(ciphertext, "WRONG CIPHERTEXT")
        )


if __name__ == "__main__":
    unittest.main()