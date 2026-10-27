"""
Comprehensive Unit Test Suite for Candidate Generation and Miller-Rabin Primality Test.

Author: Mukund Rakholiya (2024UCP1163)
Assignment: 8 - Prime Generation Using Miller-Rabin
"""

import math
import pytest

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


class TestCandidateGenerator:
    """Test suite for random odd candidate integer generation and sieve."""

    def test_generate_candidate_exact_512_bit_length(self):
        """Verify that generate_candidate(512) produces integers of exact 512 bits."""
        for _ in range(20):
            candidate = generate_candidate(512)
            assert candidate.bit_length() == 512
            assert verify_bit_length(candidate, 512) is True
            # Verify MSB is set (2^511 <= candidate < 2^512)
            assert (1 << 511) <= candidate < (1 << 512)

    @pytest.mark.parametrize("bits", [16, 64, 128, 256, 512, 1024])
    def test_generate_candidate_various_bit_lengths(self, bits):
        """Verify candidate generation across multiple cryptographic bit lengths."""
        candidate = generate_candidate(bits)
        assert candidate.bit_length() == bits
        assert verify_bit_length(candidate, bits) is True

    def test_generate_candidate_is_odd(self):
        """Verify that every generated candidate is odd (LSB is 1)."""
        for _ in range(50):
            candidate = generate_candidate(512)
            assert candidate % 2 == 1
            assert (candidate & 1) == 1

    def test_generate_candidate_invalid_bit_length(self):
        """Verify that bit lengths < 2 raise ValueError."""
        with pytest.raises(ValueError):
            generate_candidate(1)
        with pytest.raises(ValueError):
            generate_candidate(0)
        with pytest.raises(ValueError):
            generate_candidate(-10)

    def test_get_small_primes_count_and_caching(self):
        """Verify the sieve of small primes up to 1000 produces exactly 168 primes."""
        primes = get_small_primes(1000)
        assert len(primes) == 168
        assert primes[0] == 2
        assert primes[1] == 3
        assert primes[-1] == 997

        # Verify caching returns identical object
        primes2 = get_small_primes(1000)
        assert primes is primes2

    def test_sieve_of_small_primes_detects_composites(self):
        """Verify that multiples of small primes are rejected by the sieve."""
        primes = get_small_primes(1000)
        # Small primes themselves pass
        for p in [2, 3, 5, 7, 11, 13, 997]:
            assert sieve_of_small_primes(p, primes) is True

        # Multiples of 3, 5, 7, 11 fail
        assert sieve_of_small_primes(9, primes) is False
        assert sieve_of_small_primes(15, primes) is False
        assert sieve_of_small_primes(21, primes) is False
        assert sieve_of_small_primes(77, primes) is False
        assert sieve_of_small_primes(3 * 997, primes) is False
        assert sieve_of_small_primes(13 * 17, primes) is False

    def test_verify_bit_length_edge_cases(self):
        """Verify edge cases for verify_bit_length."""
        assert verify_bit_length(0, 512) is False
        assert verify_bit_length(-5, 512) is False
        assert verify_bit_length((1 << 511), 512) is True
        assert verify_bit_length((1 << 512) - 1, 512) is True
        assert verify_bit_length((1 << 512), 512) is False


class TestDecomposition:
    """Test suite for n - 1 = 2^s * d decomposition."""

    @pytest.mark.parametrize(
        "n, expected_s, expected_d",
        [
            (3, 1, 1),       # 3 - 1 = 2 = 2^1 * 1
            (5, 2, 1),       # 5 - 1 = 4 = 2^2 * 1
            (7, 1, 3),       # 7 - 1 = 6 = 2^1 * 3
            (9, 3, 1),       # 9 - 1 = 8 = 2^3 * 1
            (17, 4, 1),      # 17 - 1 = 16 = 2^4 * 1
            (21, 2, 5),      # 21 - 1 = 20 = 2^2 * 5
            (221, 2, 55),    # 221 - 1 = 220 = 2^2 * 55
        ],
    )
    def test_decompose_known_values(self, n, expected_s, expected_d):
        s, d = decompose(n)
        assert s == expected_s
        assert d == expected_d
        assert (2**s) * d == n - 1
        assert d % 2 == 1

    def test_decompose_large_odd_integer(self):
        candidate = generate_candidate(512)
        s, d = decompose(candidate)
        assert s >= 1
        assert d % 2 == 1
        assert (1 << s) * d == candidate - 1

    def test_decompose_invalid_inputs(self):
        with pytest.raises(ValueError):
            decompose(2)  # Even
        with pytest.raises(ValueError):
            decompose(4)  # Even
        with pytest.raises(ValueError):
            decompose(0)
        with pytest.raises(ValueError):
            decompose(-7)


class TestMillerRabinWitnessTest:
    """Test suite for single-base Miller-Rabin primality witness testing."""

    @pytest.mark.parametrize(
        "prime",
        [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71],
    )
    def test_known_small_primes_pass(self, prime):
        """All small primes must pass witness tests."""
        for base in [2, 3, 5]:
            assert miller_rabin_test(prime, base) is True

    @pytest.mark.parametrize(
        "composite",
        [4, 6, 8, 9, 10, 12, 14, 15, 16, 18, 20, 21, 22, 24, 25, 26, 27, 28, 33, 35, 49, 121],
    )
    def test_known_small_composites_fail(self, composite):
        """Small composites must fail for tested witnesses."""
        has_witness = False
        for base in range(2, composite):
            if not miller_rabin_test(composite, base):
                has_witness = True
                break
        assert has_witness is True

    @pytest.mark.parametrize(
        "carmichael",
        [561, 1105, 1729, 2465, 2821, 6601, 8911],
    )
    def test_carmichael_numbers_fail_miller_rabin(self, carmichael):
        """
        Carmichael numbers fool Fermat's test for all coprime bases,
        but Miller-Rabin detects their compositeness with high probability.
        """
        is_prime, _ = is_probable_prime(carmichael, rounds=20)
        assert is_prime is False
        assert miller_rabin_test(561, 2) is False

    def test_miller_rabin_edge_cases(self):
        """Verify handling of edge values."""
        assert miller_rabin_test(0, 2) is False
        assert miller_rabin_test(1, 2) is False
        assert miller_rabin_test(2, 2) is True
        assert miller_rabin_test(3, 2) is True
        assert miller_rabin_test(4, 2) is False


class TestIsProbablePrime:
    """Test suite for multi-round Miller-Rabin testing."""

    @pytest.mark.parametrize(
        "prime",
        [
            104729,             # 10,000th prime
            2147483647,         # Mersenne prime M31 = 2^31 - 1
            2305843009213693951 # Mersenne prime M61 = 2^61 - 1
        ],
    )
    def test_known_large_primes(self, prime):
        """Verify that known large primes pass 40 rounds of Miller-Rabin."""
        is_prime, rounds_passed = is_probable_prime(prime, rounds=40)
        assert is_prime is True
        assert rounds_passed == 40

    def test_custom_specified_bases(self):
        """Verify primality testing using explicit deterministic bases."""
        specified_bases = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37]
        is_prime, passed = is_probable_prime(97, bases=specified_bases)
        assert is_prime is True
        assert passed == len(specified_bases)

        is_prime, _ = is_probable_prime(91, bases=specified_bases)
        assert is_prime is False

    def test_error_probability_calculation(self):
        """Verify calculation of error bounds."""
        assert calculate_error_bound(1) == 0.25
        assert calculate_error_bound(2) == 0.0625
        assert calculate_error_bound(4) == pytest.approx(1 / 256)
        assert calculate_error_bound(40) == pytest.approx(4**(-40))
        assert calculate_error_bound(40) < 1e-24

    def test_composite_product_of_two_large_primes(self):
        """Verify that the product of two distinct 64-bit primes is detected as composite."""
        p = 18446744073709551557  # Largest prime < 2^64
        q = 18446744073709551533
        n = p * q
        is_prime, _ = is_probable_prime(n, rounds=10)
        assert is_prime is False
