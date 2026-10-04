"""
Unit Tests for Oracle Simulation & Single-Byte Decryption — Assignment 7
Member 1: Mukund Rakholiya (2024UCP1163)

Tests:
1. PKCS#7 padding and unpadding compliance and error detection.
2. PaddingOracle operational integrity, tamper detection, and query counting.
3. recover_byte right-to-left intermediate state and plaintext recovery without key access.
"""

import pytest
import os
from attacks.padding_oracle_attack.oracle import (
    pad_pkcs7,
    unpad_pkcs7,
    PaddingOracle,
)
from attacks.padding_oracle_attack.byte_decryptor import (
    recover_byte,
)


class TestPKCS7Padding:
    """Tests for standard PKCS#7 padding and unpadding logic."""

    def test_pad_partial_block(self):
        data = b"HELLO"  # 5 bytes
        padded = pad_pkcs7(data, block_size=16)
        assert len(padded) == 16
        assert padded[:5] == b"HELLO"
        assert padded[5:] == bytes([11] * 11)

    def test_pad_exact_block_boundary(self):
        data = b"0123456789ABCDEF"  # 16 bytes
        padded = pad_pkcs7(data, block_size=16)
        assert len(padded) == 32
        assert padded[:16] == data
        assert padded[16:] == bytes([16] * 16)

    def test_pad_empty_data(self):
        padded = pad_pkcs7(b"", block_size=16)
        assert len(padded) == 16
        assert padded == bytes([16] * 16)

    def test_unpad_roundtrip(self):
        samples = [
            b"",
            b"A",
            b"CryptoLabX Group 17",
            b"Exact 16 bytes!!",
            b"A longer message spanning several blocks for comprehensive testing...",
        ]
        for s in samples:
            padded = pad_pkcs7(s, block_size=16)
            assert unpad_pkcs7(padded, block_size=16) == s

    def test_unpad_invalid_inputs(self):
        with pytest.raises(ValueError):
            unpad_pkcs7(b"", block_size=16)
        with pytest.raises(ValueError):
            unpad_pkcs7(b"not-16-bytes", block_size=16)
        
        # Inconsistent pad bytes: ends with 0x03, 0x02, 0x03 instead of 0x03, 0x03, 0x03
        bad_pad = b"A" * 13 + bytes([3, 2, 3])
        with pytest.raises(ValueError):
            unpad_pkcs7(bad_pad, block_size=16)

        # Pad byte 0x00 is invalid in PKCS#7
        bad_zero = b"A" * 15 + bytes([0])
        with pytest.raises(ValueError):
            unpad_pkcs7(bad_zero, block_size=16)

        # Pad byte greater than block_size
        bad_high = b"A" * 15 + bytes([17])
        with pytest.raises(ValueError):
            unpad_pkcs7(bad_high, block_size=16)


class TestPaddingOracle:
    """Tests for PaddingOracle class environment."""

    def test_oracle_initialization(self):
        key = os.urandom(16)
        oracle = PaddingOracle(key=key, block_size=16)
        assert oracle.block_size == 16
        assert oracle.query_count == 0

        # Invalid key sizes
        with pytest.raises(ValueError):
            PaddingOracle(key=b"too_short")

    def test_oracle_encryption_and_validity(self):
        oracle = PaddingOracle()
        plaintext = b"Confidential AES-CBC Message"
        iv, ciphertext = oracle.encrypt(plaintext)
        
        assert len(iv) == 16
        assert len(ciphertext) % 16 == 0
        assert oracle.is_padding_valid(iv, ciphertext) is True
        assert oracle.query_count == 1

    def test_oracle_tamper_detection(self):
        oracle = PaddingOracle()
        iv, ciphertext = oracle.encrypt(b"Test Tampering")
        
        # Tampering with last byte almost certainly breaks PKCS#7 padding
        tampered_ct = bytearray(ciphertext)
        tampered_ct[-1] ^= 0xFF
        
        # Test several modified bytes
        assert oracle.is_padding_valid(iv, bytes(tampered_ct)) is False
        assert oracle.query_count == 1

        # Invalid IV length
        assert oracle.is_padding_valid(b"bad_iv", ciphertext) is False

    def test_oracle_query_counter_reset(self):
        oracle = PaddingOracle()
        iv, ct = oracle.encrypt(b"Counter test")
        for _ in range(5):
            oracle.is_padding_valid(iv, ct)
        assert oracle.query_count == 5
        oracle.reset_query_count()
        assert oracle.query_count == 0


class TestByteDecryptor:
    """Tests for recover_byte functionality."""

    def test_recover_single_block_bytes(self):
        oracle = PaddingOracle()
        original_plaintext = b"AttackAtDawn1234"  # Exactly 16 bytes
        iv, ciphertext = oracle.encrypt(original_plaintext)
        
        # ciphertext has 2 blocks: block 0 (AttackAtDawn1234) and block 1 (padding block 0x10 * 16)
        # Let's attack block 0 using iv as predecessor!
        block_0 = ciphertext[:16]
        
        known_intermediate = {}
        recovered_bytes = bytearray(16)
        
        # Recover right-to-left
        for k in range(15, -1, -1):
            intermediate_b, plain_b = recover_byte(
                oracle=oracle,
                prev_block=iv,
                target_block=block_0,
                byte_index=k,
                known_intermediate=known_intermediate
            )
            assert 0 <= intermediate_b <= 255
            assert plain_b == original_plaintext[k]
            known_intermediate[k] = intermediate_b
            recovered_bytes[k] = plain_b

        assert bytes(recovered_bytes) == original_plaintext
        assert oracle.query_count > 0

    def test_recover_byte_input_validation(self):
        oracle = PaddingOracle()
        with pytest.raises(ValueError):
            recover_byte(oracle, b"short", b"target", 0, {})
        with pytest.raises(ValueError):
            recover_byte(oracle, b"A"*16, b"B"*16, 16, {})  # byte_index 16 invalid
