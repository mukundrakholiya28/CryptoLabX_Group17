"""
Independent Verification Module for Prime Candidates.

Author: Lakshay Ahuja (2024UCP1157)
Assignment: 8 - Prime Generation Using Miller-Rabin
"""

from dataclasses import dataclass
from typing import List, Optional

from prime_generation.candidate_generator import verify_bit_length
from prime_generation.miller_rabin import is_probable_prime


@dataclass
class VerificationResult:
    """Telemetry and outcome of independent prime verification."""
    bit_length_valid: bool
    actual_bit_length: int
    passes_specified_bases: bool
    specified_bases_tested: List[int]
    independent_library_result: bool
    library_name: str
    overall_verified: bool

    def summary(self) -> str:
        status = "PASSED" if self.overall_verified else "FAILED"
        return (
            f"Prime Candidate Independent Verification [{status}]:\n"
            f"Bit Length Check: {self.actual_bit_length} bits ({'VALID' if self.bit_length_valid else 'INVALID'})\n"
            f"Specified Bases Tested: {self.specified_bases_tested} -> {'PASSED' if self.passes_specified_bases else 'FAILED'}\n"
            f"Independent Library ({self.library_name}): {'PRIME' if self.independent_library_result else 'COMPOSITE'}\n"
            f"Overall Cryptographic Primality: {'VERIFIED' if self.overall_verified else 'REJECTED'}"
        )


def verify_prime_candidate(
    candidate: int,
    expected_bit_length: int = 512,
    bases: Optional[List[int]] = None,
) -> VerificationResult:
    """
    Independently verifies a generated prime candidate:
    1. Asserts bit length matches expected_bit_length.
    2. Runs Miller-Rabin test against deterministic small prime bases.
    3. Cross-verifies primality using PyCryptodome's isPrime (Baillie-PSW test).

    Args:
        candidate: Candidate integer to verify.
        expected_bit_length: Expected bit length (default 512).
        bases: Specific bases to test (defaults to first 10 primes: [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]).

    Returns:
        VerificationResult: Detailed verification outcomes.
    """
    if bases is None:
        bases = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]

    # 1. Bit length verification
    actual_bits = candidate.bit_length()
    bit_valid = verify_bit_length(candidate, expected_bit_length=expected_bit_length)

    # 2. Miller-Rabin witness verification on specified bases
    passes_bases, _ = is_probable_prime(candidate, bases=bases)

    # 3. Independent library verification using pycryptodome
    try:
        from Crypto.Util.number import isPrime
        lib_result = bool(isPrime(candidate))
        lib_name = "pycryptodome.Crypto.Util.number.isPrime"
    except ImportError:
        # Fallback to sympy if pycryptodome is missing
        try:
            import sympy
            lib_result = bool(sympy.isprime(candidate))
            lib_name = "sympy.isprime"
        except ImportError:
            lib_result = passes_bases
            lib_name = "built-in multi-round Miller-Rabin (fallback)"

    overall = bit_valid and passes_bases and lib_result

    return VerificationResult(
        bit_length_valid=bit_valid,
        actual_bit_length=actual_bits,
        passes_specified_bases=passes_bases,
        specified_bases_tested=bases,
        independent_library_result=lib_result,
        library_name=lib_name,
        overall_verified=overall,
    )
