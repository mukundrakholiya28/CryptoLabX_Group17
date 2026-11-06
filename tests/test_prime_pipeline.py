"""
Unit Tests for Prime Generation Pipeline, Benchmarks, and Independent Verifier.

Author: Lakshay Ahuja (2024UCP1157)
Assignment: 8 - Prime Generation Using Miller-Rabin
"""

import pytest
from prime_generation.pipeline import generate_512bit_prime, benchmark_generation
from prime_generation.verifier import verify_prime_candidate


class TestPrimeGenerationPipeline:
    """Tests for generation pipeline orchestrator."""

    def test_generate_128bit_prime(self):
        res = generate_512bit_prime(bit_length=128, rounds=20, use_sieve=True)
        assert res.bit_length == 128
        assert res.assigned_bit_length == 128
        assert res.candidates_tested >= 1
        assert res.passed_sieve_count >= 1
        assert res.execution_time_seconds > 0

    def test_generate_512bit_prime(self):
        res = generate_512bit_prime(bit_length=512, rounds=40, use_sieve=True)
        assert res.bit_length == 512
        assert res.assigned_bit_length == 512
        assert res.rounds_performed == 40

    def test_invalid_bit_length_raises_error(self):
        with pytest.raises(ValueError, match="Bit length must be >= 2"):
            generate_512bit_prime(bit_length=1)

    def test_benchmark_generation(self):
        bench = benchmark_generation(iterations=1, bit_lengths=[128])
        assert 128 in bench
        assert "avg_time_sec" in bench[128]
        assert "avg_candidates_tested" in bench[128]
        assert "sieve_rejection_pct" in bench[128]


class TestPrimeVerifier:
    """Tests for independent verification."""

    def test_verify_known_prime(self):
        # Known small prime
        p = 65537
        res = verify_prime_candidate(p, expected_bit_length=17, bases=[2, 3, 5])
        assert res.bit_length_valid is True
        assert res.passes_specified_bases is True
        assert res.independent_library_result is True
        assert res.overall_verified is True

    def test_verify_composite_rejected(self):
        # Known composite: 65535 = 3 * 5 * 17 * 257
        c = 65535
        res = verify_prime_candidate(c, expected_bit_length=16, bases=[2, 3])
        assert res.passes_specified_bases is False
        assert res.independent_library_result is False
        assert res.overall_verified is False

    def test_verify_bit_length_mismatch(self):
        p = 65537  # 17 bits
        res = verify_prime_candidate(p, expected_bit_length=512)
        assert res.bit_length_valid is False
        assert res.overall_verified is False

