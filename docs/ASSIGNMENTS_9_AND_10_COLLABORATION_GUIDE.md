# CryptoLabX — Assignments 9 & 10 Collaboration & Architecture Blueprint

**Assignment 9**: Operating System Random Number Generation & Statistical Evaluation  
**Assignment 10**: MT19937 Stream Cipher Cryptanalysis & Predictable Password Reset Token Attack  
**Group Number**: 17  
**Team Members**:
- **Member 1 (Mukund Rakholiya - 2024UCP1163)**
- **Member 2 (Lakshay Ahuja - 2024UCP1157)**

---

## 📌 Executive Summary & Key Directives

| Aspect | Assignment 9 Details | Assignment 10 Details |
| :--- | :--- | :--- |
| **Topic** | OS Random Number Generation (Linux `/dev/urandom`, OpenSSL `rand`, Windows CNG API) & Statistical cryptanalysis | MT19937 Stream Cipher (Part A: 16-bit Seed Brute-Force) & Predictable Reset Token Attack (Part B: Timestamp seeding) |
| **Language** | Python 3 (ctypes for Windows `bcrypt.dll`, subprocess for WSL/Linux and OpenSSL, `scipy`, `numpy`, `matplotlib`, `nbformat`) | Python 3 (standard Mersenne Twister engine, XOR keystream generator, brute-force cracking engines) |
| **Key Constraints** | Generate $\ge 1$ MB true random data per source; evaluate distributions, autocorrelation, patterns; compare Linux vs Windows CSPRNG mechanisms | Symmetric XOR cipher; 14-char "A" sequence location unknown in ciphertext; brute-force all 65,536 seeds; timestamp window $[T-300, T+300]$ |
| **Work Distribution** | **50% Mukund Rakholiya / 50% Lakshay Ahuja** | **50% Mukund Rakholiya (Part A) / 50% Lakshay Ahuja (Part B)** |
| **Collaboration Goal** | Seamless parallel development with **0 merge conflicts** and clear architectural boundaries | Strict separation of Part A (Stream Cipher) and Part B (Token Prediction) with shared notebook |

---

## 1. Zero-Merge-Conflict Git Strategy

To maintain repository hygiene and allow both team members to develop simultaneously without merge friction:

### Golden Rules
1. **File-Level Isolation**:
   - **Mukund**:
     - `analysis/os_rng/generator.py` (Multi-platform OS RNG generator: Windows CNG, OpenSSL, Linux WSL)
     - `analysis/os_rng/metrics.py` (Byte frequency, bit distribution, serial correlation, repeated patterns)
     - `modern/mt19937_cipher.py` (MT19937 stream cipher, 16-bit seed encryption & brute-force recovery)
     - `tests/test_os_rng.py` (Unit tests for OS RNG generator and statistical metrics)
     - `tests/test_mt19937_cipher.py` (Unit tests for MT19937 stream cipher and seed recovery)
     - `notebooks/assignment_9_os_rng_evaluation.ipynb` (Assignment 9 interactive analysis notebook)
     - `notebooks/assignment_10_mt19937_cryptanalysis.ipynb` (Assignment 10 interactive cryptanalysis notebook)
   - **Lakshay**:
     - `analysis/os_rng/statistical_tests.py` (NIST SP 800-22 tests: Runs test, Longest Run of Ones, DFT Spectral, Approx Entropy)
     - `analysis/os_rng/cli.py` (CLI runner and comparative reporting tables)
     - `attacks/reset_token_attack.py` (Timestamp-seeded token generator, window attacker, recovery verifier)
     - `tests/test_os_rng_advanced.py` (Unit tests for advanced statistical tests)
     - `tests/test_reset_token_attack.py` (Unit tests for reset token attack)
2. **Shared Package Contracts**:
   - `analysis/os_rng/__init__.py` and `attacks/__init__.py` cleanly re-export all modules.
3. **Dedicated Feature Branches**:
   - Mukund: `feat/lab9-10-core-mukund`
   - Lakshay: `feat/lab9-10-advanced-lakshay`

```
       [main] ────────────────────────────────────────────────────────┬───────────────┬───> [main updated]
          │                                                           │               │
          ├──> [feat/lab9-10-core-mukund] ────────────────────────────┘ (PR 1 merged) │
          │                                                                           │
          └──> [feat/lab9-10-advanced-lakshay] ───────────────────── (rebase main) ───┘ (PR 2 merged cleanly)
```

---

## 2. Work Breakdown Structure (50/50 Division)

### Assignment 9: OS Random Number Generation & Evaluation

| Task / Component | Mukund Rakholiya (Member 1) | Lakshay Ahuja (Member 2) |
| :--- | :--- | :--- |
| **Role & Responsibilities** | **Data Generation Engine & Low-Level Statistical Metrics** | **NIST SP 800-22 Tests, OS Architecture & Security Comparison** |
| **Primary Code Files** | `analysis/os_rng/generator.py`<br>`analysis/os_rng/metrics.py` | `analysis/os_rng/statistical_tests.py`<br>`analysis/os_rng/cli.py` |
| **Test File** | `tests/test_os_rng.py` | `tests/test_os_rng_advanced.py` |
| **Assigned Functions / Responsibilities** | 1. `generate_windows_cng_bytes(length: int) -> bytes`<br>2. `generate_openssl_rand_bytes(length: int) -> bytes`<br>3. `generate_linux_urandom_bytes(length: int) -> bytes`<br>4. Multi-platform generation runner creating $\ge 1$ MB datasets (`datasets/rng/`)<br>5. `byte_frequency_distribution(data: bytes) -> ByteFreqResult` (counts, $\chi^2$ test, p-value)<br>6. `bit_distribution(data: bytes) -> BitDistResult` (0s vs 1s, proportion, z-score)<br>7. `serial_correlation(data: bytes, lag: int = 1) -> float`<br>8. `repeated_patterns_analysis(data: bytes) -> PatternResult` (runs, n-grams, max run length) | 1. `runs_test(data: bytes) -> TestResult` (total runs, p-value via erfc)<br>2. `longest_run_ones_test(data: bytes) -> TestResult`<br>3. `discrete_fourier_transform_test(data: bytes) -> TestResult`<br>4. `approximate_entropy_test(data: bytes, m: int = 2) -> TestResult`<br>5. `shannon_entropy(data: bytes) -> float`<br>6. CLI benchmarking runner and summary table generator |
| **Theoretical Tasks** | **Task 4 (Linux)**: In-depth architectural investigation of Linux CSPRNG (`/dev/urandom`, ChaCha20 CRNG since Linux 4.8 / 5.17+, entropy pools, input harvesting, non-blocking semantics, forward secrecy via state erasure). | **Task 4 (Windows) & Task 5**: In-depth investigation of Windows CNG (`BCryptGenRandom`, `cng.sys`, dual-state accumulator, AES-CTR DRBG SP 800-90A) and comprehensive treatise on *Why Passing Statistical Tests Does Not Guarantee Cryptographic Security*. |
| **Deliverables** | Multi-platform binary datasets ($\ge 1$ MB), core statistical engine, Linux CSPRNG report, unit tests, notebook metrics visualization. | NIST statistical test suite, Windows CNG report, security comparison matrix, CLI benchmark tool. |

---

### Assignment 10: MT19937 Stream Cipher & Predictable Token Attack

| Task / Component | Mukund Rakholiya (Member 1) | Lakshay Ahuja (Member 2) |
| :--- | :--- | :--- |
| **Role & Responsibilities** | **Part A: MT19937 Stream Cipher & 16-Bit Seed Brute-Force Recovery** | **Part B: Predictable Password Reset Tokens & Timestamp Window Attack** |
| **Primary Code Files** | `modern/mt19937_cipher.py` | `attacks/reset_token_attack.py` |
| **Test File** | `tests/test_mt19937_cipher.py` | `tests/test_reset_token_attack.py` |
| **Assigned Functions / Responsibilities** | 1. `MT19937StreamCipher`: 32-bit Mersenne Twister engine, 8-bit keystream extraction, symmetric XOR encryption/decryption.<br>2. Round-trip verification helper: `verify_cipher_roundtrip()`.<br>3. `generate_plaintext(prefix_len: int = None) -> bytes`: Random printable prefix (5-20 chars) + 14 'A' characters (`AAAAAAAAAAAAAA`).<br>4. `encrypt_with_16bit_seed(plaintext: bytes, seed: int = None) -> tuple[bytes, int]`.<br>5. `brute_force_16bit_seed(ciphertext: bytes, known_sequence: bytes = b"AAAAAAAAAAAAAA") -> tuple[int, bytes, float, int]`: tests all 65,536 seeds.<br>6. `verify_recovered_result(ciphertext: bytes, original_seed: int, recovered_seed: int, original_pt: bytes, recovered_pt: bytes) -> bool`. | 1. `generate_reset_token(timestamp: int = None) -> tuple[int, str, bytes]`: MT19937 seeded with integer Unix timestamp $T$, 16 consecutive 8-bit outputs as 16-byte hex token.<br>2. `predict_reset_token(observed_token_hex: str, approx_timestamp: int, window_seconds: int = 300) -> tuple[int, int, float]`: tests $[T - 300, T + 300]$.<br>3. `verify_token_match(timestamp: int, observed_token_hex: str) -> bool`.<br>4. CLI demonstration and profiling runner for token prediction. |
| **Theoretical Tasks** | **Tasks 12 & 13**: MT19937 algorithm, linear recurrence on GF(2), tempering matrix, state invertibility, why it is not cryptographically secure, known-plaintext keystream revelation ($K_i = C_i \oplus P_i$), 16-bit seed space calculation ($2^{16} = 65,536$).<br>**Task 15 (Part A)**: Pseudocode for 16-bit seed recovery. | **Task 14 & 15 (Part B)**: Why timestamp-based seeding is vulnerable (low entropy, coarse 1-second resolution, NTP/HTTP header synchronization), attack window complexity, pseudocode for token prediction, industrial mitigations (CSPRNG, salts, HMAC). |
| **Demonstration Deliverables** | **Tasks 16 & 17**: Source code, encryption/decryption proof, plaintext/ciphertext, brute-force speed, recovered seed and verified full plaintext. | **Tasks 18 & 19**: Token output, timestamp $T$, search window $[T-300, T+300]$, candidates tested, recovered timestamp, token verification. |

---

## 3. Architecture & Interface Specifications

### Directory Layout
```
CryptoLabX_Group17/
├── analysis/
│   └── os_rng/
│       ├── __init__.py               # [Shared] Package exports
│       ├── generator.py              # [Mukund] Windows CNG, OpenSSL & Linux urandom generators
│       ├── metrics.py                # [Mukund] Byte freq, bit distribution, serial correlation, patterns
│       ├── statistical_tests.py      # [Lakshay] NIST SP 800-22 advanced tests (runs, DFT, approx entropy)
│       └── cli.py                    # [Lakshay] CLI analysis runner & comparative table
├── attacks/
│   ├── __init__.py                   # Package exports
│   └── reset_token_attack.py         # [Lakshay] Timestamp-seeded reset token attack
├── datasets/
│   └── rng/
│       ├── linux_urandom_1mb.bin     # [Mukund] 1MB generated from Linux /dev/urandom
│       ├── openssl_rand_1mb.bin      # [Mukund] 1MB generated from OpenSSL rand
│       ├── windows_cng_1mb.bin       # [Mukund] 1MB generated from Windows CNG API
│       └── mt19937_prng_1mb.bin      # [Mukund] 1MB PRNG baseline for comparison
├── docs/
│   ├── ASSIGNMENTS_9_AND_10_COLLABORATION_GUIDE.md  # [Shared] Collaboration Blueprint
│   ├── LAB_MANUAL_ASSIGNMENT_9.md                   # [Shared Notebook] Lab Manual for Assignment 9
│   └── LAB_MANUAL_ASSIGNMENT_10.md                  # [Shared Notebook] Lab Manual for Assignment 10
├── modern/
│   ├── __init__.py                   # Package exports
│   └── mt19937_cipher.py             # [Mukund] MT19937 stream cipher & 16-bit seed brute-force
├── notebooks/
│   ├── assignment_9_os_rng_evaluation.ipynb          # [Mukund & Lakshay] OS RNG analysis & visualizations
│   └── assignment_10_mt19937_cryptanalysis.ipynb     # [Mukund & Lakshay] Stream cipher & reset token attack
└── tests/
    ├── test_os_rng.py                # [Mukund] OS RNG generation & metrics tests
    ├── test_os_rng_advanced.py       # [Lakshay] Advanced statistical tests
    ├── test_mt19937_cipher.py        # [Mukund] MT19937 cipher & seed brute-force tests
    └── test_reset_token_attack.py    # [Lakshay] Password reset token attack tests
```

---

## 4. Module Interface Contracts (Mukund's Modules)

### `analysis/os_rng/generator.py`
```python
def generate_windows_cng_bytes(length: int = 1048576) -> bytes:
    """Generates cryptographically secure random bytes via Windows CNG (bcrypt.dll BCryptGenRandom)."""
    ...

def generate_openssl_rand_bytes(length: int = 1048576) -> bytes:
    """Generates cryptographically secure random bytes using OpenSSL CLI utility."""
    ...

def generate_linux_urandom_bytes(length: int = 1048576) -> bytes:
    """Generates cryptographically secure random bytes from Linux /dev/urandom (via WSL or direct read)."""
    ...

def generate_all_datasets(output_dir: str = "datasets/rng", size_bytes: int = 1048576) -> dict[str, str]:
    """Generates and writes >= 1 MB binary files for Linux, OpenSSL, Windows CNG, and MT19937 baseline."""
    ...
```

### `analysis/os_rng/metrics.py`
```python
@dataclass
class ByteFreqResult:
    counts: np.ndarray          # 256 byte frequencies
    expected: float             # Expected count per byte (N / 256)
    chi2_stat: float            # Chi-square goodness-of-fit statistic
    p_value: float              # Chi-square p-value (df = 255)
    is_uniform: bool            # True if p_value > 0.01

@dataclass
class BitDistResult:
    total_bits: int
    zero_count: int
    one_count: int
    one_proportion: float       # Count of 1s / total bits
    z_score: float              # Standard normal statistic

@dataclass
class PatternResult:
    max_identical_byte_run: int
    expected_max_run: float
    byte_run_counts: dict[int, int]
    duplicate_16bit_pairs: int

def byte_frequency_distribution(data: bytes) -> ByteFreqResult:
    """Analyzes distribution of all 256 byte values and performs chi-square goodness of fit."""
    ...

def bit_distribution(data: bytes) -> BitDistResult:
    """Evaluates 0 vs 1 bit distribution, proportions, and standard normal deviation."""
    ...

def serial_correlation(data: bytes, lag: int = 1) -> float:
    """Calculates Pearson serial correlation (autocorrelation) at given byte lag."""
    ...

def repeated_patterns_analysis(data: bytes) -> PatternResult:
    """Analyzes runs of identical consecutive bytes and repeated n-gram patterns."""
    ...
```

### `modern/mt19937_cipher.py`
```python
class MT19937:
    """Standard 32-bit Mersenne Twister PRNG."""
    def __init__(self, seed: int = 5489): ...
    def extract_number(self) -> int: ...

class MT19937StreamCipher:
    """Toy stream cipher using MT19937 8-bit keystream XORed with input."""
    def __init__(self, seed: int): ...
    def keystream_byte(self) -> int: ...
    def encrypt(self, plaintext: bytes) -> bytes: ...
    def decrypt(self, ciphertext: bytes) -> bytes: ...

def generate_plaintext(prefix_len: int = None) -> bytes:
    """Generates plaintext with 5-20 random printable characters followed by 14 'A' characters."""
    ...

def encrypt_with_16bit_seed(plaintext: bytes, seed: int = None) -> tuple[bytes, int]:
    """Encrypts plaintext with a random or specified 16-bit seed (0..65535)."""
    ...

def brute_force_16bit_seed(ciphertext: bytes, known_sequence: bytes = b"AAAAAAAAAAAAAA") -> tuple[int, bytes, float, int]:
    """
    Brute-forces all 65,536 seeds (0..65535) to find the matching seed
    that produces known_sequence in decrypted plaintext.
    Returns (recovered_seed, recovered_plaintext, elapsed_seconds, seeds_tested).
    """
    ...

def verify_recovered_result(
    ciphertext: bytes,
    original_seed: int,
    recovered_seed: int,
    original_pt: bytes,
    recovered_pt: bytes,
    known_sequence: bytes = b"AAAAAAAAAAAAAA"
) -> bool:
    """Verifies complete round-trip match, seed recovery, and presence of known sequence."""
    ...
```

---

## 5. Verification & Test Strategy

- **Assignment 9 Tests**:
  - Test OS generators produce expected exact byte counts ($\ge 1$ MB).
  - Test Windows CNG API ctypes integration functions correctly without errors.
  - Test OpenSSL subprocess wrapper succeeds and generates non-zero random output.
  - Test Linux `/dev/urandom` reader handles WSL and native platforms gracefully.
  - Test statistical metric calculations against known synthetic datasets (all zeros, alternating bytes, uniform distributions).
  - Verify $\chi^2$ p-value computation, bit proportions, serial correlations, and pattern run lengths.

- **Assignment 10 Tests**:
  - Test `MT19937StreamCipher` symmetry: `cipher.decrypt(cipher.encrypt(data)) == data` for short and long messages.
  - Test plaintext generator enforces 5-20 printable prefix and exact 14 'A' characters (`AAAAAAAAAAAAAA`).
  - Test 16-bit seed encryption bounds: $0 \le \text{seed} \le 65535$.
  - Test brute-force recovery: recovers the exact seed and original plaintext across multiple randomized runs in $< 2$ seconds.
  - Test handling of ciphertexts with arbitrary prefix lengths.
