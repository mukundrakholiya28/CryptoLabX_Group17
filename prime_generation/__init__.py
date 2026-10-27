"""
Cryptographic Prime Generation Package.

Group 17:
- Mukund Rakholiya (2024UCP1163) - Candidate Generation & Miller-Rabin Testing Core
- Lakshay Ahuja (2024UCP1157) - Pipeline Orchestrator, Verifier, & CLI
"""

from prime_generation.candidate_generator import (
    generate_candidate,
    get_small_primes,
    sieve_of_small_primes,
    verify_bit_length,
)
from prime_generation.miller_rabin import (
    calculate_error_bound,
    decompose,
    is_probable_prime,
    miller_rabin_test,
)

__all__ = [
    "generate_candidate",
    "get_small_primes",
    "sieve_of_small_primes",
    "verify_bit_length",
    "decompose",
    "miller_rabin_test",
    "is_probable_prime",
    "calculate_error_bound",
]
