"""
Integrated Demonstration Runner for Assignment 10:
MT19937 Stream Cipher & Predictable Password Reset Token Attack.

Author: Mukund Rakholiya (2024UCP1163) & Lakshay Ahuja (2024UCP1157)
Group: 17
"""

import os
import sys

# Ensure repository root is on sys.path
sys.path.append(os.path.abspath("."))

from modern.mt19937_cipher import (
    MT19937StreamCipher,
    verify_cipher_roundtrip,
    generate_plaintext,
    encrypt_with_16bit_seed,
    brute_force_16bit_seed,
    verify_recovered_result,
)
from attacks.reset_token_attack import (
    generate_reset_token,
    predict_reset_token,
    verify_token_match,
)


def run_assignment_10():
    print("=" * 85)
    print("CryptoLabX — Assignment 10: MT19937 Stream Cipher & Predictable Token Attack")
    print("Team: Group 17 | Mukund Rakholiya (2024UCP1163) & Lakshay Ahuja (2024UCP1157)")
    print("=" * 85)

    # -------------------------------------------------------------
    # PART A: MT19937 Stream Cipher & 16-Bit Seed Brute-Force
    # -------------------------------------------------------------
    print("\n" + "=" * 85)
    print("PART A: MT19937 STREAM CIPHER & 16-BIT SEED BRUTE-FORCE RECOVERY (TASKS 1-5, 16-17)")
    print("=" * 85)

    # Tasks 1 & 2: Stream Cipher Symmetry
    test_msg = b"CryptoLabX Symmetric Stream Cipher Verification Test."
    is_symmetric = verify_cipher_roundtrip(test_msg)
    print("\n[+] Task 1 & 2: Stream Cipher Keystream & Symmetric Verification")
    print(f"    Keystream Extraction : 1 byte (8-bit value) per input byte via MT19937")
    print(f"    Cipher Functionality : Symmetric bitwise XOR (encrypt == decrypt)")
    print(f"    Test Message Payload : {test_msg.decode()}")
    print(f"    Round-trip Symmetry  : decrypt(encrypt(M)) == M -> [{'PASSED' if is_symmetric else 'FAILED'}]")

    # Task 3: Plaintext Generation & 16-bit Seed Encryption
    pt = generate_plaintext()
    prefix = pt[:-14]
    known_seq = pt[-14:]
    ct, seed = encrypt_with_16bit_seed(pt)

    print("\n[+] Task 3: Plaintext Generation & Weak 16-bit Seed Encryption")
    print(f"    Total Plaintext Length : {len(pt)} bytes")
    print(f"    Random Prefix Length   : {len(prefix)} printable ASCII characters")
    print(f"    Random Prefix Content  : '{prefix.decode()}'")
    print(f"    Known Sequence Content : '{known_seq.decode()}' (14 consecutive 'A's)")
    print(f"    Full Plaintext Bytes   : {pt}")
    print(f"    Secret 16-Bit Seed     : {seed} (Hex: 0x{seed:04X}, Range: [0, 65535])")
    print(f"    Ciphertext (Hex)       : {ct.hex()}")
    print(f"    Ciphertext (Bytes)     : {list(ct)}")

    # Task 4: Brute-Force Key Recovery
    print("\n[+] Task 4: Exhaustive 16-bit Seed Brute-Force Recovery")
    print(f"    Search Space Size      : 2^16 = 65,536 candidate seeds [0 .. 65535]")
    print(f"    Known Sequence Target  : b'AAAAAAAAAAAAAA' (location unknown in ciphertext)")

    res_a = brute_force_16bit_seed(ct, known_sequence=b"AAAAAAAAAAAAAA", scan_entire_space=True)
    print(f"    Candidates Tested      : {res_a.seeds_tested:,} / {res_a.total_search_space:,} (100.0% scan)")
    print(f"    Elapsed Execution Time : {res_a.elapsed_time * 1000:.2f} ms ({res_a.elapsed_time:.4f} s)")
    print(f"    Search Throughput      : {res_a.seeds_per_second:,.0f} seeds/second")
    print(f"    Recovered Seed         : {res_a.recovered_seed} (Hex: 0x{res_a.recovered_seed:04X})")
    print(f"    Pattern Offset in PT   : Index {res_a.sequence_offset}")
    print(f"    Recovered Plaintext    : '{res_a.recovered_plaintext.decode()}'")

    # Task 5: Verification
    is_valid_a = verify_recovered_result(ct, seed, res_a.recovered_seed, pt, res_a.recovered_plaintext)
    print("\n[+] Task 5: Cryptographic Result Verification")
    print(f"    Recovered Seed Matches Original : {res_a.recovered_seed == seed} ({res_a.recovered_seed} == {seed})")
    print(f"    Recovered Plaintext Matches     : {res_a.recovered_plaintext == pt}")
    print(f"    Contains Known 14 'A' Sequence  : {b'AAAAAAAAAAAAAA' in res_a.recovered_plaintext}")
    print(f"    Part A Overall Verification     : [{'SUCCESS' if is_valid_a else 'FAILED'}]")

    # -------------------------------------------------------------
    # PART B: Predictable Password Reset Tokens
    # -------------------------------------------------------------
    print("\n" + "=" * 85)
    print("PART B: PREDICTABLE PASSWORD RESET TOKENS (TASKS 6-11, 18-19)")
    print("=" * 85)

    # Tasks 6-8: Token Generation
    server_t, tok_hex, tok_bytes = generate_reset_token()
    print("\n[+] Tasks 6-8: Server Generates 16-byte Password Reset Token")
    print(f"    Generation Timestamp (T): {server_t} (Unix Epoch integer seconds)")
    print(f"    PRNG Seeding Mechanism  : MT19937 seeded with T")
    print(f"    16-Byte Token (Hex)     : {tok_hex} (32 hexadecimal characters)")
    print(f"    Raw Token Bytes         : {list(tok_bytes)}")

    # Tasks 9-11: Attacker Time-Window Attack
    attacker_skew = 145  # Simulated 145 seconds network/clock offset
    approx_t = server_t + attacker_skew
    window = 300

    print("\n[+] Tasks 9-11: Attacker Intercepts Token & Launches Time-Window Attack")
    print(f"    Observed Token (Hex)    : {tok_hex}")
    print(f"    Attacker Approx Time    : {approx_t} (Clock skew: +{attacker_skew}s)")
    print(f"    Search Interval Window  : [T_approx - {window}, T_approx + {window}]")
    print(f"    Total Interval Bounds   : [{approx_t - window}, {approx_t + window}] (601 candidate seeds)")

    res_b = predict_reset_token(tok_hex, approx_timestamp=approx_t, window_seconds=window)
    print(f"    Candidates Evaluated    : {res_b.candidates_tested:,} / {res_b.total_window_candidates}")
    print(f"    Elapsed Attack Time     : {res_b.elapsed_time_seconds * 1000:.3f} ms ({res_b.elapsed_time_seconds:.6f} s)")
    print(f"    Search Throughput       : {res_b.candidates_per_second:,.0f} seeds/second")
    print(f"    Recovered Timestamp     : {res_b.recovered_timestamp}")
    print(f"    Timestamp Accuracy Check: {res_b.recovered_timestamp == server_t} ({res_b.recovered_timestamp} == {server_t})")
    print(f"    Token Regeneration Match: {verify_token_match(res_b.recovered_timestamp, tok_hex)} (Bit-for-bit verified)")
    print(f"    Part B Overall Status   : [{'CRACKED & VERIFIED' if res_b.is_verified else 'FAILED'}]")

    # -------------------------------------------------------------
    # THEORETICAL SUMMARY (Tasks 12-15)
    # -------------------------------------------------------------
    print("\n" + "=" * 85)
    print("THEORETICAL CRYPTANALYSIS SUMMARY (TASKS 12-15)")
    print("=" * 85)
    print("""1. Task 12 (MT19937 Non-Cryptographic Flaws):
   - Linear recurrence over GF(2): x_{k+n} = x_{k+m} ^ ((x_k^u | x_{k+1}^l) * A).
   - Invertible tempering matrix: observing 624 outputs (19,968 bits) fully reconstructs state.
   - Zero forward/backward secrecy: past outputs can be reversed, future outputs predicted.

2. Task 13 (Known-Plaintext & 16-Bit Keyspace):
   - Stream cipher identity: C = P ^ K => K = P ^ C (keystream is revealed directly).
   - 16-bit keyspace: 2^16 = 65,536 seeds. Cracked in ~0.6 seconds at ~100,000 seeds/sec.
   - 14 'A' characters provide 112 bits of constraint (false positive probability ~ 3.2 x 10^-33).

3. Task 14 (Vulnerability of Timestamp Seeding):
   - Coarse 1-second resolution collapses 128-bit token space down to 1 state/second.
   - HTTP Date response headers reveal target timestamp within +/- 300s window (601 candidates, < 2 ms attack).

4. Task 15 (Industrial Mitigation):
   - Always use OS kernel CSPRNGs (secrets, os.urandom, BCryptGenRandom, /dev/urandom).
   - Reset tokens must have >= 128 bits of true entropy and be stored securely hashed with SHA-256.""")
    print("=" * 85)


if __name__ == "__main__":
    run_assignment_10()
