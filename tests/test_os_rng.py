"""
CryptoLabX — Unit Tests for OS RNG Data Generation & Statistical Metrics Engine
Author: Mukund Rakholiya (2024UCP1163)
Group: 17
"""

import math
import numpy as np
import pytest

from analysis.os_rng.generator import (
    generate_windows_cng_bytes,
    generate_openssl_rand_bytes,
    generate_linux_urandom_bytes,
    generate_mt19937_bytes,
)
from analysis.os_rng.metrics import (
    byte_frequency_distribution,
    bit_distribution,
    serial_correlation,
    compute_autocorrelation_vector,
    repeated_patterns_analysis,
    analyze_dataset,
)


class TestOSRNGGenerators:
    """Tests for multi-platform cryptographic random number generators."""

    def test_windows_cng_generator(self):
        length = 1024
        data = generate_windows_cng_bytes(length)
        assert isinstance(data, bytes)
        assert len(data) == length
        # Assert non-trivial entropy (not all zeros)
        assert len(set(data)) > 10

    def test_openssl_rand_generator(self):
        length = 512
        data = generate_openssl_rand_bytes(length)
        assert isinstance(data, bytes)
        assert len(data) == length
        assert len(set(data)) > 10

    def test_linux_urandom_generator(self):
        length = 512
        data = generate_linux_urandom_bytes(length)
        assert isinstance(data, bytes)
        assert len(data) == length
        assert len(set(data)) > 10

    def test_mt19937_generator_determinism(self):
        length = 256
        data1 = generate_mt19937_bytes(length, seed=12345)
        data2 = generate_mt19937_bytes(length, seed=12345)
        data3 = generate_mt19937_bytes(length, seed=99999)
        assert data1 == data2
        assert data1 != data3


class TestByteFrequencyDistribution:
    """Tests for byte-frequency distribution and Chi-Square goodness-of-fit."""

    def test_uniform_distribution_passes(self):
        # Construct synthetic uniform distribution: every byte 0..255 appears exactly 100 times
        synthetic_uniform = bytes(range(256)) * 100
        res = byte_frequency_distribution(synthetic_uniform)
        assert res.sample_size == 25600
        assert res.expected_count == 100.0
        assert res.min_count == 100
        assert res.max_count == 100
        assert res.chi2_stat == pytest.approx(0.0, abs=1e-6)
        assert res.p_value == pytest.approx(1.0, abs=1e-6)
        assert res.is_uniform is True

    def test_biased_distribution_fails(self):
        # Highly biased data: only 0x41 ('A')
        biased_data = b"A" * 1000
        res = byte_frequency_distribution(biased_data)
        assert res.chi2_stat > 1000.0
        assert res.p_value < 1e-10
        assert res.is_uniform is False

    def test_empty_input_raises_error(self):
        with pytest.raises(ValueError, match="Data cannot be empty"):
            byte_frequency_distribution(b"")


class TestBitDistribution:
    """Tests for bit-level distribution and Monobit test."""

    def test_balanced_bits(self):
        # 0x55 is 01010101 (exactly 4 zeros, 4 ones per byte)
        balanced_data = bytes([0x55]) * 1000
        res = bit_distribution(balanced_data)
        assert res.total_bits == 8000
        assert res.zero_count == 4000
        assert res.one_count == 4000
        assert res.one_proportion == 0.5
        assert res.z_score == 0.0
        assert res.p_value == 1.0
        assert res.is_balanced is True

    def test_all_zeros_fails(self):
        zeros_data = bytes([0x00]) * 500
        res = bit_distribution(zeros_data)
        assert res.zero_count == 4000
        assert res.one_count == 0
        assert res.one_proportion == 0.0
        assert res.p_value < 1e-10
        assert res.is_balanced is False

    def test_empty_input_raises_error(self):
        with pytest.raises(ValueError, match="Data cannot be empty"):
            bit_distribution(b"")


class TestSerialCorrelation:
    """Tests for Pearson autocorrelation."""

    def test_independent_random_data_low_correlation(self):
        # Generate PRNG sequence
        data = generate_mt19937_bytes(65536, seed=42)
        r1 = serial_correlation(data, lag=1)
        # For N=65536, standard error is 1/sqrt(N) = 1/256 ~ 0.0039
        assert abs(r1) < 0.03

    def test_repeating_pattern_high_correlation(self):
        # Repeating pattern: 1, 2, 3, 4, 1, 2, 3, 4...
        pattern = bytes([10, 20, 30, 40]) * 1000
        # Lag 4 should have near perfect correlation (> 0.99)
        r4 = serial_correlation(pattern, lag=4)
        assert r4 > 0.99

    def test_autocorrelation_vector(self):
        data = generate_mt19937_bytes(4096, seed=777)
        lags = compute_autocorrelation_vector(data, max_lag=5)
        assert len(lags) == 5
        assert all(isinstance(v, float) for v in lags.values())

    def test_invalid_lag_raises_error(self):
        with pytest.raises(ValueError, match="must be greater than lag"):
            serial_correlation(b"abc", lag=5)


class TestRepeatedPatternAnalysis:
    """Tests for repeated byte runs and bigram coverage."""

    def test_pattern_detection(self):
        # Byte sequence with known run of 5 identical bytes: 0xFF * 5
        data = b"hello" + (b"\xFF" * 5) + b"world"
        res = repeated_patterns_analysis(data)
        assert res.max_identical_byte_run == 5
        assert 5 in res.run_length_distribution
        assert res.run_length_distribution[5] == 1

    def test_bigram_coverage(self):
        # Full uniform sequence contains high bigram coverage
        data = generate_mt19937_bytes(200000, seed=123)
        res = repeated_patterns_analysis(data)
        assert res.pair_coverage_ratio > 0.90  # >90% coverage for 200k bytes


class TestFullBatteryAnalysis:
    """Tests full pipeline analyzer wrapper."""

    def test_analyze_dataset(self):
        data = generate_mt19937_bytes(10000, seed=999)
        res = analyze_dataset(data, "TestPRNG")
        assert res["name"] == "TestPRNG"
        assert res["sample_size"] == 10000
        assert "byte_freq" in res
        assert "bit_dist" in res
        assert "lag1_autocorr" in res
        assert "patterns" in res
