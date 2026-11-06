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
    print("=" * 85)
    print("CryptoLabX — Assignment 8: 512-bit Probable Prime Generation Report")
    print("Team: Group 17 | Mukund Rakholiya (2024UCP1163) & Lakshay Ahuja (2024UCP1157)")
    print("=" * 85)

    print("\n[*] Step 1: Executing Prime Generation Pipeline...")
    gen_result = generate_512bit_prime(bit_length=512, rounds=40, use_sieve=True)

    print("\n" + "=" * 85)
    print("ASSIGNMENT 8: EXPERIMENTAL RESULTS TABLE (SUBMISSION FORMAT)")
    print("=" * 85)
    sep = "+" + "-" * 39 + "+" + "-" * 43 + "+"
    print(sep)
    print(f"| {'Parameter':<37} | {'Value':<41} |")
    print(sep)
    print(f"| {'Assigned bit length':<37} | {gen_result.assigned_bit_length:<41} |")
    print(f"| {'Generated prime candidate (Decimal)':<37} | {str(gen_result.candidate)[:38] + '...':<41} |")
    print(f"| {'Generated prime candidate (Hex)':<37} | {hex(gen_result.candidate)[:38] + '...':<41} |")
    print(f"| {'Actual bit length of the candidate':<37} | {gen_result.bit_length:<41} |")
    print(f"| {'Number of candidates tested':<37} | {gen_result.candidates_tested:<41} |")
    print(f"| {'Number of candidates passed sieve':<37} | {gen_result.passed_sieve_count:<41} |")
    print(f"| {'Number of Miller–Rabin rounds':<37} | {gen_result.rounds_performed:<41} |")
    print(f"| {'Total execution time':<37} | {f'{gen_result.execution_time_seconds:.4f} seconds':<41} |")
    print(sep)

    print("\nFull 512-bit Prime Candidate (Decimal):")
    print(gen_result.candidate)
    print("\nFull 512-bit Prime Candidate (Hex):")
    print(hex(gen_result.candidate))

    print("\n" + "=" * 85)
    print("ASSIGNMENT 8: VERIFICATION DEMONSTRATION")
    print("=" * 85)
    test_bases = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37]
    ver_result = verify_prime_candidate(
        candidate=gen_result.candidate,
        expected_bit_length=512,
        bases=test_bases,
    )
    print(f"1. Bit Length Verification : {gen_result.bit_length} == 512 -> [{'PASSED' if ver_result.bit_length_valid else 'FAILED'}]")
    print(f"   Bounds Check            : 2^511 <= p < 2^512 -> {2**511 <= gen_result.candidate < 2**512}")
    print(f"2. Specified Bases Tested  : {test_bases}")
    print(f"   Miller-Rabin Result     : [{'PASSED' if ver_result.passes_specified_bases else 'FAILED'}] (all 12 bases confirmed prime witness)")
    print(f"3. Independent Library     : {ver_result.library_name}")
    print(f"   Independent Result      : [{'PRIME' if ver_result.independent_library_result else 'COMPOSITE'}]")
    print(f"   Overall Verification    : [{'VERIFIED PROBABLE PRIME' if ver_result.overall_verified else 'REJECTED'}]")

    print("\n" + "=" * 85)
    print("PERFORMANCE PROFILING & SIEVE BENCHMARK")
    print("=" * 85)
    bench = benchmark_generation(iterations=2, bit_lengths=[128, 256, 512])
    print("| Bit Length | Avg Candidates Tested | Passed Sieve | Sieve Rejection % | Avg Time (s) |")
    print("| :--- | :--- | :--- | :--- | :--- |")
    for bits, data in bench.items():
        print(
            f"| {bits:4d} bits | {data['avg_candidates_tested']:21.1f} | "
            f"{data['avg_sieve_passed']:12.1f} | {data['sieve_rejection_pct']:16.2f}% | "
            f"{data['avg_time_sec']:10.4f} s |"
        )

    print("=" * 85)


if __name__ == "__main__":
    run_submission_report()
