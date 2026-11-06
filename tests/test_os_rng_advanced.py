"""
CryptoLabX — Unit Tests for Advanced NIST SP 800-22 Statistical Testing Suite
Author: Lakshay Ahuja (2024UCP1157)
Group: 17
"""

import pytest
import numpy as np
from analysis.os_rng.statistical_tests import (
    shannon_entropy,
    runs_test,
    longest_run_ones_test,
    discrete_fourier_transform_test,
    approximate_entropy_test,
    run_advanced_statistical_battery,
)
from analysis.os_rng.generator import generate_mt19937_bytes


class TestShannonEntropy:
    """Tests for Shannon entropy calculation."""

    def test_ideal_uniform_entropy(self):
        # 256 bytes with perfectly equal representation
        data = bytes(range(256)) * 100
        h = shannon_entropy(data)
        assert h == pytest.approx(8.0, abs=1e-5)

    def test_zero_entropy_single_byte(self):
        # All identical bytes have zero information
        data = b"\x00" * 1000
        h = shannon_entropy(data)
        assert h == 0.0

    def test_empty_entropy(self):
        assert shannon_entropy(b"") == 0.0


class TestRunsTest:
    """Tests for NIST SP 800-22 Runs Test."""

    def test_random_data_passes_runs(self):
        data = generate_mt19937_bytes(10000, seed=42)
        res = runs_test(data)
        assert res.passed is True
        assert res.p_value >= 0.01

    def test_all_zeros_fails_runs(self):
        data = b"\x00" * 1000
        res = runs_test(data)
        assert res.passed is False
        assert res.p_value == 0.0

    def test_alternating_bytes_fails_runs(self):
        # Extremely fast oscillation: 0x55 is 01010101
        data = b"\x55" * 1000
        res = runs_test(data)
        # All bits oscillate on every single bit, causing runs test failure
        assert res.passed is False

    def test_empty_data_raises_error(self):
        with pytest.raises(ValueError, match="Data cannot be empty"):
            runs_test(b"")


class TestLongestRunOfOnes:
    """Tests for Longest Run of Ones in a Block Test."""

    def test_random_data_passes(self):
        data = generate_mt19937_bytes(10000, seed=777)
        res = longest_run_ones_test(data)
        assert res.passed is True
        assert res.p_value >= 0.01


class TestDiscreteFourierTransform:
    """Tests for Spectral DFT Test."""

    def test_random_data_passes_dft(self):
        data = generate_mt19937_bytes(10000, seed=1234)
        res = discrete_fourier_transform_test(data)
        assert res.passed is True
        assert res.p_value >= 0.01


class TestApproximateEntropy:
    """Tests for Approximate Entropy Test."""

    def test_random_data_passes_apen(self):
        data = generate_mt19937_bytes(10000, seed=5678)
        res = approximate_entropy_test(data, m=2)
        assert res.passed is True
        assert res.p_value >= 0.01


class TestFullAdvancedBattery:
    """Tests for complete advanced testing battery."""

    def test_full_battery_execution(self):
        data = generate_mt19937_bytes(5000, seed=999)
        results = run_advanced_statistical_battery(data)
        assert "shannon_entropy" in results
        assert "runs_test" in results
        assert "longest_run_ones" in results
        assert "dft_spectral" in results
        assert "approx_entropy" in results
        assert results["shannon_entropy"] > 7.9

