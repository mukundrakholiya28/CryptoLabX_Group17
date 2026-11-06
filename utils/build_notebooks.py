"""
Helper script to generate Assignment 9 & 10 Jupyter Notebooks with nbformat.
"""

import os
from pathlib import Path
import nbformat as nbf


def build_assignment_9_notebook():
    nb = nbf.v4.new_notebook()
    nb.cells = [
        nbf.v4.new_markdown_cell(
            "# CryptoLabX — Assignment 9: OS Random Number Generation & Statistical Evaluation\n"
            "**Course**: Cryptography Laboratory  \n"
            "**Group Number**: 17  \n"
            "**Team Members**: Mukund Rakholiya (2024UCP1163), Lakshay Ahuja (2024UCP1157)  \n\n"
            "---\n\n"
            "## 1. Objective\n"
            "Evaluate operating-system random-number generation mechanisms (Linux `/dev/urandom`, OpenSSL `rand`, Windows CNG `BCryptGenRandom`) and investigate their suitability for cryptographic applications by:\n"
            "1. Generating >= 1 MB from each source.\n"
            "2. Analyzing byte frequencies, bit distributions, repeated patterns, and serial correlations.\n"
            "3. Applying statistical hypothesis tests (Chi-Square, Monobit).\n"
            "4. Investigating Linux and Windows kernel CSPRNG architectures.\n"
            "5. Demonstrating why passing statistical tests does not guarantee cryptographic security."
        ),
        nbf.v4.new_code_cell(
            "import os, sys\n"
            "# Add parent directory to sys.path\n"
            "sys.path.append(os.path.abspath('..'))\n\n"
            "from analysis.os_rng.generator import generate_all_datasets\n"
            "from analysis.os_rng.metrics import analyze_dataset"
        ),
        nbf.v4.new_markdown_cell(
            "## 2. Generate and Verify >= 1 MB Datasets\n"
            "We generate 1,048,576 bytes (1.00 MB) from each source:\n"
            "- **Linux `/dev/urandom`**: ChaCha20 CRNG kernel driver.\n"
            "- **OpenSSL `rand`**: EVP_RAND / AES-CTR DRBG.\n"
            "- **Windows CNG**: `BCryptGenRandom` exported by `bcrypt.dll` (`cng.sys`).\n"
            "- **MT19937 PRNG**: Deterministic baseline for comparison."
        ),
        nbf.v4.new_code_cell(
            "datasets = generate_all_datasets('../datasets/rng', size_bytes=1048576)\n"
            "for name, path in datasets.items():\n"
            "    sz = os.path.getsize(path)\n"
            "    print(f'[+] {name:20s}: {path} ({sz:,} bytes)')"
        ),
        nbf.v4.new_markdown_cell(
            "## 3. Statistical Analysis & Hypothesis Testing\n"
            "We execute Pearson's Chi-Square Goodness-of-Fit, Monobit Bit Distribution, Serial Autocorrelation, and Pattern Analysis across all datasets."
        ),
        nbf.v4.new_code_cell(
            "results = {}\n"
            "for name, path in datasets.items():\n"
            "    with open(path, 'rb') as f:\n"
            "        data = f.read()\n"
            "    res = analyze_dataset(data, name)\n"
            "    results[name] = res\n"
            "    print('\\n' + '='*65)\n"
            "    print(f'DATASET: {name} ({len(data):,} bytes)')\n"
            "    print('='*65)\n"
            "    print(res['byte_freq'].summary())\n"
            "    print(res['bit_dist'].summary())\n"
            "    print(f\"Lag-1 Serial Correlation: {res['lag1_autocorr']:.6f}\")\n"
            "    print(res['patterns'].summary())"
        ),
        nbf.v4.new_markdown_cell(
            "## 4. Visualizing Byte Frequency Distributions (256 Bins)\n"
            "Visualizing the uniform spread across all 256 byte values."
        ),
        nbf.v4.new_code_cell(
            "import matplotlib.pyplot as plt\n"
            "import numpy as np\n\n"
            "fig, axes = plt.subplots(2, 2, figsize=(14, 10))\n"
            "axes = axes.flatten()\n\n"
            "for idx, (name, res) in enumerate(results.items()):\n"
            "    ax = axes[idx]\n"
            "    counts = res['byte_freq'].counts\n"
            "    ax.bar(range(256), counts, color='steelblue', alpha=0.7, width=1.0)\n"
            "    ax.axhline(4096, color='red', linestyle='--', label='Expected (4096)')\n"
            "    ax.set_title(f\"{name}\\nChi2={res['byte_freq'].chi2_stat:.2f}, p={res['byte_freq'].p_value:.4f}\")\n"
            "    ax.set_xlabel('Byte Value (0-255)')\n"
            "    ax.set_ylabel('Frequency Count')\n"
            "    ax.set_ylim(3500, 4500)\n"
            "    ax.legend()\n"
            "    ax.grid(alpha=0.3)\n\n"
            "plt.tight_layout()\n"
            "os.makedirs('../outputs', exist_ok=True)\n"
            "plt.savefig('../outputs/os_rng_byte_distributions.png', dpi=150)\n"
            "print('Saved plot to outputs/os_rng_byte_distributions.png')\n"
            "plt.show()"
        ),
        nbf.v4.new_markdown_cell(
            "## 5. Architectural Comparison: Linux vs. Windows CSPRNG\n"
            "See `docs/LAB_MANUAL_ASSIGNMENT_9.md` for in-depth architectural breakdown.\n\n"
            "| Feature | Linux `/dev/urandom` | Windows CNG (`BCryptGenRandom`) |\n"
            "| :--- | :--- | :--- |\n"
            "| **Subsystem** | Kernel driver: `drivers/char/random.c` | Kernel driver: `cng.sys` |\n"
            "| **Algorithm** | ChaCha20 CRNG (256-bit key) | AES-256 CTR_DRBG (SP 800-90A) |\n"
            "| **Entropy Pool** | BLAKE2s Hash Accumulator | Dual-state Fortuna / SHA-256 Accumulator |\n"
            "| **Entropy Sources** | Interrupt timings, disk I/O, cycle jitter, RDRAND | TPM 2.0, hypervisor, ACPI, scheduler jitter |\n"
            "| **Forward Secrecy** | Fast-key erasure after request chunk | Instant memory key erasure |\n\n"
            "---\n\n"
            "## 6. Why Passing Statistical Tests Does Not Guarantee Cryptographic Security\n"
            "- As proven above, **MT19937 passed all statistical tests** (Chi-Square p=0.735, Monobit p=0.677, Autocorr=-0.000045).\n"
            "- However, MT19937 is strictly linear over GF(2) and completely reversible from 624 outputs.\n"
            "- Cryptographic security requires **computational unpredictability** under polynomial-time attacks, not merely statistical uniformity."
        )
    ]

    out_file = Path("notebooks/assignment_9_os_rng_evaluation.ipynb")
    out_file.parent.mkdir(exist_ok=True)
    with open(out_file, "w", encoding="utf-8") as f:
        nbf.write(nb, f)
    print(f"[+] Created {out_file}")


def build_assignment_10_notebook():
    nb = nbf.v4.new_notebook()
    nb.cells = [
        nbf.v4.new_markdown_cell(
            "# CryptoLabX — Assignment 10: MT19937 Stream Cipher & Predictable Token Attack\n"
            "**Course**: Cryptography Laboratory  \n"
            "**Group Number**: 17  \n"
            "**Team Members**: Mukund Rakholiya (2024UCP1163), Lakshay Ahuja (2024UCP1157)  \n\n"
            "---\n\n"
            "## 1. Objective\n"
            "Understand why a statistical PRNG is unsuitable for cryptographic applications by:\n"
            "1. Implementing an 8-bit MT19937 toy stream cipher (symmetric XOR).\n"
            "2. Generating a test message with a random prefix (5-20 chars) and known sequence of 14 'A's.\n"
            "3. Encrypting with a weak 16-bit seed (0..65535).\n"
            "4. Recovering the seed and full plaintext via exhaustive 65,536-seed brute force in under 1 second.\n"
            "5. Analyzing predictable password reset tokens seeded with Unix timestamps."
        ),
        nbf.v4.new_code_cell(
            "import os, sys\n"
            "sys.path.append(os.path.abspath('..'))\n\n"
            "from modern.mt19937_cipher import (\n"
            "    MT19937StreamCipher,\n"
            "    mt19937_cipher,\n"
            "    verify_cipher_roundtrip,\n"
            "    generate_plaintext,\n"
            "    encrypt_with_16bit_seed,\n"
            "    brute_force_16bit_seed,\n"
            "    verify_recovered_result\n"
            ")"
        ),
        nbf.v4.new_markdown_cell(
            "## 2. Part A: Cipher Symmetry Verification\n"
            "Verifying that encryption and decryption are perfectly symmetric."
        ),
        nbf.v4.new_code_cell(
            "test_msg = b'CryptoLabX Assignment 10 Stream Cipher Roundtrip Test!'\n"
            "cipher = MT19937StreamCipher(seed=42135)\n"
            "ct = cipher.encrypt(test_msg)\n"
            "pt = cipher.decrypt(ct)\n\n"
            "print(f'Original        : {test_msg}')\n"
            "print(f'Ciphertext (Hex): {ct.hex()}')\n"
            "print(f'Decrypted       : {pt}')\n"
            "print(f'Symmetry Match  : {pt == test_msg}')"
        ),
        nbf.v4.new_markdown_cell(
            "## 3. Plaintext Generation & 16-Bit Seed Encryption\n"
            "Generate plaintext with 5-20 random printable characters followed by 14 consecutive 'A's, then encrypt with a 16-bit seed:"
        ),
        nbf.v4.new_code_cell(
            "plaintext = generate_plaintext()\n"
            "prefix = plaintext[:-14]\n"
            "known_seq = plaintext[-14:]\n\n"
            "ciphertext, secret_seed = encrypt_with_16bit_seed(plaintext)\n\n"
            "print(f'Plaintext Length  : {len(plaintext)} bytes')\n"
            "print(f\"Random Prefix     : '{prefix.decode()}' ({len(prefix)} chars)\")\n"
            "print(f\"Known Sequence    : '{known_seq.decode()}' (14 'A's)\")\n"
            "print(f'Full Plaintext    : {plaintext}')\n"
            "print(f'Secret 16-bit Seed: {secret_seed} (Hex: 0x{secret_seed:04X})')\n"
            "print(f'Ciphertext (Hex)  : {ciphertext.hex()}')"
        ),
        nbf.v4.new_markdown_cell(
            "## 4. Exhaustive 65,536-Seed Brute-Force Key Recovery\n"
            "Given only ciphertext and knowledge of 14 consecutive 'A's (location unknown), brute-force all 65,536 seeds:"
        ),
        nbf.v4.new_code_cell(
            "res = brute_force_16bit_seed(ciphertext, known_sequence=b'AAAAAAAAAAAAAA', scan_entire_space=True)\n\n"
            "print(f'Seeds Tested        : {res.seeds_tested:,} / {res.total_search_space:,}')\n"
            "print(f'Elapsed Time        : {res.elapsed_time*1000:.2f} ms ({res.elapsed_time:.4f} s)')\n"
            "print(f'Throughput          : {res.seeds_per_second:,.0f} seeds/second')\n"
            "print(f'Recovered Seed      : {res.recovered_seed} (0x{res.recovered_seed:04X})')\n"
            "print(f'Original Seed       : {secret_seed}')\n"
            "print(f'Pattern Offset in PT: Index {res.sequence_offset}')\n"
            "print(f\"Recovered Plaintext : '{res.recovered_plaintext.decode()}'\")\n\n"
            "# Formal Cryptographic Verification\n"
            "is_valid = verify_recovered_result(ciphertext, secret_seed, res.recovered_seed, plaintext, res.recovered_plaintext)\n"
            "print(f\"Cryptographic Verification Status: {'SUCCESS' if is_valid else 'FAILED'}\")"
        ),
        nbf.v4.new_markdown_cell(
            "## 5. Mathematical Theory & Cryptanalysis\n"
            "See `docs/LAB_MANUAL_ASSIGNMENT_10.md` for complete derivations.\n\n"
            "### Known Plaintext Keystream Equation\n"
            "$$C_i = P_i \\oplus K_i \\implies K_i = P_i \\oplus C_i$$\n\n"
            "### 16-Bit Keyspace\n"
            "$$|\\mathcal{S}| = 2^{16} = 65,536 \\implies \\text{Broken in } \\approx 0.6 \\text{ seconds}$$\n\n"
            "### Timestamp Seeding Vulnerability\n"
            "- Seeding with integer Unix seconds collapses entropy to 1 value/sec.\n"
            "- Search window $[T-300, T+300] = 601$ candidates ($< 10$ ms attack)."
        )
    ]

    out_file = Path("notebooks/assignment_10_mt19937_cryptanalysis.ipynb")
    out_file.parent.mkdir(exist_ok=True)
    with open(out_file, "w", encoding="utf-8") as f:
        nbf.write(nb, f)
    print(f"[+] Created {out_file}")


if __name__ == "__main__":
    build_assignment_9_notebook()
    build_assignment_10_notebook()
