# CryptoLabX — Assignments 5 & 6 Collaboration & Architecture Blueprint

**Group Number**: 17  
**Team Members**:
- **Member 1 (User)**: Mukund Rakholiya (2024UCP1163)
- **Member 2 (Friend)**: Lakshay Ahuja (2024UCP1157)

---

## 📌 Executive Summary & Key Directives

| Aspect | Assignment 5 | Assignment 6 |
| :--- | :--- | :--- |
| **Topic** | Cryptanalysis of Vigenère Cipher using Kasiski Examination & Frequency Analysis | Monoalphabetic Substitution Cipher & Cryptanalysis using Frequency & Pattern Analysis |
| **Language Allowed** | Python 3 (Integrates directly into existing repo architecture) | **Except Python, any language can be used** → **Standard C++ (C++17)** |
| **Group 17 Inputs** | **Group 17 is ODD** $\rightarrow$ Assigned **Ciphertext 1 (Odd Group No.)** | Text from *Modern Cryptography* by Katz & Lindell, **Page ($17 + 30$) = Page 47** |
| **Work Distribution** | **50% Mukund / 50% Lakshay** | **50% Mukund / 50% Lakshay** |
| **Collaboration Goal** | Parallel development on separate machines with **0 merge conflicts** | Parallel development on separate machines with **0 merge conflicts** |

---

## 1. Zero-Merge-Conflict Git Strategy

To ensure you and your friend can develop concurrently on your own computers without ever causing merge conflicts:

### Golden Rules for Conflict Prevention
1. **File-Level Isolation**: Mukund and Lakshay **never** write to or edit the same file simultaneously. Every component is isolated into distinct files.
2. **Strict Interface Contracts**: Both members agree on function signatures and return types beforehand (specified in this document).
3. **Dedicated Feature Branches**: Never commit directly to `main`. Always work on a feature branch.
4. **Independent Test Files**: Mukund writes `test_kasiski.py` and `test_cipher_stats.cpp`; Lakshay writes `test_vigenere_freq.py` and `test_pattern_solver.cpp`.
5. **Separation of Logic and Shared Drivers**: The runner/driver (`main.py` / `main.cpp`) is scaffolded with stubs first.

### Git Branching Workflow

```
       [main] ───────────────────────────────────────────┬───────────────┬───> [main updated]
          │                                              │               │
          ├──> [feat/lab5-kasiski-mukund] ───────────────┘ (PR 1 merged) │
          │                                                              │
          └──> [feat/lab5-freq-lakshay] ──── (git rebase origin/main) ───┘ (PR 2 merged cleanly)
```

#### Step-by-Step Commands:
1. **Starting work**:
   ```bash
   git checkout main
   git pull origin main
   # Mukund creates his branch:
   git checkout -b feat/lab5-kasiski-mukund
   # Lakshay creates his branch on his PC:
   git checkout -b feat/lab5-freq-lakshay
   ```
2. **When Mukund finishes and merges first**:
   - Mukund commits and pushes:
     ```bash
     git add attacks/vigenere_attack/kasiski_engine.py tests/test_kasiski.py
     git commit -m "feat(vigenere): implement kasiski examination and IC analysis"
     git push origin feat/lab5-kasiski-mukund
     ```
   - Open Pull Request on GitHub and merge into `main`.
3. **When Lakshay is ready to merge**:
   - Lakshay updates his local `main` and rebases his feature branch:
     ```bash
     git checkout main
     git pull origin main
     git checkout feat/lab5-freq-lakshay
     git rebase main
     git push origin feat/lab5-freq-lakshay
     ```
   - Because Lakshay only touched `frequency_engine.py` and `test_vigenere_freq.py`, **git merges cleanly with 0 conflicts!**

---

## 2. Integrated Project Structure

Here is how Assignment 5 and Assignment 6 fit into your existing `CryptoLabX_Group17` repository:

```
CryptoLabX_Group17/
├── classical/
│   ├── __init__.py
│   ├── caesar.py
│   └── vigenere_cipher.py           # Reusable Vigenère cipher engine
├── attacks/
│   ├── shift_cipher_attack/         # Completed from Assignment 2 & 3
│   └── vigenere_attack/             # [ASSIGNMENT 5]
│       ├── __init__.py
│       ├── kasiski_engine.py        # [Mukund] Kasiski & IC estimation
│       ├── frequency_engine.py      # [Lakshay] Coset frequency analysis & key recovery
│       └── run_vigenere.py          # Unified CLI runner linking both modules
├── monoalphabetic_cipher/           # [ASSIGNMENT 6] (C++ Project - No Python)
│   ├── CMakeLists.txt               # Or simple g++ build script (build.bat / Makefile)
│   ├── include/
│   │   ├── cipher_and_stats.hpp     # [Mukund] Header for Cipher & Letter/Word Freq
│   │   └── pattern_solver.hpp       # [Lakshay] Header for Patterns & Iterative Solver
│   ├── src/
│   │   ├── cipher_and_stats.cpp     # [Mukund] Implementation
│   │   ├── pattern_solver.cpp       # [Lakshay] Implementation
│   │   └── main.cpp                 # Interactive CLI driver
│   ├── tests/
│   │   ├── test_cipher_stats.cpp    # [Mukund] Tests
│   │   └── test_pattern_solver.cpp  # [Lakshay] Tests
│   └── build/                       # Ignored compiled binaries
├── datasets/
│   ├── vigenere_ciphertext_group17.txt  # Assignment 5 Ciphertext 1
│   └── katz_lindell_p47.txt             # Assignment 6 Plaintext (Book p.47)
├── docs/
│   ├── ASSIGNMENTS_5_AND_6_COLLABORATION_GUIDE.md  # (This document)
│   └── cryptanalysis_decisions_table.md            # Assignment 6 Decision Log
├── tests/
│   ├── test_kasiski.py              # [Mukund]
│   └── test_vigenere_freq.py        # [Lakshay]
├── utils/
│   ├── file_analysis.py             # (Existing)
│   └── logger.py                    # (Existing logging system)
└── main.py                          # Updated root CLI to launch Lab 5 & 6
```

---

## 3. Assignment 5: Vigenère Cipher Cryptanalysis

### Problem Specification
- **Group 17 is ODD** $\rightarrow$ Use **Ciphertext 1 (Odd Group No.)**.
- **Ciphertext Text**:
  ```
  DAZFI SFSPA VQLSN PXYSZ WXALC DAFGQ UISMT PHZGA MKTTF TCCFX
  KFCRG GLPFE TZMMM ZOZDE ADWVZ WMWKV GQSOH QSVHP WFKLS LEASE
  PWHMJ EGKPU RVSXJ XVBWV POSDE TEQTX OBZIK WCXLW NUOVJ MJCLL
  OEOFA ZENVM JILOW ZEKAZ EJAQD ILSWW ESGUG KTZGQ ZVRMN WTQSE
  OTKTK PBSTA MQVER MJEGL JQRTL GFJYG SPTZP GTACM OECBX SESCI
  YGUFP KVILL TWDKS ZODFW FWEAA PQTFS TQIRG MPMEL RYELH QSVWB
  AWMOS DELHM UZGPG YEKZU KWTAM ZJMLS EVJQT GLAWV OVVXH KWQIL
  IEUYS ZWXAH HUSZO GMUZQ CIMVZ UVWIF JJHPW VXFSE TZEDF
  ```

### 50/50 Work Distribution Breakdown

| Parameter | Mukund Rakholiya (Member 1) | Lakshay Ahuja (Member 2) |
| :--- | :--- | :--- |
| **Component Name** | **Kasiski Key Length & Pattern Engine** | **Coset Frequency & Decryption Engine** |
| **Primary File** | `attacks/vigenere_attack/kasiski_engine.py` | `attacks/vigenere_attack/frequency_engine.py` |
| **Unit Test File** | `tests/test_kasiski.py` | `tests/test_vigenere_freq.py` |
| **Assigned Functions** | 1. `clean_ciphertext()`<br>2. `find_repeated_patterns()`<br>3. `calculate_distances()`<br>4. `find_factors()`<br>5. `kasiski_analysis()`<br>6. `calculate_ic()` | 1. `split_into_groups()`<br>2. `frequency_analysis()`<br>3. `find_shift()`<br>4. `find_key()`<br>5. `vigenere_decrypt()`<br>6. `vigenere_encrypt()`<br>7. `verify()` |
| **Weightage** | 6 functions (Statistical distance & IC) | 7 functions (Frequency, Caesar shift, verification) |
| **Deliverable** | Candidate key length(s) with IC score validation | Recovered key, decrypted plaintext & re-encryption validation |

### Precise Function Signatures & Interface Contract

#### Member 1 (Mukund) — `attacks/vigenere_attack/kasiski_engine.py`:
```python
def clean_ciphertext(raw_text: str) -> str:
    """Removes spaces, punctuation, numbers, and normalizes to uppercase A-Z."""
    ...

def find_repeated_patterns(text: str, min_len: int = 3, max_len: int = 5) -> dict[str, list[int]]:
    """Identifies repeated sequences of length min_len to max_len and their starting indices."""
    ...

def calculate_distances(pattern_positions: dict[str, list[int]]) -> dict[str, list[int]]:
    """Calculates distances between successive occurrences of each repeated pattern."""
    ...

def find_factors(number: int, max_factor: int = 16) -> list[int]:
    """Returns all factors of a given distance between 2 and max_factor."""
    ...

def kasiski_analysis(ciphertext: str, top_n: int = 5) -> list[tuple[int, int]]:
    """Combines pattern search, distances, and factor frequency to suggest candidate key lengths.
    Returns: List of tuples (candidate_key_length, factor_occurrence_count) sorted descending.
    """
    ...

def calculate_ic(text: str) -> float:
    """Calculates the Index of Coincidence (IC) for a given text string.
    Expected for random text ≈ 0.038, English text ≈ 0.065-0.068.
    """
    ...
```

#### Member 2 (Lakshay) — `attacks/vigenere_attack/frequency_engine.py`:
```python
# Reusable from attacks/shift_cipher_attack/src/chi_square_attack.py:
from attacks.shift_cipher_attack.src.chi_square_attack import ENGLISH_FREQ

def split_into_groups(ciphertext: str, key_length: int) -> list[str]:
    """Divides ciphertext into 'key_length' coset strings (interleaved columns)."""
    ...

def frequency_analysis(group_text: str) -> dict[str, float]:
    """Calculates observed A-Z letter frequency percentages for a single group."""
    ...

def find_shift(group_text: str) -> int:
    """Estimates the best Caesar shift (0-25) for a group using Chi-Square goodness-of-fit with ENGLISH_FREQ."""
    ...

def find_key(groups: list[str]) -> str:
    """Combines individual shifts from each group into the probable Vigenère key string."""
    ...

def vigenere_decrypt(ciphertext: str, key: str) -> str:
    """Decrypts ciphertext using the recovered repeating key: P[i] = (C[i] - K[i]) mod 26."""
    ...

def vigenere_encrypt(plaintext: str, key: str) -> str:
    """Re-encrypts plaintext using the key: C[i] = (P[i] + K[i]) mod 26."""
    ...

def verify(original_ciphertext: str, re_encrypted_text: str) -> bool:
    """Checks whether re-encryption produces the original cleaned ciphertext."""
    ...
```

#### Shared Driver (`attacks/vigenere_attack/run_vigenere.py`):
```python
"""Entry point for Assignment 5. Imports both engines cleanly without conflicts."""
from attacks.vigenere_attack.kasiski_engine import (
    clean_ciphertext, kasiski_analysis, calculate_ic
)
from attacks.vigenere_attack.frequency_engine import (
    split_into_groups, frequency_analysis, find_key,
    vigenere_decrypt, vigenere_encrypt, verify
)
```

---

## 4. Assignment 6: Monoalphabetic Substitution Cipher & Cryptanalysis

### Critical Constraints
1. **Language Constraint**: *"Except python any language can be used"* $\rightarrow$ **C++ (C++17)** selected. Fast, standard across all OS, no third-party libraries needed.
2. **Plaintext Selection**:
   - Source: *Modern Cryptography* by Katz & Lindell.
   - Page calculation: $\text{Page} = \text{Group\_number} + 30 = 17 + 30 = \mathbf{47}$.
   - Length: At least 1 full page of text.
   - Saved in: `datasets/katz_lindell_p47.txt`.
3. **Cryptanalysis Requirement**:
   - Iterative recovery without using black-box libraries.
   - Cryptanalytic decision log table filled in the notebook/report.

### 50/50 Work Distribution Breakdown

| Parameter | Mukund Rakholiya (Member 1) | Lakshay Ahuja (Member 2) |
| :--- | :--- | :--- |
| **Component Name** | **Cipher Engine & Statistical Analysis Module** | **Pattern Analysis & Interactive Solver Module** |
| **Header File** | `monoalphabetic_cipher/include/cipher_and_stats.hpp` | `monoalphabetic_cipher/include/pattern_solver.hpp` |
| **Source File** | `monoalphabetic_cipher/src/cipher_and_stats.cpp` | `monoalphabetic_cipher/src/pattern_solver.cpp` |
| **Test File** | `monoalphabetic_cipher/tests/test_cipher_stats.cpp` | `monoalphabetic_cipher/tests/test_pattern_solver.cpp` |
| **Assigned Functions** | 1. `generate_random_key()`<br>2. `mono_encrypt()`<br>3. `mono_decrypt()`<br>4. `frequency_analysis()`<br>5. `word_frequency_analysis()` (1, 2, and 3-letter words) | 1. `pattern_analysis()` (repeated words, double letters, word signatures)<br>2. `apply_substitution()`<br>3. `display_partial_plaintext()`<br>4. `verify_solution()`<br>5. Interactive CLI & Step-Table Logger |
| **Deliverables** | Encryption engine, letter frequency sorter, n-letter word extractor | Pattern matcher, candidate key mapping, partial display, verification |

### Precise C++ Interface Contract

#### Member 1 (Mukund) — `include/cipher_and_stats.hpp`:
```cpp
#pragma once
#include <string>
#include <vector>
#include <map>

struct LetterFrequency {
    char letter;
    int count;
    double percentage;
};

struct WordStats {
    std::map<std::string, int> one_letter_words;
    std::map<std::string, int> two_letter_words;
    std::map<std::string, int> three_letter_words;
    std::map<std::string, int> repeated_words;
};

// Functions implemented by Mukund:
std::string generate_random_key();
std::string mono_encrypt(const std::string& plaintext, const std::string& key);
std::string mono_decrypt(const std::string& ciphertext, const std::string& key);

std::vector<LetterFrequency> frequency_analysis(const std::string& ciphertext);
WordStats word_frequency_analysis(const std::string& ciphertext);
```

#### Member 2 (Lakshay) — `include/pattern_solver.hpp`:
```cpp
#pragma once
#include <string>
#include <vector>
#include <map>

struct CryptanalysisStep {
    int step_number;
    std::string observation;
    std::string possible_substitution;
    std::string substitution_tested;
    std::string result;
    std::string decision;
};

struct PatternStats {
    std::map<std::string, std::vector<std::string>> pattern_signatures; // e.g., "1232" -> "THAT"
    std::map<std::string, int> double_letter_patterns;                  // e.g., "EE", "LL"
};

// Functions implemented by Lakshay:
PatternStats pattern_analysis(const std::string& ciphertext);
std::string apply_substitution(const std::string& ciphertext, const std::map<char, char>& cipher_to_plain_map);
void display_partial_plaintext(const std::string& ciphertext, const std::map<char, char>& cipher_to_plain_map);
bool verify_solution(const std::string& original_plaintext, const std::string& recovered_key, const std::string& ciphertext);
```

---

## 5. Lab 6 Notebook Decision Table Template

The assignment requires documenting and justifying cryptanalytic decisions. This table should be included in your lab report/notebook:

| Step | Observation | Possible Substitution | Substitution Tested | Result | Decision |
| :---: | :--- | :---: | :---: | :--- | :---: |
| **1** | Most frequent ciphertext letter is `Q` (12.8%) | `Q` $\rightarrow$ `e` | `Q` $\rightarrow$ `e` | Appears frequently, especially at ends of words | **Good Decision** (Accepted) |
| **2** | Single-letter words in ciphertext are `X` and `M` | `X, M` $\rightarrow$ `a, i` | `X` $\rightarrow$ `a` | Fits grammatical positions | **Good Decision** (Accepted) |
| **3** | Repeated 3-letter word `ZBQ` appears 14 times with ending `Q` (`e`) | `ZBQ` $\rightarrow$ `the` | `Z` $\rightarrow$ `t`, `B` $\rightarrow$ `h` | Forms common prefixes `th-` | **Good Decision** (Accepted) |
| **4** | Double letter `KK` appears in multiple words | `K` $\rightarrow$ `l` or `s` or `o` | `K` $\rightarrow$ `l` | Yields readable words like `all` | **Good Decision** (Accepted) |
| **5** | Two-letter word `ZT` with known `Z` (`t`) | `T` $\rightarrow$ `o` or `i` | `T` $\rightarrow$ `o` (`to`) | Matches common English usage | **Good Decision** (Accepted) |
| **6** | Partial word `th-se` observed | Missing letter $\rightarrow$ `o` | Test substitution | Yields `those` | **Good Decision** (Accepted) |
| **7** | Full key recovered | Complete 26-char mapping | Re-encrypt | Ciphertext matches perfectly | **Key Validated** |

---

## 6. How Existing Work from Labs 1–4 is Reused

1. **`attacks/shift_cipher_attack/src/chi_square_attack.py`**:
   - The statistical frequency distribution `ENGLISH_FREQ` and the Chi-Square statistic formula $\chi^2 = \sum \frac{(O_i - E_i)^2}{E_i}$ are directly reused in `find_shift()` for Assignment 5.
2. **`utils/logger.py`**:
   - Used by the Assignment 5 runner to log every cryptanalysis step, estimated key lengths, and verification status to `outputs/execution.log`.
3. **`datasets/`**:
   - Houses the new Group 17 ciphertext (`datasets/vigenere_ciphertext_group17.txt`) and Katz & Lindell Page 47 plaintext (`datasets/katz_lindell_p47.txt`).
4. **`main.py` Root Menu**:
   - Option 3 ("Attack") is enhanced to route into:
     - Shift Cipher Cryptanalysis (Lab 2/3)
     - Vigenère Cryptanalysis (Lab 5)
     - Monoalphabetic Cryptanalysis Runner (Lab 6)

---

## 7. Execution and Verification Commands

### Assignment 5 (Python):
```bash
# Run Mukund's unit tests:
python -m unittest tests/test_kasiski.py

# Run Lakshay's unit tests:
python -m unittest tests/test_vigenere_freq.py

# Run full Vigenère cryptanalysis for Group 17:
python attacks/vigenere_attack/run_vigenere.py
```

### Assignment 6 (C++):
```bash
cd monoalphabetic_cipher

# Compile with g++ (standard C++17):
g++ -std=c++17 -Iinclude src/cipher_and_stats.cpp src/pattern_solver.cpp src/main.cpp -o mono_cryptanalysis

# Run interactive cryptanalysis:
./mono_cryptanalysis
```

---

## 8. Summary Checklist for Group 17

- [ ] Mukund creates branch `feat/lab5-kasiski-mukund` and implements Kasiski & IC functions.
- [ ] Lakshay creates branch `feat/lab5-freq-lakshay` and implements Coset Frequency, Caesar shift, and decryption.
- [ ] Mukund prepares `datasets/vigenere_ciphertext_group17.txt` (Odd group ciphertext) and `datasets/katz_lindell_p47.txt` (Page 47).
- [ ] Mukund implements C++ cipher and frequency analysis in `src/cipher_and_stats.cpp`.
- [ ] Lakshay implements C++ pattern solver and substitution display in `src/pattern_solver.cpp`.
- [ ] Both merge their feature branches sequentially into `main` via GitHub Pull Requests.
- [ ] Fill out the cryptanalytic decisions table in the final lab submission notebook.
