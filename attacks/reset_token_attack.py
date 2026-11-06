"""
CryptoLabX — Assignment 10 Part B: Predictable Password Reset Token Generator & Time-Window Attack
Author: Lakshay Ahuja (2024UCP1157)
Group: 17

This module implements:
1. Simulated web application password reset token generator seeded with Unix integer timestamp T.
2. 16-byte hex token generation via MT19937.
3. Attacker time-window brute-force attack testing [T - 300, T + 300] seconds.
4. Telemetry reporting (candidate count, elapsed time, throughput, recovered timestamp).
5. Formal token verification via regeneration.
"""

import random
import time
from dataclasses import dataclass
from typing import List, Optional, Tuple


def generate_reset_token(timestamp: Optional[int] = None) -> Tuple[int, str, bytes]:
    """
    Simulated web application reset token generator.
    Seeds MT19937 with current Unix timestamp (integer seconds) and generates
    a 16-byte reset token formatted as a 32-character hexadecimal string.

    Args:
        timestamp: Optional explicit Unix timestamp (seconds). If None, uses int(time.time()).

    Returns:
        tuple[int, str, bytes]: (timestamp T, token_hex, token_raw_bytes).
    """
    if timestamp is None:
        timestamp = int(time.time())

    # MT19937 seeded with integer Unix seconds
    rng = random.Random(timestamp)
    # Extract 16 consecutive 8-bit keystream values
    token_bytes = bytes(rng.getrandbits(8) for _ in range(16))
    token_hex = token_bytes.hex()

    return timestamp, token_hex, token_bytes


@dataclass
class TokenAttackResult:
    """Telemetry and outcome of password reset token prediction attack."""
    observed_token_hex: str
    approximate_timestamp: int
    search_window_seconds: int
    search_interval: Tuple[int, int]
    recovered_timestamp: Optional[int]
    candidates_tested: int
    total_window_candidates: int
    elapsed_time_seconds: float
    candidates_per_second: float
    is_verified: bool

    def summary(self) -> str:
        status = "CRACKED & VERIFIED" if self.is_verified else "FAILED"
        return (
            f"Token Attack [{status}]:\n"
            f"Observed Token (Hex) : {self.observed_token_hex}\n"
            f"Search Interval      : [{self.search_interval[0]}, {self.search_interval[1]}] "
            f"(+/- {self.search_window_seconds}s, Total Window = {self.total_window_candidates})\n"
            f"Candidates Tested    : {self.candidates_tested:,}\n"
            f"Recovered Timestamp  : {self.recovered_timestamp}\n"
            f"Elapsed Time         : {self.elapsed_time_seconds * 1000:.3f} ms ({self.elapsed_time_seconds:.6f} s)\n"
            f"Search Rate          : {self.candidates_per_second:,.0f} candidates/sec\n"
            f"Verification Match   : {'CONFIRMED MATCH' if self.is_verified else 'MISMATCH'}"
        )


def predict_reset_token(
    observed_token_hex: str,
    approx_timestamp: int,
    window_seconds: int = 300,
) -> TokenAttackResult:
    """
    Simulates attacker observing a reset token and exploiting knowledge of
    the approximate generation time within [approx_timestamp - window, approx_timestamp + window].

    Args:
        observed_token_hex: The 32-character hex reset token observed by the attacker.
        approx_timestamp: Attacker's estimated generation timestamp.
        window_seconds: Search window in seconds (default +/- 300s = 601 candidates).

    Returns:
        TokenAttackResult: Outcome containing recovered timestamp, candidates tested, and timing.

    Raises:
        ValueError: If token format is invalid or no match found in window.
    """
    target_bytes = bytes.fromhex(observed_token_hex)
    if len(target_bytes) != 16:
        raise ValueError(f"Reset token must be exactly 16 bytes (32 hex characters), got {len(target_bytes)}")

    start_t = approx_timestamp - window_seconds
    end_t = approx_timestamp + window_seconds
    total_candidates = (end_t - start_t) + 1

    t0 = time.perf_counter()
    candidates_tested = 0
    recovered_t = None

    for candidate_t in range(start_t, end_t + 1):
        candidates_tested += 1
        rng = random.Random(candidate_t)
        candidate_bytes = bytes(rng.getrandbits(8) for _ in range(16))
        if candidate_bytes == target_bytes:
            recovered_t = candidate_t
            break

    elapsed = time.perf_counter() - t0
    rate = candidates_tested / elapsed if elapsed > 0 else float("inf")

    # Verification: regenerate token with recovered timestamp
    is_verified = False
    if recovered_t is not None:
        regen_t, regen_hex, _ = generate_reset_token(recovered_t)
        is_verified = (regen_hex.lower() == observed_token_hex.lower() and regen_t == recovered_t)

    return TokenAttackResult(
        observed_token_hex=observed_token_hex,
        approximate_timestamp=approx_timestamp,
        search_window_seconds=window_seconds,
        search_interval=(start_t, end_t),
        recovered_timestamp=recovered_t,
        candidates_tested=candidates_tested,
        total_window_candidates=total_candidates,
        elapsed_time_seconds=elapsed,
        candidates_per_second=rate,
        is_verified=is_verified,
    )


def verify_token_match(timestamp: int, observed_token_hex: str) -> bool:
    """
    Independent helper validating that regenerating the token at `timestamp`
    matches `observed_token_hex` bit-for-bit.
    """
    _, regen_hex, _ = generate_reset_token(timestamp)
    return regen_hex.lower() == observed_token_hex.lower()


def run_token_attack_demo():
    """Interactive lab demonstration for Assignment 10 Part B."""
    print("=" * 75)
    print("CryptoLabX — Assignment 10 Part B: Predictable Reset Token Attack")
    print("Author: Lakshay Ahuja (2024UCP1157) | Group 17")
    print("=" * 75)

    # 1. Simulate web application generating reset token
    actual_t, token_hex, token_bytes = generate_reset_token()
    print("\n[+] Step 1: Web Application Generates Password Reset Token:")
    print(f"    Generation Timestamp (T) : {actual_t} (Unix Epoch Seconds)")
    print(f"    16-Byte Hex Token        : {token_hex}")
    print(f"    Raw Token Byte Values    : {list(token_bytes)}")

    # 2. Simulate attacker with clock synchronization offset (+125 seconds skew)
    attacker_approx_t = actual_t + 125
    window = 300
    print("\n[+] Step 2: Attacker Intercepts Token & Launches Time-Window Attack:")
    print(f"    Observed Token           : {token_hex}")
    print(f"    Attacker Approx Time     : {attacker_approx_t} (Skew: +125 seconds)")
    print(f"    Search Interval Window   : [T_approx - {window}, T_approx + {window}] (601 candidate seeds)")

    # 3. Execute attack
    res = predict_reset_token(
        observed_token_hex=token_hex,
        approx_timestamp=attacker_approx_t,
        window_seconds=window,
    )

    print("\n[+] Step 3: Attack Execution Telemetry:")
    print(res.summary())

    # 4. Verification
    print("\n[+] Step 4: Verification of Recovered Timestamp:")
    print(f"    Actual Timestamp         : {actual_t}")
    print(f"    Recovered Timestamp      : {res.recovered_timestamp}")
    print(f"    Timestamp Match Confirmed: {res.recovered_timestamp == actual_t}")
    print(f"    Regenerated Token Match  : {verify_token_match(res.recovered_timestamp, token_hex)}")
    print("=" * 75)


if __name__ == "__main__":
    run_token_attack_demo()
