"""
Oracle Simulation & PKCS#7 Padding Engine — Assignment 7 (CryptoLabX Group 17)
Member 1: Mukund Rakholiya (2024UCP1163)

This module implements:
1. Standard PKCS#7 padding and unpadding with strict validation.
2. The PaddingOracle class, simulating an external server that provides:
   - Encryption using an unexposed secret AES key in CBC mode.
   - A padding oracle function returning whether decrypted ciphertext has valid PKCS#7 padding.
   - Oracle query tracking to measure attack complexity.
"""

import os
from typing import Optional, Tuple
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend


def pad_pkcs7(data: bytes, block_size: int = 16) -> bytes:
    """Applies standard PKCS#7 padding to align byte data to block_size.
    
    Args:
        data: Raw input bytes to pad.
        block_size: Cipher block size in bytes (default 16 for AES).
        
    Returns:
        Padded byte string whose length is a positive multiple of block_size.
        
    Raises:
        ValueError: If block_size is outside the valid range 1 <= block_size <= 255.
    """
    if block_size < 1 or block_size > 255:
        raise ValueError(f"Invalid block size {block_size}; must be between 1 and 255")
    
    remainder = len(data) % block_size
    pad_len = block_size - remainder
    return data + bytes([pad_len] * pad_len)


def unpad_pkcs7(data: bytes, block_size: int = 16) -> bytes:
    """Validates and strips PKCS#7 padding from decrypted byte data.
    
    Args:
        data: Padded byte string to validate and strip.
        block_size: Cipher block size in bytes (default 16 for AES).
        
    Returns:
        Unpadded original byte string.
        
    Raises:
        ValueError: If data is empty, not a multiple of block_size,
                    or contains invalid / inconsistent PKCS#7 padding.
    """
    if not data:
        raise ValueError("Cannot unpad empty data")
    if len(data) % block_size != 0:
        raise ValueError(f"Data length {len(data)} is not a multiple of block size {block_size}")
    
    pad_len = data[-1]
    if pad_len < 1 or pad_len > block_size:
        raise ValueError(f"Invalid padding value {pad_len}; must be between 1 and {block_size}")
    
    expected_pad = bytes([pad_len] * pad_len)
    if data[-pad_len:] != expected_pad:
        raise ValueError("Inconsistent PKCS#7 padding bytes encountered")
    
    return data[:-pad_len]


class PaddingOracle:
    """Simulates a remote cryptographic service with an unexposed AES key.
    
    Under the assignment constraints:
    - The AES key is strictly private and never leaked or accessed during the attack.
    - An oracle endpoint returns only a boolean indicating whether the decrypted
      ciphertext possesses valid PKCS#7 padding.
    - Keeps an accurate tally of all oracle queries to evaluate attack complexity.
    """

    def __init__(self, key: Optional[bytes] = None, block_size: int = 16) -> None:
        """Initializes the oracle with an AES key.
        
        Args:
            key: 16-byte secret AES key. If None, securely generates a random key.
            block_size: AES block size (default: 16 bytes).
        """
        self._block_size = block_size
        if key is None:
            self._key = os.urandom(16)
        else:
            if len(key) not in (16, 24, 32):
                raise ValueError(f"Invalid AES key length {len(key)}; must be 16, 24, or 32 bytes")
            self._key = key
        
        self._query_count = 0

    @property
    def block_size(self) -> int:
        """Returns the cipher block size."""
        return self._block_size

    @property
    def query_count(self) -> int:
        """Returns the total number of oracle queries performed."""
        return self._query_count

    def reset_query_count(self) -> None:
        """Resets the query counter to zero for benchmarking."""
        self._query_count = 0

    def encrypt(self, plaintext: bytes) -> Tuple[bytes, bytes]:
        """Encrypts plaintext using AES-CBC with PKCS#7 padding.
        
        Args:
            plaintext: Raw unpadded plaintext bytes.
            
        Returns:
            Tuple of (iv, ciphertext) where IV is 16 random bytes and
            ciphertext is a multiple of 16 bytes.
        """
        padded = pad_pkcs7(plaintext, self._block_size)
        iv = os.urandom(self._block_size)
        
        cipher = Cipher(
            algorithms.AES(self._key),
            modes.CBC(iv),
            backend=default_backend()
        )
        encryptor = cipher.encryptor()
        ciphertext = encryptor.update(padded) + encryptor.finalize()
        return iv, ciphertext

    def is_padding_valid(self, iv: bytes, ciphertext: bytes) -> bool:
        """Padding Oracle Endpoint: checks if CBC decryption results in valid PKCS#7 padding.
        
        Args:
            iv: Initialization Vector (16 bytes) or crafted predecessor block.
            ciphertext: Target ciphertext block(s) (multiple of 16 bytes).
            
        Returns:
            True if padding is strictly valid, False otherwise.
        """
        self._query_count += 1
        
        if len(iv) != self._block_size:
            return False
        if not ciphertext or len(ciphertext) % self._block_size != 0:
            return False
        
        try:
            cipher = Cipher(
                algorithms.AES(self._key),
                modes.CBC(iv),
                backend=default_backend()
            )
            decryptor = cipher.decryptor()
            decrypted = decryptor.update(ciphertext) + decryptor.finalize()
            unpad_pkcs7(decrypted, self._block_size)
            return True
        except (ValueError, Exception):
            return False
