"""
Interactive CLI Runner and Report Generator for Prime Generation.

Author: Lakshay Ahuja (2024UCP1157)
Assignment: 8 - Prime Generation Using Miller-Rabin
"""

import os
import sys
sys.path.append(os.path.abspath("."))
from prime_generation.pipeline import generate_512bit_prime, benchmark_generation
from prime_generation.verifier import verify_prime_candidate


def run_submission_report():
    """Generates and displays formatted submission report for Assignment 8."""
    print("=" * 75)
    print("CryptoLabX — Assignment 8: 512-bit Probable Prime Generation Report")
    print("Team: Group 17 | Mukund Rakholiya (2024UCP1163) & Lakshay Ahuja (2024UCP1157)")
    print("=" * 75)

    print("\n[+] Step 1: Executing Prime Generation Pipeline...")
    gen_result = generate_512bit_prime(bit_length=512, rounds=40, use_sieve=True)
    print(gen_result.summary())

    print("\n[+] Step 2: Executing Independent Multi-Layer Verification...")
    test_bases = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37]
    ver_result = verify_prime_candidate(
        candidate=gen_result.candidate,
        expected_bit_length=512,
        bases=test_bases,
    )
    print(ver_result.summary())

    print("\n[+] Step 3: Performance Profiling & Sieve Benchmark...")
    bench = benchmark_generation(iterations=2, bit_lengths=[128, 256, 512])
    print("\n| Bit Length | Avg Candidates Tested | Passed Sieve | Sieve Rejection % | Avg Time (s) |")
    print("| :--- | :--- | :--- | :--- | :--- |")
    for bits, data in bench.items():
        print(
            f"| {bits} bits | {data['avg_candidates_tested']:.1f} | "
            f"{data['avg_sieve_passed']:.1f} | {data['sieve_rejection_pct']:.2f}% | "
            f"{data['avg_time_sec']:.4f} s |"
        )

    print("=" * 75)
    print("Assignment 8 Execution & Verification Completed Successfully.")


if __name__ == "__main__":
    run_submission_report()
