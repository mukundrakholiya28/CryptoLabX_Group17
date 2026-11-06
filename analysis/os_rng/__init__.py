"""
CryptoLabX — OS Random Number Generation and Statistical Analysis Package
Group 17: Mukund Rakholiya (2024UCP1163) & Lakshay Ahuja (2024UCP1157)
"""

from analysis.os_rng.generator import (
    generate_windows_cng_bytes,
    generate_openssl_rand_bytes,
    generate_linux_urandom_bytes,
    generate_mt19937_bytes,
    generate_all_datasets,
)
from analysis.os_rng.metrics import (
    ByteFreqResult,
    BitDistResult,
    PatternResult,
    byte_frequency_distribution,
    bit_distribution,
    serial_correlation,
    compute_autocorrelation_vector,
    repeated_patterns_analysis,
    analyze_dataset,
)
from analysis.os_rng.statistical_tests import (
    TestResult,
    shannon_entropy,
    runs_test,
    longest_run_ones_test,
    discrete_fourier_transform_test,
    approximate_entropy_test,
    run_advanced_statistical_battery,
)
from analysis.os_rng.cli import run_comparative_cli

__all__ = [
    "generate_windows_cng_bytes",
    "generate_openssl_rand_bytes",
    "generate_linux_urandom_bytes",
    "generate_mt19937_bytes",
    "generate_all_datasets",
    "ByteFreqResult",
    "BitDistResult",
    "PatternResult",
    "byte_frequency_distribution",
    "bit_distribution",
    "serial_correlation",
    "compute_autocorrelation_vector",
    "repeated_patterns_analysis",
    "analyze_dataset",
    "TestResult",
    "shannon_entropy",
    "runs_test",
    "longest_run_ones_test",
    "discrete_fourier_transform_test",
    "approximate_entropy_test",
    "run_advanced_statistical_battery",
    "run_comparative_cli",
]
