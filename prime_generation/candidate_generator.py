"""
Candidate Generator Module for Cryptographic Prime Generation.

Author: Mukund Rakholiya (2024UCP1163)
Assignment: 8 - Prime Generation Using Miller-Rabin
"""

import secrets
from typing import List, Optional


# Global cache for small primes to avoid redundant sieve recalculations
_CACHED_SMALL_PRIMES: Optional[List[int]] = None


def get_small_primes(limit: int = 1000) -> List[int]:
    """
    Computes a list of small primes up to `limit` using the Sieve of Eratosthenes.
    Results are cached for performance.
    
    Args:
        limit: Upper bound for small primes (default: 1000).
        
    Returns:
        List of prime numbers up to `limit`.
    """
    global _CACHED_SMALL_PRIMES
    if _CACHED_SMALL_PRIMES is not None and limit == 1000:
        return _CACHED_SMALL_PRIMES

    if limit < 2:
        return []

    is_prime = [True] * (limit + 1)
    is_prime[0] = is_prime[1] = False

    p = 2
    while p * p <= limit:
        if is_prime[p]:
            for i in range(p * p, limit + 1, p):
                is_prime[i] = False
        p += 1

    primes = [p for p in range(2, limit + 1) if is_prime[p]]
    if limit == 1000:
        _CACHED_SMALL_PRIMES = primes
    return primes


def generate_candidate(bit_length: int = 512) -> int:
    """
    Generates a cryptographically secure random odd candidate integer of exact bit length.
    
    Guarantees:
    1. MSB is set to 1: Ensures 2^(bit_length - 1) <= candidate < 2^bit_length.
    2. LSB is set to 1: Ensures the candidate is odd (eliminates trivial even composites).
    3. candidate.bit_length() == bit_length.
    
    Args:
        bit_length: Desired bit length (default: 512).
        
    Returns:
        A positive odd integer with exact bit length.
        
    Raises:
        ValueError: If bit_length < 2.
    """
    if bit_length < 2:
        raise ValueError(f"Bit length must be at least 2, got {bit_length}")

    # Generate random bits using cryptographically secure PRNG (secrets)
    candidate = secrets.randbits(bit_length)

    # Set MSB to ensure exact bit length
    candidate |= (1 << (bit_length - 1))

    # Set LSB to ensure the candidate is odd
    candidate |= 1

    return candidate


def sieve_of_small_primes(candidate: int, small_primes: Optional[List[int]] = None) -> bool:
    """
    Performs trial-division pre-screening of a candidate against small primes.
    Eliminates ~85%+ of random odd composites before executing expensive
    Miller-Rabin modular exponentiations.
    
    Args:
        candidate: The integer candidate to test.
        small_primes: Optional precomputed list of small primes.
                     If None, primes up to 1000 are used.
                     
    Returns:
        True if the candidate is not divisible by any small prime (or is a small prime itself),
        False if the candidate is composite.
    """
    if candidate < 2:
        return False

    primes = small_primes if small_primes is not None else get_small_primes(1000)

    for p in primes:
        if candidate == p:
            return True
        if candidate % p == 0:
            return False

    return True


def verify_bit_length(n: int, expected_bit_length: int = 512) -> bool:
    """
    Verifies that the integer n has exactly the expected bit length.
    
    Args:
        n: Integer to verify.
        expected_bit_length: Expected bit length (default: 512).
        
    Returns:
        True if n.bit_length() == expected_bit_length, else False.
    """
    if n <= 0:
        return False
    return n.bit_length() == expected_bit_length
