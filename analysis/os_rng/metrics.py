"""
CryptoLabX — Assignment 9: OS RNG Statistical Metrics Analysis Engine
Author: Mukund Rakholiya (2024UCP1163)
Group: 17

This module implements low-level statistical metrics for assessing randomness:
1. Byte-Frequency Distribution & Chi-Square Goodness-of-Fit Test.
2. Bit Distribution (Monobit 0s vs 1s, proportion, z-score, p-value).
3. Serial Correlation (Lag-1 and Lag-k Pearson autocorrelation).
4. Repeated Pattern Analysis (consecutive identical byte runs, max run length, n-gram coverage).
"""

import math
from dataclasses import dataclass, field
from typing import Dict, List, Tuple
import numpy as np
from scipy import stats
from scipy.special import erfc


@dataclass
class ByteFreqResult:
    """Result container for byte-frequency analysis."""
    counts: np.ndarray
    sample_size: int
    expected_count: float
    min_count: int
    max_count: int
    mean_count: float
    std_count: float
    chi2_stat: float
    degrees_of_freedom: int
    p_value: float
    is_uniform: bool  # True if p_value > 0.01 (alpha = 0.01)

    def summary(self) -> str:
        status = "PASSED (Uniform)" if self.is_uniform else "FAILED (Non-uniform)"
        return (
            f"Byte Frequency: N={self.sample_size:,} bytes | Expected={self.expected_count:.1f}\n"
            f"Min={self.min_count} | Max={self.max_count} | Mean={self.mean_count:.2f} | Std={self.std_count:.2f}\n"
            f"Chi-Square: stat={self.chi2_stat:.4f}, df={self.degrees_of_freedom}, p-value={self.p_value:.6f} [{status}]"
        )


@dataclass
class BitDistResult:
    """Result container for bit-level distribution analysis."""
    total_bits: int
    zero_count: int
    one_count: int
    one_proportion: float
    bit_difference: int  # |ones - zeros|
    z_score: float
    p_value: float
    is_balanced: bool  # True if p_value > 0.01

    def summary(self) -> str:
        status = "PASSED (Balanced)" if self.is_balanced else "FAILED (Biased)"
        return (
            f"Bit Distribution: Total={self.total_bits:,} bits\n"
            f"Zeros={self.zero_count:,} ({100 - self.one_proportion * 100:.3f}%) | "
            f"Ones={self.one_count:,} ({self.one_proportion * 100:.3f}%)\n"
            f"Z-Score={self.z_score:.4f} | p-value={self.p_value:.6f} [{status}]"
        )


@dataclass
class PatternResult:
    """Result container for repeated patterns and run lengths."""
    max_identical_byte_run: int
    theoretical_expected_max_run: float
    run_length_distribution: Dict[int, int]
    unique_16bit_pairs: int
    total_16bit_pairs: int
    pair_coverage_ratio: float  # unique_16bit_pairs / 65536

    def summary(self) -> str:
        runs_str = ", ".join(f"len {k}: {v:,}" for k, v in sorted(self.run_length_distribution.items()) if k >= 2)
        return (
            f"Pattern Analysis: Max consecutive identical bytes={self.max_identical_byte_run} "
            f"(Theoretical Exp ~ {self.theoretical_expected_max_run:.2f})\n"
            f"Repeated Byte Runs: [{runs_str}]\n"
            f"16-bit Distinct Bigrams: {self.unique_16bit_pairs:,} / 65,536 "
            f"({self.pair_coverage_ratio * 100:.2f}% coverage)"
        )


def byte_frequency_distribution(data: bytes, alpha: float = 0.01) -> ByteFreqResult:
    """
    Analyzes the frequency of each byte value (0 to 255) and tests whether
    the distribution conforms to a discrete uniform distribution using Pearson's
    Chi-Square Goodness-of-Fit test.

    Null Hypothesis (H0): Byte values are uniformly distributed over [0, 255].
    Alternative Hypothesis (H1): Byte values deviate significantly from uniform.

    Args:
        data: Input byte sequence (>= 1,000 bytes recommended).
        alpha: Significance level threshold (default 0.01).

    Returns:
        ByteFreqResult: Complete distribution statistics and hypothesis test verdict.
    """
    n = len(data)
    if n == 0:
        raise ValueError("Data cannot be empty.")

    arr = np.frombuffer(data, dtype=np.uint8)
    counts = np.bincount(arr, minlength=256)
    expected = n / 256.0

    # Chi-Square statistic: sum((observed - expected)^2 / expected)
    chi2_stat = float(np.sum((counts - expected) ** 2 / expected))
    df = 255
    # Survival function (1 - CDF) gives the upper-tail p-value
    p_value = float(stats.chi2.sf(chi2_stat, df=df))
    is_uniform = p_value >= alpha

    return ByteFreqResult(
        counts=counts,
        sample_size=n,
        expected_count=expected,
        min_count=int(np.min(counts)),
        max_count=int(np.max(counts)),
        mean_count=float(np.mean(counts)),
        std_count=float(np.std(counts)),
        chi2_stat=chi2_stat,
        degrees_of_freedom=df,
        p_value=p_value,
        is_uniform=is_uniform,
    )


def bit_distribution(data: bytes, alpha: float = 0.01) -> BitDistResult:
    """
    Analyzes the bit-level distribution (Monobit test).
    Counts total 0s and 1s and computes the standard normal statistic
    and two-sided p-value based on the complementary error function.

    Null Hypothesis (H0): Bits are identically and independently distributed Bernoulli(0.5).

    Args:
        data: Input byte sequence.
        alpha: Significance level threshold (default 0.01).

    Returns:
        BitDistResult: Total bits, bit counts, proportion of ones, z-score, and p-value.
    """
    n_bytes = len(data)
    if n_bytes == 0:
        raise ValueError("Data cannot be empty.")

    arr = np.frombuffer(data, dtype=np.uint8)
    # Count set bits efficiently using byte-level popcount lookup table
    lut = np.array([bin(i).count('1') for i in range(256)], dtype=np.uint8)
    one_count = int(np.sum(lut[arr]))
    total_bits = n_bytes * 8
    zero_count = total_bits - one_count

    one_proportion = one_count / total_bits
    s_n = abs(one_count - zero_count)
    z_score = s_n / math.sqrt(total_bits)
    # Two-sided p-value: erfc(z / sqrt(2))
    p_value = float(erfc(z_score / math.sqrt(2.0)))
    is_balanced = p_value >= alpha

    return BitDistResult(
        total_bits=total_bits,
        zero_count=zero_count,
        one_count=one_count,
        one_proportion=one_proportion,
        bit_difference=s_n,
        z_score=z_score,
        p_value=p_value,
        is_balanced=is_balanced,
    )


def serial_correlation(data: bytes, lag: int = 1) -> float:
    """
    Computes Pearson's serial correlation coefficient (autocorrelation) at a specified byte lag.

    Formula:
        r_k = sum((X_i - X_mean) * (X_{i+k} - X_mean)) / sum((X_i - X_mean)^2)

    For an ideal random sequence of length N:
        E[r_k] = -1 / (N - 1) ~ 0
        Var[r_k] ~ 1 / N

    Args:
        data: Input byte sequence.
        lag: Byte offset distance (default 1).

    Returns:
        float: Correlation coefficient r_k in [-1.0, 1.0].
    """
    n = len(data)
    if n <= lag:
        raise ValueError(f"Data length ({n}) must be greater than lag ({lag}).")

    arr = np.frombuffer(data, dtype=np.uint8).astype(np.float64)
    mean = np.mean(arr)
    diff = arr - mean
    denominator = np.sum(diff ** 2)

    if denominator == 0:
        return 0.0

    numerator = np.sum(diff[:-lag] * diff[lag:])
    return float(numerator / denominator)


def compute_autocorrelation_vector(data: bytes, max_lag: int = 10) -> Dict[int, float]:
    """
    Computes autocorrelation for lags from 1 up to max_lag.

    Args:
        data: Input byte sequence.
        max_lag: Maximum lag offset to evaluate.

    Returns:
        dict[int, float]: Mapping of lag to correlation coefficient.
    """
    return {lag: serial_correlation(data, lag) for lag in range(1, max_lag + 1)}


def repeated_patterns_analysis(data: bytes) -> PatternResult:
    """
    Analyzes repeated patterns:
    1. Maximum run length of consecutive identical byte values.
    2. Distribution of consecutive run lengths (lengths >= 2).
    3. 16-bit word (bigram) collision rate and coverage over 2^16 = 65,536 space.

    Args:
        data: Input byte sequence.

    Returns:
        PatternResult: Pattern statistics, run distribution, and bigram coverage.
    """
    n = len(data)
    if n == 0:
        raise ValueError("Data cannot be empty.")

    arr = np.frombuffer(data, dtype=np.uint8)

    # 1. Consecutive identical byte runs
    # Find change points where arr[i] != arr[i-1]
    change_indices = np.where(arr[1:] != arr[:-1])[0] + 1
    # Run lengths are differences between successive change indices
    run_starts = np.r_[0, change_indices]
    run_ends = np.r_[change_indices, n]
    run_lengths = run_ends - run_starts

    max_run = int(np.max(run_lengths))
    # Count frequencies of runs of length >= 2
    unique_runs, counts = np.unique(run_lengths, return_counts=True)
    run_dist = {int(length): int(cnt) for length, cnt in zip(unique_runs, counts) if length >= 2}

    # Theoretical expected maximum run length for geometric distribution Geo(p=1/256):
    # E[L_max] ~ log_256(n) + gamma / ln(256) - 1/2
    gamma = 0.5772156649  # Euler-Mascheroni constant
    expected_max_run = (math.log(n) / math.log(256)) + (gamma / math.log(256)) - 0.5

    # 2. 16-bit bigram coverage
    # Pack adjacent bytes into 16-bit words
    bigrams = arr[:-1].astype(np.uint16) * 256 + arr[1:].astype(np.uint16)
    unique_bigrams = len(np.unique(bigrams))
    total_bigrams = n - 1
    coverage_ratio = unique_bigrams / 65536.0

    return PatternResult(
        max_identical_byte_run=max_run,
        theoretical_expected_max_run=expected_max_run,
        run_length_distribution=run_dist,
        unique_16bit_pairs=unique_bigrams,
        total_16bit_pairs=total_bigrams,
        pair_coverage_ratio=coverage_ratio,
    )


def analyze_dataset(data: bytes, name: str = "Dataset") -> Dict:
    """
    Runs full statistical battery on a dataset and returns aggregated metrics.

    Args:
        data: Raw byte sequence.
        name: Human-readable label for reporting.

    Returns:
        dict: Aggregated dictionary of all metric results.
    """
    bf = byte_frequency_distribution(data)
    bd = bit_distribution(data)
    sc1 = serial_correlation(data, lag=1)
    autocorr = compute_autocorrelation_vector(data, max_lag=5)
    pat = repeated_patterns_analysis(data)

    return {
        "name": name,
        "sample_size": len(data),
        "byte_freq": bf,
        "bit_dist": bd,
        "lag1_autocorr": sc1,
        "autocorr_vector": autocorr,
        "patterns": pat,
    }


if __name__ == "__main__":
    print("=" * 60)
    print("CryptoLabX — OS RNG Metrics Test Runner (Mukund Rakholiya)")
    print("=" * 60)

    import os
    dataset_files = [
        ("Linux /dev/urandom", "datasets/rng/linux_urandom_1mb.bin"),
        ("OpenSSL rand", "datasets/rng/openssl_rand_1mb.bin"),
        ("Windows CNG", "datasets/rng/windows_cng_1mb.bin"),
        ("MT19937 Baseline", "datasets/rng/mt19937_prng_1mb.bin"),
    ]

    for label, path in dataset_files:
        if os.path.exists(path):
            with open(path, "rb") as f:
                content = f.read()
            res = analyze_dataset(content, label)
            print(f"\n--- Analysis for: {label} ({len(content):,} bytes) ---")
            print(res["byte_freq"].summary())
            print(res["bit_dist"].summary())
            print(f"Lag-1 Serial Correlation: {res['lag1_autocorr']:.6f}")
            print(res["patterns"].summary())
