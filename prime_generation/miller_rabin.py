"""
Miller-Rabin Primality Testing Engine.

Author: Mukund Rakholiya (2024UCP1163)
Assignment: 8 - Prime Generation Using Miller-Rabin
"""

import math
import secrets
from typing import List, Optional, Tuple


def decompose(n: int) -> Tuple[int, int]:
    """
    Decomposes n - 1 into 2^s * d, where d is odd and s >= 1.
    
    Args:
        n: An odd integer greater than 2.
        
    Returns:
        A tuple (s, d) satisfying n - 1 = (2^s) * d with d odd.
        
    Raises:
        ValueError: If n <= 2 or n is even.
    """
    if n <= 2 or n % 2 == 0:
        raise ValueError(f"Decomposition requires an odd integer > 2, got {n}")

    d = n - 1
    s = 0
    while (d & 1) == 0:
        d >>= 1
        s += 1

    return s, d


def miller_rabin_test(n: int, a: int) -> bool:
    """
    Executes a single-base Miller-Rabin primality witness test for base a.
    
    Based on Fermat's Little Theorem and the non-existence of non-trivial square roots
    of 1 modulo a prime:
    - If n is prime and n - 1 = 2^s * d:
      Then either a^d = 1 (mod n) or a^(2^r * d) = -1 (mod n) for some 0 <= r < s.
    
    Args:
        n: The odd candidate integer (n > 2).
        a: Base integer in range [2, n - 2] (or will be reduced modulo n).
        
    Returns:
        True if n is probably prime with respect to base a,
        False if n is definitely composite (a is a witness to the compositeness of n).
    """
    if n <= 1:
        return False
    if n in (2, 3):
        return True
    if n % 2 == 0:
        return False

    # Normalize base a
    a = a % n
    if a <= 1 or a == n - 1:
        # Trivial bases are not conclusive witnesses; gcd check
        g = math.gcd(a, n)
        return g == 1 or g == n

    # Check GCD for composite detection directly
    g = math.gcd(a, n)
    if 1 < g < n:
        return False

    s, d = decompose(n)

    # Compute x = a^d mod n using fast modular exponentiation
    x = pow(a, d, n)

    if x == 1 or x == n - 1:
        return True

    # Repeatedly square x up to s - 1 times
    for _ in range(s - 1):
        x = pow(x, 2, n)
        if x == n - 1:
            return True
        if x == 1:
            # Found a non-trivial square root of 1 modulo n -> n is composite
            return False

    # Finished loop without finding -1 (mod n) -> n is composite
    return False


def is_probable_prime(
    n: int,
    rounds: int = 40,
    bases: Optional[List[int]] = None
) -> Tuple[bool, int]:
    """
    Performs multi-round Miller-Rabin primality testing on candidate n.
    
    Error Probability:
    For any odd composite, at most 1/4 of all possible bases can be false witnesses (liars).
    Therefore, with k independent random rounds:
        P(composite passes k rounds) <= 4^(-k).
    For k = 40 rounds, P(error) <= 4^(-40) approx 8.27 x 10^(-25).
    
    Args:
        n: Integer candidate to test.
        rounds: Number of random bases to test (default: 40).
        bases: Optional explicit list of bases to test. If provided, `rounds` is ignored
               and each base in `bases` is tested.
               
    Returns:
        A tuple (is_prime, rounds_passed):
        - is_prime: True if all rounds passed, False if any round failed.
        - rounds_passed: Total number of rounds successfully passed.
    """
    if n < 2:
        return False, 0
    if n in (2, 3):
        return True, 1
    if n % 2 == 0:
        return False, 0

    # If specific bases are provided, test them deterministically
    if bases is not None:
        passed = 0
        for b in bases:
            base = b % n
            if base <= 1 or base == n - 1:
                # Still check gcd
                if 1 < math.gcd(b, n) < n:
                    return False, passed
                passed += 1
                continue
            if not miller_rabin_test(n, base):
                return False, passed
            passed += 1
        return True, passed

    # If n is small enough that we can't pick enough unique bases in [2, n - 2]
    max_bases = n - 3
    if max_bases <= 0:
        return True, 1
    total_rounds = min(rounds, max_bases)

    # Pick cryptographically secure random unique bases in [2, n - 2]
    tested_bases = set()
    passed = 0

    while len(tested_bases) < total_rounds:
        # secrets.randbelow(n - 3) returns [0, n - 4] -> + 2 yields [2, n - 2]
        a = secrets.randbelow(n - 3) + 2
        if a in tested_bases:
            continue
        tested_bases.add(a)

        if not miller_rabin_test(n, a):
            return False, passed

        passed += 1

    return True, passed


def calculate_error_bound(rounds: int) -> float:
    """
    Calculates the theoretical upper bound on error probability P(error) <= 4^(-k).
    
    Args:
        rounds: Number of Miller-Rabin rounds executed.
        
    Returns:
        Maximum probability that a composite passed all rounds.
    """
    return 4.0 ** (-rounds)
