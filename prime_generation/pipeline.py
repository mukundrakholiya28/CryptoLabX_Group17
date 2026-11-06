"""
Prime Generation Pipeline Orchestrator.

Author: Lakshay Ahuja (2024UCP1157)
Assignment: 8 - Prime Generation Using Miller-Rabin
"""

import time
from dataclasses import dataclass
from typing import Dict, List, Optional

from prime_generation.candidate_generator import (
    generate_candidate,
    get_small_primes,
    sieve_of_small_primes,
)
from prime_generation.miller_rabin import is_probable_prime


@dataclass
class PrimeGenerationResult:
    """Telemetry and output from prime generation pipeline."""
    candidate: int
    bit_length: int
    assigned_bit_length: int
    candidates_tested: int
    rounds_performed: int
    execution_time_seconds: float
    passed_sieve_count: int

    def summary(self) -> str:
        return (
            f"512-bit Probable Prime Generated Successfully:\n"
            f"Bit Length: {self.bit_length} bits | Assigned: {self.assigned_bit_length} bits\n"
            f"Candidates Generated: {self.candidates_tested:,} | Passed Small Prime Sieve: {self.passed_sieve_count:,}\n"
            f"Miller-Rabin Rounds: {self.rounds_performed} | Execution Time: {self.execution_time_seconds:.4f} seconds\n"
            f"Candidate (Hex): {hex(self.candidate)}\n"
            f"Candidate (Dec): {self.candidate}"
        )


def generate_512bit_prime(
    bit_length: int = 512,
    rounds: int = 40,
    use_sieve: bool = True,
    small_primes_limit: int = 1000,
) -> PrimeGenerationResult:
    """
    Orchestrates the prime generation pipeline:
    1. Generates cryptographically secure random odd candidates of exact bit_length.
    2. Applies small prime trial-division sieve pre-filter (if use_sieve=True).
    3. Executes multi-round Miller-Rabin primality test.
    4. Iterates until a verified probable prime is found.

    Args:
        bit_length: Target bit length (default 512).
        rounds: Number of Miller-Rabin witness rounds (default 40, error <= 4^-40).
        use_sieve: Whether to pre-filter candidates with small prime sieve.
        small_primes_limit: Upper bound for small primes sieve.

    Returns:
        PrimeGenerationResult: Telemetry and verified prime number.
    """
    if bit_length < 2:
        raise ValueError(f"Bit length must be >= 2, got {bit_length}")

    small_primes = get_small_primes(small_primes_limit) if use_sieve else []
    candidates_tested = 0
    passed_sieve_count = 0

    start_time = time.perf_counter()

    while True:
        candidates_tested += 1
        candidate = generate_candidate(bit_length=bit_length)

        # Pre-filter using trial division sieve
        if use_sieve:
            if not sieve_of_small_primes(candidate, small_primes=small_primes):
                continue
            passed_sieve_count += 1
        else:
            passed_sieve_count += 1

        # Multi-round Miller-Rabin primality test
        is_prime, rounds_passed = is_probable_prime(candidate, rounds=rounds)
        if is_prime:
            elapsed_time = time.perf_counter() - start_time
            return PrimeGenerationResult(
                candidate=candidate,
                bit_length=candidate.bit_length(),
                assigned_bit_length=bit_length,
                candidates_tested=candidates_tested,
                rounds_performed=rounds_passed,
                execution_time_seconds=elapsed_time,
                passed_sieve_count=passed_sieve_count,
            )


def benchmark_generation(
    iterations: int = 3,
    bit_lengths: Optional[List[int]] = None,
) -> Dict[int, Dict[str, float]]:
    """
    Benchmarks generation throughput and sieve efficiency across various bit lengths.

    Args:
        iterations: Number of primes generated per configuration.
        bit_lengths: List of bit lengths to evaluate (default [128, 256, 512]).

    Returns:
        dict: Performance statistics mapped by bit length.
    """
    if bit_lengths is None:
        bit_lengths = [128, 256, 512]

    stats = {}
    for bits in bit_lengths:
        total_time = 0.0
        total_candidates = 0
        total_sieve_passed = 0

        for _ in range(iterations):
            res = generate_512bit_prime(bit_length=bits, rounds=40, use_sieve=True)
            total_time += res.execution_time_seconds
            total_candidates += res.candidates_tested
            total_sieve_passed += res.passed_sieve_count

        avg_time = total_time / iterations
        avg_candidates = total_candidates / iterations
        avg_sieve_passed = total_sieve_passed / iterations
        sieve_rejection_rate = (1.0 - (avg_sieve_passed / avg_candidates)) * 100.0 if avg_candidates > 0 else 0.0

        stats[bits] = {
            "avg_time_sec": avg_time,
            "avg_candidates_tested": avg_candidates,
            "avg_sieve_passed": avg_sieve_passed,
            "sieve_rejection_pct": sieve_rejection_rate,
        }

    return stats
