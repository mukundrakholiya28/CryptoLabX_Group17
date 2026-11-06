"""
CryptoLabX — Assignment 10: MT19937 Stream Cipher & 16-Bit Seed Brute-Force Recovery
Author: Mukund Rakholiya (2024UCP1163)
Group: 17

This module implements:
1. MT19937 Stream Cipher (8-bit keystream XOR encryption & decryption).
2. Symmetric cipher verification with round-trip test messages.
3. Plaintext generator with random prefix (5-20 printable chars) followed by 14 'A's.
4. Random 16-bit seed encryption.
5. High-performance brute-force recovery across all 65,536 seeds.
6. Comprehensive verification of recovered seed and plaintext.
"""

import os
import random
import secrets
import string
import time
from dataclasses import dataclass
from typing import List, Optional, Tuple


def mt19937_cipher(data: bytes, seed: int) -> bytes:
    """
    Symmetric stream cipher utilizing Python's inbuilt MT19937 PRNG.
    Generates one 8-bit keystream byte per input byte and XORs it with the data.
    The exact same function serves for both encryption and decryption:
        Ciphertext = Plaintext ^ Keystream
        Plaintext  = Ciphertext ^ Keystream

    Args:
        data: Plaintext or ciphertext bytes.
        seed: Initial seed for MT19937 generator.

    Returns:
        bytes: Encrypted or decrypted byte sequence.
    """
    rng = random.Random(seed)
    # Extract 8 bits per input byte from MT19937
    keystream = bytes(rng.getrandbits(8) for _ in range(len(data)))
    # Bitwise XOR data with keystream
    return bytes(b ^ k for b, k in zip(data, keystream))


class MT19937StreamCipher:
    """
    Object-oriented wrapper for the MT19937 stream cipher.
    Provides identical encrypt and decrypt methods.
    """
    def __init__(self, seed: int):
        self.seed = int(seed)

    def encrypt(self, plaintext: bytes) -> bytes:
        """Encrypts plaintext bytes with MT19937 keystream."""
        return mt19937_cipher(plaintext, self.seed)

    def decrypt(self, ciphertext: bytes) -> bytes:
        """Decrypts ciphertext bytes with MT19937 keystream."""
        return mt19937_cipher(ciphertext, self.seed)


def verify_cipher_roundtrip(test_message: bytes = b"CryptoLabX Assignment 10 MT19937 Test!") -> bool:
    """
    Verifies that encryption and decryption are perfectly symmetric and recover
    the original message across arbitrary seeds.

    Args:
        test_message: Test byte payload.

    Returns:
        bool: True if test_message == decrypt(encrypt(test_message)).
    """
    test_seed = secrets.randbelow(65536)
    cipher = MT19937StreamCipher(test_seed)
    ct = cipher.encrypt(test_message)
    pt = cipher.decrypt(ct)
    return pt == test_message


def generate_plaintext(prefix_len: Optional[int] = None) -> bytes:
    """
    Generates plaintext containing a random prefix of 5 to 20 printable characters
    followed by 14 consecutive 'A' characters (known sequence).

    Args:
        prefix_len: Optional explicit prefix length (5 to 20). If None, chosen randomly.

    Returns:
        bytes: Plaintext bytes formatted as: [random prefix of 5-20 chars] + b"AAAAAAAAAAAAAA".
    """
    if prefix_len is None:
        prefix_len = secrets.choice(range(5, 21))  # 5 to 20 inclusive
    elif not (5 <= prefix_len <= 20):
        raise ValueError(f"Prefix length must be between 5 and 20, got {prefix_len}")

    # Use printable alphanumeric and common punctuation characters
    charset = string.ascii_letters + string.digits + "!@#$%^&*()-_=+"
    prefix = "".join(secrets.choice(charset) for _ in range(prefix_len))
    known_sequence = "A" * 14
    full_text = prefix + known_sequence
    return full_text.encode("utf-8")


def encrypt_with_16bit_seed(plaintext: bytes, seed: Optional[int] = None) -> Tuple[bytes, int]:
    """
    Encrypts plaintext using a 16-bit seed (range 0 to 65535).

    Args:
        plaintext: Plaintext bytes to encrypt.
        seed: Optional explicit 16-bit seed. If None, chosen uniformly in [0, 65535].

    Returns:
        tuple[bytes, int]: (ciphertext, 16-bit seed used).
    """
    if seed is None:
        seed = secrets.randbelow(65536)
    elif not (0 <= seed <= 65535):
        raise ValueError(f"Seed must be a 16-bit unsigned integer (0..65535), got {seed}")

    ciphertext = mt19937_cipher(plaintext, seed)
    return ciphertext, seed


@dataclass
class BruteForceResult:
    """Detailed telemetry from 16-bit seed brute-force attack."""
    recovered_seed: int
    recovered_plaintext: bytes
    known_sequence: bytes
    sequence_offset: int
    seeds_tested: int
    total_search_space: int
    elapsed_time: float
    seeds_per_second: float
    matching_seeds: List[int]


def brute_force_16bit_seed(
    ciphertext: bytes,
    known_sequence: bytes = b"AAAAAAAAAAAAAA",
    scan_entire_space: bool = False
) -> BruteForceResult:
    """
    Brute-forces the 16-bit seed space (0 to 65,535) given ciphertext and
    knowledge of 14 consecutive 'A' characters with unknown offset.

    Args:
        ciphertext: Ciphertext bytes to attack.
        known_sequence: Target known substring (default b'AAAAAAAAAAAAAA').
        scan_entire_space: If True, tests all 65,536 seeds to prove uniqueness.
                           If False, terminates immediately on first match.

    Returns:
        BruteForceResult: Recovered seed, recovered plaintext, timing, and search metrics.

    Raises:
        ValueError: If no candidate seed produces the known sequence.
    """
    ct_len = len(ciphertext)
    total_space = 65536
    matching_seeds = []
    first_recovered_seed = None
    first_recovered_pt = None
    seq_offset = -1

    t0 = time.perf_counter()
    tested_count = 0

    for candidate_seed in range(total_space):
        tested_count += 1
        rng = random.Random(candidate_seed)
        # Generate keystream for ciphertext length
        keystream = bytes(rng.getrandbits(8) for _ in range(ct_len))
        # Decrypt
        candidate_pt = bytes(c ^ k for c, k in zip(ciphertext, keystream))

        idx = candidate_pt.find(known_sequence)
        if idx != -1:
            matching_seeds.append(candidate_seed)
            if first_recovered_seed is None:
                first_recovered_seed = candidate_seed
                first_recovered_pt = candidate_pt
                seq_offset = idx
                if not scan_entire_space:
                    break

    elapsed = time.perf_counter() - t0
    rate = tested_count / elapsed if elapsed > 0 else float("inf")

    if first_recovered_seed is None:
        raise ValueError(f"Brute force failed: no seed in [0, 65535] matched '{known_sequence.decode()}'")

    return BruteForceResult(
        recovered_seed=first_recovered_seed,
        recovered_plaintext=first_recovered_pt,
        known_sequence=known_sequence,
        sequence_offset=seq_offset,
        seeds_tested=tested_count,
        total_search_space=total_space,
        elapsed_time=elapsed,
        seeds_per_second=rate,
        matching_seeds=matching_seeds,
    )


def verify_recovered_result(
    ciphertext: bytes,
    original_seed: int,
    recovered_seed: int,
    original_pt: bytes,
    recovered_pt: bytes,
    known_sequence: bytes = b"AAAAAAAAAAAAAA"
) -> bool:
    """
    Formally verifies that:
    1. The recovered seed exactly equals the original seed.
    2. Decrypting the ciphertext with the recovered seed yields the recovered plaintext.
    3. The recovered plaintext strictly matches the original plaintext.
    4. The known sequence is present in the decrypted plaintext.

    Returns:
        bool: True if all cryptographic conditions are satisfied.
    """
    # 1. Seed match
    seed_ok = (recovered_seed == original_seed)

    # 2. Independent decryption with recovered seed
    re_decrypted = mt19937_cipher(ciphertext, recovered_seed)
    decrypt_ok = (re_decrypted == recovered_pt)

    # 3. Full plaintext fidelity
    pt_ok = (recovered_pt == original_pt)

    # 4. Known sequence presence
    seq_ok = (known_sequence in recovered_pt)

    return seed_ok and decrypt_ok and pt_ok and seq_ok


def run_demonstration():
    """Executes a full interactive lab demonstration for Part A."""
    print("=" * 70)
    print("CryptoLabX — Assignment 10 Part A: MT19937 Stream Cipher Cryptanalysis")
    print("Author: Mukund Rakholiya (2024UCP1163) | Group 17")
    print("=" * 70)

    # Step 1 & 2: Test message encryption and decryption
    test_msg = b"Verification test: MT19937 symmetric XOR stream cipher."
    assert verify_cipher_roundtrip(test_msg), "Cipher symmetry test failed!"
    print("\n[+] Task 1 & 2: Stream Cipher Symmetry Verified Successfully")
    print(f"    Test payload: {test_msg.decode()}")
    print("    Symmetric property: decrypt(encrypt(M)) == M confirmed.")

    # Step 3: Generate plaintext with random prefix (5-20 chars) + 14 'A's
    plaintext = generate_plaintext()
    prefix = plaintext[:-14]
    print(f"\n[+] Task 3: Generated Target Plaintext")
    print(f"    Total Plaintext Length : {len(plaintext)} bytes")
    print(f"    Prefix Length          : {len(prefix)} chars")
    print(f"    Random Prefix          : '{prefix.decode()}'")
    print(f"    Known Sequence         : '{plaintext[-14:].decode()}' (14 consecutive 'A's)")
    print(f"    Full Plaintext         : {plaintext}")

    # Encrypt with random 16-bit seed
    ciphertext, secret_seed = encrypt_with_16bit_seed(plaintext)
    print(f"\n[+] Encrypted with Random 16-bit Seed:")
    print(f"    Secret 16-bit Seed     : {secret_seed} (Hex: 0x{secret_seed:04X})")
    print(f"    Ciphertext (Hex)       : {ciphertext.hex()}")
    print(f"    Ciphertext (Bytes)     : {list(ciphertext)}")

    # Step 4: Brute-force seed recovery
    print(f"\n[+] Task 4: Launching Exhaustive Brute-Force Key Search...")
    print(f"    Search Space: 2^16 = 65,536 candidate seeds [0 .. 65535]")
    print(f"    Target known pattern: b'AAAAAAAAAAAAAA' (location unknown in ciphertext)")

    res = brute_force_16bit_seed(ciphertext, scan_entire_space=True)

    print(f"\n[+] Brute-Force Search Completed:")
    print(f"    Seeds Tested           : {res.seeds_tested:,} / {res.total_search_space:,}")
    print(f"    Elapsed Time           : {res.elapsed_time * 1000:.2f} ms ({res.elapsed_time:.4f} s)")
    print(f"    Throughput             : {res.seeds_per_second:,.0f} seeds/second")
    print(f"    Matching Seeds Found   : {res.matching_seeds}")
    print(f"    Recovered Seed         : {res.recovered_seed} (0x{res.recovered_seed:04X})")
    print(f"    Pattern Offset in PT   : Index {res.sequence_offset}")
    print(f"    Recovered Plaintext    : '{res.recovered_plaintext.decode()}'")

    # Step 5: Verification
    is_valid = verify_recovered_result(
        ciphertext=ciphertext,
        original_seed=secret_seed,
        recovered_seed=res.recovered_seed,
        original_pt=plaintext,
        recovered_pt=res.recovered_plaintext
    )
    print(f"\n[+] Task 5: Formal Cryptographic Verification:")
    print(f"    Recovered Seed Matches Original Seed : {res.recovered_seed == secret_seed}")
    print(f"    Recovered Plaintext Matches Original : {res.recovered_plaintext == plaintext}")
    print(f"    Contains 14 Consecutive 'A's        : {b'AAAAAAAAAAAAAA' in res.recovered_plaintext}")
    print(f"    Overall Cryptanalytic Result         : {'VERIFIED SUCCESS' if is_valid else 'FAILURE'}")
    print("=" * 70)


if __name__ == "__main__":
    run_demonstration()
