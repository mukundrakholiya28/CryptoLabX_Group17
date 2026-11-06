"""
CryptoLabX — Assignment 9: Advanced NIST SP 800-22 Statistical Testing Suite
Author: Lakshay Ahuja (2024UCP1157)
Group: 17

This module implements advanced statistical tests for assessing cryptographic randomness:
1. NIST SP 800-22 Runs Test (Bit-level run transitions).
2. NIST Longest Run of Ones in a Block Test.
3. NIST Discrete Fourier Transform (DFT / Spectral) Test.
4. NIST Approximate Entropy Test.
5. Shannon Entropy Calculation (H ~ 8.0 bits/byte).
"""

import math
from dataclasses import dataclass
from typing import Dict, Tuple
import numpy as np
from scipy import stats
from scipy.special import erfc, gammaincc


@dataclass
class TestResult:
    """Standardized test result container for NIST statistical tests."""
    test_name: str
    statistic: float
    p_value: float
    passed: bool
    details: Dict[str, float]

    def summary(self) -> str:
        status = "PASSED" if self.passed else "FAILED"
        det_str = ", ".join(f"{k}={v:.4f}" if isinstance(v, float) else f"{k}={v}" for k, v in self.details.items())
        return f"[{status}] {self.test_name}: p-value={self.p_value:.6f}, Stat={self.statistic:.4f} ({det_str})"


def shannon_entropy(data: bytes) -> float:
    """
    Calculates the Shannon entropy in bits per byte:
        H = - sum(p_i * log2(p_i))
    Ideal true random data achieves H -> 8.0 bits/byte.

    Args:
        data: Input byte sequence.

    Returns:
        float: Entropy value in range [0.0, 8.0].
    """
    n = len(data)
    if n == 0:
        return 0.0

    arr = np.frombuffer(data, dtype=np.uint8)
    counts = np.bincount(arr, minlength=256)
    probs = counts[counts > 0] / float(n)
    return float(-np.sum(probs * np.log2(probs)))


def runs_test(data: bytes, alpha: float = 0.01) -> TestResult:
    """
    NIST SP 800-22 Section 2.2: Runs Test.
    Tests the total number of continuous runs of 0s and 1s to determine whether
    oscillation between bit states is too fast or too slow.

    Args:
        data: Input byte sequence.
        alpha: Significance level threshold (default 0.01).

    Returns:
        TestResult: Outcome of the runs test.
    """
    n_bytes = len(data)
    if n_bytes == 0:
        raise ValueError("Data cannot be empty.")

    # Convert to bit array
    arr = np.frombuffer(data, dtype=np.uint8)
    bits = np.unpackbits(arr)
    n = len(bits)

    # Step 1: Pre-requisite proportion test
    one_count = int(np.sum(bits))
    pi = one_count / float(n)
    if abs(pi - 0.5) >= (2.0 / math.sqrt(n)):
        return TestResult(
            test_name="NIST Runs Test",
            statistic=0.0,
            p_value=0.0,
            passed=False,
            details={"reason": "Failed pre-requisite frequency proportion", "pi": pi},
        )

    # Step 2: Compute observed runs V_n
    # Run transition occurs where bits[k] != bits[k+1]
    transitions = np.sum(bits[:-1] != bits[1:])
    v_n = int(transitions + 1)

    # Step 3: Compute test statistic Z and p-value
    numerator = abs(v_n - 2.0 * n * pi * (1.0 - pi))
    denominator = 2.0 * math.sqrt(2.0 * n) * pi * (1.0 - pi)

    if denominator == 0:
        p_val = 0.0
    else:
        p_val = float(erfc(numerator / (denominator * math.sqrt(2.0))))

    passed = p_val >= alpha

    return TestResult(
        test_name="NIST Runs Test",
        statistic=v_n,
        p_value=p_val,
        passed=passed,
        details={"total_runs": v_n, "expected_runs": 2.0 * n * pi * (1.0 - pi), "proportion_ones": pi},
    )


def longest_run_ones_test(data: bytes, alpha: float = 0.01) -> TestResult:
    """
    NIST SP 800-22 Section 2.3: Test for the Longest Run of Ones in a Block.
    Determines whether the longest run of ones within fixed sub-blocks conforms
    to the expected distribution.

    Args:
        data: Input byte sequence.
        alpha: Significance level threshold (default 0.01).

    Returns:
        TestResult: Chi-square statistic and p-value.
    """
    arr = np.frombuffer(data, dtype=np.uint8)
    bits = np.unpackbits(arr)
    n = len(bits)

    # Use standard NIST parameters: block size M = 128 bits
    m_block = 128
    k_categories = 6
    num_blocks = n // m_block

    if num_blocks < 10:
        # Fallback for very small datasets
        m_block = 8
        k_categories = 4
        num_blocks = n // m_block

    # Truncate to whole blocks
    bits_truncated = bits[:num_blocks * m_block].reshape(num_blocks, m_block)

    # NIST theoretical probabilities for M = 128, K = 5 (6 bins: <=4, 5, 6, 7, 8, >=9)
    pi_values = [0.1174, 0.2430, 0.2493, 0.1752, 0.1027, 0.1124]

    # Find longest run of ones in each block
    freq_bins = [0] * 6
    for block in bits_truncated:
        padded = np.r_[0, block.astype(np.int32), 0]
        diffs = np.diff(padded)
        starts = np.where(diffs == 1)[0]
        ends = np.where(diffs == -1)[0]
        max_run = int(np.max(ends - starts)) if len(starts) > 0 else 0

        if max_run <= 4:
            freq_bins[0] += 1
        elif max_run == 5:
            freq_bins[1] += 1
        elif max_run == 6:
            freq_bins[2] += 1
        elif max_run == 7:
            freq_bins[3] += 1
        elif max_run == 8:
            freq_bins[4] += 1
        else:
            freq_bins[5] += 1

    # Compute Chi-Square statistic
    chi2 = 0.0
    for obs, pi in zip(freq_bins, pi_values):
        exp = num_blocks * pi
        chi2 += ((obs - exp) ** 2) / exp

    df = 5
    p_val = float(gammaincc(df / 2.0, chi2 / 2.0))
    passed = p_val >= alpha

    return TestResult(
        test_name="NIST Longest Run of Ones Test",
        statistic=chi2,
        p_value=p_val,
        passed=passed,
        details={"blocks_evaluated": num_blocks, "degrees_of_freedom": df},
    )


def discrete_fourier_transform_test(data: bytes, alpha: float = 0.01) -> TestResult:
    """
    NIST SP 800-22 Section 2.6: Discrete Fourier Transform (Spectral) Test.
    Detects periodic features (repetitive patterns) in the bit sequence.

    Args:
        data: Input byte sequence (tested on first 100,000 bits for fast execution).
        alpha: Significance level threshold (default 0.01).

    Returns:
        TestResult: Peak statistics and p-value.
    """
    arr = np.frombuffer(data, dtype=np.uint8)
    bits = np.unpackbits(arr)

    # Subsample to 100,000 bits for computational efficiency if larger
    n = min(len(bits), 100000)
    bits_sub = bits[:n]

    # Convert 0, 1 bits to polar form: -1, +1
    x = 2 * bits_sub.astype(np.float64) - 1.0

    # Compute Fast Fourier Transform
    s = np.fft.fft(x)
    m = np.abs(s[:n // 2])

    # 95% threshold: T = sqrt(2.995732274 * n)
    t = math.sqrt(2.995732274 * n)
    n0 = 0.95 * (n / 2.0)
    n1 = float(np.sum(m < t))

    d = (n1 - n0) / math.sqrt(n * 0.95 * 0.05 / 4.0)
    p_val = float(erfc(abs(d) / math.sqrt(2.0)))
    passed = p_val >= alpha

    return TestResult(
        test_name="NIST Spectral (DFT) Test",
        statistic=d,
        p_value=p_val,
        passed=passed,
        details={"subsample_bits": n, "peak_threshold": t, "observed_sub_peaks": n1, "expected_peaks": n0},
    )


def approximate_entropy_test(data: bytes, m: int = 2, alpha: float = 0.01) -> TestResult:
    """
    NIST SP 800-22 Section 2.12: Approximate Entropy Test.
    Compares the frequency of overlapping blocks of consecutive lengths m and m+1.

    Args:
        data: Input byte sequence.
        m: Length of bit blocks (default 2).
        alpha: Significance level threshold (default 0.01).

    Returns:
        TestResult: ApEn statistic and p-value.
    """
    arr = np.frombuffer(data, dtype=np.uint8)
    bits = np.unpackbits(arr)
    n = min(len(bits), 50000)  # Standard evaluation block
    bits_sub = bits[:n]

    def _phi(block_len: int) -> float:
        # Augment with circular wrap-around
        augmented = np.r_[bits_sub, bits_sub[:block_len - 1]]
        # Extract all overlapping substrings
        patterns = np.zeros(2 ** block_len, dtype=np.int32)
        # Convert bit slices to integer pattern indices
        for i in range(n):
            sub = augmented[i:i + block_len]
            val = 0
            for b in sub:
                val = (val << 1) | b
            patterns[val] += 1
        probs = patterns[patterns > 0] / float(n)
        return float(np.sum(probs * np.log(probs)))

    phi_m = _phi(m)
    phi_m1 = _phi(m + 1)
    apen = phi_m - phi_m1

    chi2 = 2.0 * n * (math.log(2.0) - apen)
    df = 2 ** (m - 1)
    p_val = float(gammaincc(df / 2.0, chi2 / 2.0))
    passed = p_val >= alpha

    return TestResult(
        test_name="NIST Approximate Entropy Test",
        statistic=chi2,
        p_value=p_val,
        passed=passed,
        details={"block_length_m": m, "approx_entropy": apen, "chi2": chi2},
    )


def run_advanced_statistical_battery(data: bytes) -> Dict[str, TestResult]:
    """
    Executes full NIST SP 800-22 advanced statistical testing battery.

    Args:
        data: Input byte sequence.

    Returns:
        dict[str, TestResult]: Mapping of test identifiers to outcomes.
    """
    ent = shannon_entropy(data)
    runs = runs_test(data)
    l_ones = longest_run_ones_test(data)
    dft = discrete_fourier_transform_test(data)
    apen = approximate_entropy_test(data, m=2)

    return {
        "shannon_entropy": ent,
        "runs_test": runs,
        "longest_run_ones": l_ones,
        "dft_spectral": dft,
        "approx_entropy": apen,
    }
