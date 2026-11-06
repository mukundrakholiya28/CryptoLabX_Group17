"""
CryptoLabX — Unit Tests for MT19937 Stream Cipher & 16-Bit Seed Brute-Force Recovery
Author: Mukund Rakholiya (2024UCP1163)
Group: 17
"""

import pytest

from modern.mt19937_cipher import (
    MT19937StreamCipher,
    mt19937_cipher,
    verify_cipher_roundtrip,
    generate_plaintext,
    encrypt_with_16bit_seed,
    brute_force_16bit_seed,
    verify_recovered_result,
)


class TestMT19937CipherSymmetry:
    """Tests for stream cipher symmetry and XOR reversibility."""

    def test_roundtrip_test_message(self):
        assert verify_cipher_roundtrip() is True

    @pytest.mark.parametrize("payload", [
        b"",
        b"A",
        b"Hello, World!",
        b"1234567890!@#$%^&*()_+",
        bytes(range(256)),
    ])
    def test_arbitrary_payload_symmetry(self, payload):
        seed = 42135
        cipher = MT19937StreamCipher(seed)
        ciphertext = cipher.encrypt(payload)
        decrypted = cipher.decrypt(ciphertext)
        assert decrypted == payload

    def test_different_seeds_produce_different_ciphertexts(self):
        msg = b"Confidential Cryptographic Message"
        ct1 = mt19937_cipher(msg, seed=1000)
        ct2 = mt19937_cipher(msg, seed=2000)
        assert ct1 != ct2


class TestPlaintextGenerator:
    """Tests for plaintext format compliance (5-20 random prefix + 14 'A's)."""

    def test_default_plaintext_structure(self):
        for _ in range(20):
            pt = generate_plaintext()
            assert isinstance(pt, bytes)
            assert len(pt) >= 19  # 5 + 14
            assert len(pt) <= 34  # 20 + 14
            assert pt.endswith(b"AAAAAAAAAAAAAA")
            prefix = pt[:-14]
            assert 5 <= len(prefix) <= 20
            # Ensure prefix is printable
            assert prefix.decode("utf-8").isprintable()

    def test_explicit_prefix_length(self):
        pt_5 = generate_plaintext(prefix_len=5)
        assert len(pt_5) == 19
        assert pt_5.endswith(b"AAAAAAAAAAAAAA")

        pt_20 = generate_plaintext(prefix_len=20)
        assert len(pt_20) == 34
        assert pt_20.endswith(b"AAAAAAAAAAAAAA")

    def test_invalid_prefix_length_raises_error(self):
        with pytest.raises(ValueError, match="between 5 and 20"):
            generate_plaintext(prefix_len=4)
        with pytest.raises(ValueError, match="between 5 and 20"):
            generate_plaintext(prefix_len=21)


class Test16BitSeedEncryption:
    """Tests for 16-bit seed encryption bounds and output properties."""

    def test_seed_bounds(self):
        pt = b"test_message"
        ct, seed = encrypt_with_16bit_seed(pt)
        assert 0 <= seed <= 65535
        assert len(ct) == len(pt)
        assert ct != pt

    def test_explicit_seed(self):
        pt = b"test_payload"
        ct, seed = encrypt_with_16bit_seed(pt, seed=54321)
        assert seed == 54321
        assert mt19937_cipher(ct, seed=54321) == pt

    def test_invalid_seed_range_raises_error(self):
        pt = b"data"
        with pytest.raises(ValueError, match="16-bit unsigned integer"):
            encrypt_with_16bit_seed(pt, seed=-1)
        with pytest.raises(ValueError, match="16-bit unsigned integer"):
            encrypt_with_16bit_seed(pt, seed=65536)


class TestBruteForceSeedRecovery:
    """Tests for exhaustive 16-bit seed brute-force recovery."""

    @pytest.mark.parametrize("seed", [0, 137, 32768, 65535])
    def test_recover_boundary_seeds(self, seed):
        pt = generate_plaintext(prefix_len=7)
        ct, _ = encrypt_with_16bit_seed(pt, seed=seed)

        res = brute_force_16bit_seed(ct, known_sequence=b"AAAAAAAAAAAAAA", scan_entire_space=False)
        assert res.recovered_seed == seed
        assert res.recovered_plaintext == pt
        assert b"AAAAAAAAAAAAAA" in res.recovered_plaintext

        # Verify formal verification function
        assert verify_recovered_result(ct, seed, res.recovered_seed, pt, res.recovered_plaintext) is True

    def test_unmatched_sequence_raises_error(self):
        pt = b"random_string_without_target_letters"
        ct, _ = encrypt_with_16bit_seed(pt, seed=123)
        with pytest.raises(ValueError, match="Brute force failed"):
            brute_force_16bit_seed(ct, known_sequence=b"ZZZZZZZZZZZZZZ", scan_entire_space=False)

    def test_verify_recovered_result_catches_tampering(self):
        pt = b"prefix" + b"A" * 14
        ct, orig_seed = encrypt_with_16bit_seed(pt, seed=100)

        # Mismatched seed
        assert verify_recovered_result(ct, orig_seed, orig_seed + 1, pt, pt) is False

        # Mismatched plaintext
        assert verify_recovered_result(ct, orig_seed, orig_seed, pt, b"tampered") is False
