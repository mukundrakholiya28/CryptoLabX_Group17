"""
Prime Generation Package — Group 17.

Mukund Rakholiya (2024UCP1163) & Lakshay Ahuja (2024UCP1157)
"""

from prime_generation.candidate_generator import (
    generate_candidate,
    get_small_primes,
    sieve_of_small_primes,
    verify_bit_length,
)
from prime_generation.miller_rabin import (
    decompose,
    is_probable_prime,
    miller_rabin_test,
)
from prime_generation.pipeline import (
    PrimeGenerationResult,
    benchmark_generation,
    generate_512bit_prime,
)
from prime_generation.verifier import (
    VerificationResult,
    verify_prime_candidate,
)

__all__ = [
    "generate_candidate",
    "get_small_primes",
    "sieve_of_small_primes",
    "verify_bit_length",
    "decompose",
    "is_probable_prime",
    "miller_rabin_test",
    "PrimeGenerationResult",
    "generate_512bit_prime",
    "benchmark_generation",
    "VerificationResult",
    "verify_prime_candidate",
]
