# CryptoLabX — Assignment 8 Collaboration & Architecture Blueprint

**Assignment**: Cryptographic Prime Generation Using Miller–Rabin  
**Group Number**: 17  
**Team Members**:
- **Member 1 (Mukund Rakholiya - 2024UCP1163)**
- **Member 2 (Lakshay Ahuja - 2024UCP1157)**

---

## 📌 Executive Summary & Key Directives

| Aspect | Assignment 8 Details |
| :--- | :--- |
| **Topic** | Cryptographic 512-bit Probable Prime Generation via Miller–Rabin Primality Test |
| **Language** | Python 3 (Standard library `secrets` for CSPRNG; custom Miller–Rabin from scratch; `pycryptodome` for verification) |
| **Key Constraints** | Exact 512-bit candidate length ($2^{511} \le p < 2^{512}$), odd candidate enforcement, no built-in prime generation for core test, rigorous multi-round testing ($\ge 40$ rounds), independent cross-verification |
| **Work Distribution** | **50% Mukund Rakholiya / 50% Lakshay Ahuja** |
| **Collaboration Goal** | Seamless parallel development with **0 merge conflicts** and clear architectural boundaries |

---

## 1. Zero-Merge-Conflict Git Strategy

To maintain repository hygiene and allow both team members to develop simultaneously without merge friction:

### Golden Rules
1. **File-Level Isolation**:
   - **Mukund**: `prime_generation/candidate_generator.py`, `prime_generation/miller_rabin.py`, `tests/test_miller_rabin.py`
   - **Lakshay**: `prime_generation/pipeline.py`, `prime_generation/verifier.py`, `prime_generation/cli.py`, `tests/test_prime_pipeline.py`
2. **Shared Package Exports**:
   - `prime_generation/__init__.py` acts as the unified contract exposing both members' modules cleanly.
3. **Dedicated Feature Branches**:
   - Mukund: `feat/lab8-candidate-miller-rabin-mukund`
   - Lakshay: `feat/lab8-pipeline-verifier-lakshay`

```
       [main] ───────────────────────────────────────────────────┬───────────────┬───> [main updated]
          │                                                      │               │
          ├──> [feat/lab8-candidate-miller-rabin-mukund] ────────┘ (PR 1 merged) │
          │                                                                      │
          └──> [feat/lab8-pipeline-verifier-lakshay] ────────── (rebase main) ───┘ (PR 2 merged cleanly)
```

---

## 2. Work Breakdown Structure (50/50 Division)

| Parameter | Mukund Rakholiya (Member 1) | Lakshay Ahuja (Member 2) |
| :--- | :--- | :--- |
| **Module / Role** | **Candidate Generation & Core Miller–Rabin Engine** | **Generation Pipeline, Independent Verifier & CLI Analytics** |
| **Primary Code Files** | `prime_generation/candidate_generator.py`<br>`prime_generation/miller_rabin.py` | `prime_generation/pipeline.py`<br>`prime_generation/verifier.py`<br>`prime_generation/cli.py` |
| **Test File** | `tests/test_miller_rabin.py` | `tests/test_prime_pipeline.py` |
| **Assigned Functions / Responsibilities** | 1. `generate_candidate(bit_length: int = 512) -> int`<br>2. `get_small_primes(limit: int = 1000) -> list[int]`<br>3. `sieve_of_small_primes(candidate: int, small_primes: list[int] = None) -> bool`<br>4. `verify_bit_length(n: int, expected_bit_length: int = 512) -> bool`<br>5. `decompose(n: int) -> tuple[int, int]` ($n-1 = 2^s \cdot d$)<br>6. `miller_rabin_test(n: int, a: int) -> bool` (single witness test)<br>7. `is_probable_prime(n: int, rounds: int = 40, bases: list[int] = None) -> tuple[bool, int]` | 1. `generate_512bit_prime(bit_length: int = 512, rounds: int = 40, use_sieve: bool = True) -> PrimeGenerationResult`<br>2. `verify_prime_candidate(candidate: int, expected_bit_length: int, bases: list[int]) -> VerificationResult`<br>3. `benchmark_generation(iterations: int = 5, bit_lengths: list[int] = [128, 256, 512]) -> dict`<br>4. Interactive CLI and formatted execution report generator |
| **Theoretical Tasks** | 1. Prime Number Theorem and candidate density ($\pi(x) \approx x / \ln x$).<br>2. Mathematical derivation of Miller–Rabin (Fermat's Little Theorem & non-trivial square roots of unity).<br>3. Error bound analysis ($P(\text{composite passes } k \text{ rounds}) \le 4^{-k}$). | 1. Empirical performance profiling (number of candidates tested, sieve efficiency, execution time vs bit length).<br>2. Independent verification mechanics using Baillie–PSW / `Crypto.Util.number.isPrime`.<br>3. Cryptographic deployment analysis (RSA key generation, safe primes $p = 2q+1$, side-channel considerations). |
| **Deliverables Ownership** | Cryptographically secure random candidate engine, pre-screening sieve, modular exponentiation & witness tester, comprehensive unit tests. | Multi-candidate loop orchestrator, execution metrics tracker, independent library verification, CLI reporting table. |

---

## 3. Architecture & Interface Specifications

### Directory Layout
```
CryptoLabX_Group17/
├── docs/
│   ├── ASSIGNMENT_8_COLLABORATION_GUIDE.md  # [Shared] Collaboration Blueprint
│   └── LAB_MANUAL_ASSIGNMENT_8.md          # [Shared] Laboratory Manual & Mathematical Theory
├── prime_generation/
│   ├── __init__.py                         # Package exports
│   ├── candidate_generator.py              # [Mukund] CSPRNG odd candidate generation & sieve
│   ├── miller_rabin.py                     # [Mukund] Core Miller-Rabin test engine
│   ├── pipeline.py                         # [Lakshay] Generation loop & metrics collector
│   ├── verifier.py                         # [Lakshay] Cross-verification (bit-length & library)
│   └── cli.py                              # [Lakshay] CLI table formatter & runner
└── tests/
    ├── test_miller_rabin.py                # [Mukund] Generator & Miller-Rabin unit tests
    └── test_prime_pipeline.py              # [Lakshay] Pipeline & verifier integration tests
```

### Module Interface Contracts

#### 1. Mukund's Modules (`candidate_generator.py` & `miller_rabin.py`)

```python
def generate_candidate(bit_length: int = 512) -> int:
    """
    Generates a cryptographically secure random odd integer of exact bit_length.
    Ensures bit_length - 1 and bit 0 are set to 1.
    """
    ...

def sieve_of_small_primes(candidate: int, small_primes: list[int] = None) -> bool:
    """
    Trial division pre-filter against small primes (< 1000).
    Returns False if candidate is composite (divisible by a small prime), True if it passes.
    """
    ...

def verify_bit_length(n: int, expected_bit_length: int = 512) -> bool:
    """Returns True if n.bit_length() == expected_bit_length."""
    ...

def decompose(n: int) -> tuple[int, int]:
    """
    Decomposes n - 1 into 2^s * d, where d is odd.
    Returns (s, d).
    """
    ...

def miller_rabin_test(n: int, a: int) -> bool:
    """
    Single-base Miller-Rabin primality test for base a in [2, n - 2].
    Returns True if n is probably prime to base a; False if n is composite.
    """
    ...

def is_probable_prime(
    n: int, 
    rounds: int = 40, 
    bases: list[int] = None
) -> tuple[bool, int]:
    """
    Multi-round Miller-Rabin primality test.
    If bases is provided, tests each base in bases.
    Otherwise, picks `rounds` cryptographically secure random bases.
    Returns (is_probable_prime, rounds_passed).
    """
    ...
```

#### 2. Lakshay's Modules (`pipeline.py`, `verifier.py`, & `cli.py`)

```python
@dataclass
class PrimeGenerationResult:
    candidate: int
    bit_length: int
    assigned_bit_length: int
    candidates_tested: int
    rounds_performed: int
    execution_time_seconds: float
    passed_sieve_count: int

def generate_512bit_prime(
    bit_length: int = 512,
    rounds: int = 40,
    use_sieve: bool = True
) -> PrimeGenerationResult:
    """
    Orchestrates the generation loop:
    Generates odd candidate -> Small prime sieve -> Miller-Rabin test.
    Repeats until a probable prime is found.
    """
    ...

@dataclass
class VerificationResult:
    bit_length_valid: bool
    actual_bit_length: int
    passes_specified_bases: bool
    specified_bases_tested: list[int]
    independent_library_result: bool
    library_name: str
    overall_verified: bool

def verify_prime_candidate(
    candidate: int,
    expected_bit_length: int = 512,
    bases: list[int] = None
) -> VerificationResult:
    """
    Verifies the candidate:
    1. Bit length == expected_bit_length
    2. Miller-Rabin for specified bases
    3. Independent library verification (pycryptodome isPrime)
    """
    ...
```

---

## 4. Deliverables Checklist & Task Alignment

- [x] **Candidate Generation Engine** (`candidate_generator.py` - Mukund)
- [x] **Miller–Rabin Test Core** (`miller_rabin.py` - Mukund)
- [x] **Unit & Edge Case Test Suite** (`test_miller_rabin.py` - Mukund)
- [ ] **Generation Pipeline Orchestrator** (`pipeline.py` - Lakshay)
- [ ] **Independent Verifier & Library Check** (`verifier.py` - Lakshay)
- [ ] **CLI Submission Table Runner** (`cli.py` - Lakshay)
- [ ] **Integration Test Suite** (`test_prime_pipeline.py` - Lakshay)
