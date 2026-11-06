"""
CryptoLabX — Script to generate visualization plots for Assignment 9
"""

import os
import sys
sys.path.append(os.path.abspath("."))
import matplotlib.pyplot as plt
import numpy as np
from analysis.os_rng.metrics import analyze_dataset

def main():
    datasets = [
        ("Linux /dev/urandom", "datasets/rng/linux_urandom_1mb.bin"),
        ("OpenSSL rand", "datasets/rng/openssl_rand_1mb.bin"),
        ("Windows CNG", "datasets/rng/windows_cng_1mb.bin"),
        ("MT19937 Baseline", "datasets/rng/mt19937_prng_1mb.bin"),
    ]

    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    axes = axes.flatten()

    for idx, (name, path) in enumerate(datasets):
        with open(path, "rb") as f:
            data = f.read()
        res = analyze_dataset(data, name)
        ax = axes[idx]
        counts = res["byte_freq"].counts
        ax.bar(range(256), counts, color="#1f77b4", alpha=0.75, width=1.0)
        ax.axhline(4096, color="crimson", linestyle="--", linewidth=1.5, label="Expected Uniform (4,096)")
        chi2 = res["byte_freq"].chi2_stat
        pval = res["byte_freq"].p_value
        ax.set_title(f"{name}\nChi-Sq: {chi2:.2f} (df=255, p={pval:.4f})", fontsize=11, fontweight="bold")
        ax.set_xlabel("Byte Value (0-255)")
        ax.set_ylabel("Observed Count")
        ax.set_ylim(3700, 4500)
        ax.legend(loc="upper right")
        ax.grid(alpha=0.3)

    plt.suptitle("CryptoLabX Assignment 9: OS Random Number Generation Byte Distributions", fontsize=14, fontweight="bold")
    plt.tight_layout()
    os.makedirs("outputs", exist_ok=True)
    out_path = "outputs/os_rng_byte_distributions.png"
    plt.savefig(out_path, dpi=150)
    print(f"Successfully generated {out_path}")

if __name__ == "__main__":
    main()
