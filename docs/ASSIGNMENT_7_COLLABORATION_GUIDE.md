# CryptoLabX — Assignment 7 Collaboration & Architecture Blueprint

**Assignment**: Padding Oracle Attack on AES-CBC  
**Group Number**: 17  
**Team Members**:
- **Member 1 (Mukund Rakholiya - 2024UCP1163)**
- **Member 2 (Lakshay Ahuja - 2024UCP1157)**

---

## 📌 Executive Summary & Key Directives

| Aspect | Assignment 7 Details |
| :--- | :--- |
| **Topic** | Cryptanalysis of AES-CBC via Padding Oracle Side-Channel Attack |
| **Language** | Python 3 (standard `pycryptodome` or `cryptography` permitted for target cipher setup; attack itself written from scratch) |
| **Key Constraint** | The AES key must **never** be used or accessed during the attack. No ready-made padding-oracle libraries allowed. |
| **Work Distribution** | **50% Mukund Rakholiya / 50% Lakshay Ahuja** |
| **Collaboration Goal** | Seamless parallel development on separate workstations with **0 merge conflicts** |

---

## 1. Zero-Merge-Conflict Git Strategy

To maintain clean repository hygiene and allow both team members to develop simultaneously without merge friction:

### Golden Rules
1. **File-Level Isolation**: Mukund and Lakshay work in separate source files.
   - Mukund: `oracle.py`, `byte_decryptor.py`, `tests/test_oracle_and_byte.py`
   - Lakshay: `block_attack.py`, `run_attack.py`, `tests/test_block_attack.py`
2. **Strict Interface Contracts**: Clear type signatures for inputs, intermediate state bytes, and query counters.
3. **Dedicated Feature Branches**:
   - Mukund: `feat/lab7-oracle-byte-mukund`
   - Lakshay: `feat/lab7-block-orchestrator-lakshay`

```
       [main] ───────────────────────────────────────────┬───────────────┬───> [main updated]
          │                                              │               │
          ├──> [feat/lab7-oracle-byte-mukund] ───────────┘ (PR 1 merged) │
          │                                                              │
          └──> [feat/lab7-block-orchestrator-lakshay] ── (rebase main) ──┘ (PR 2 merged cleanly)
```

---

## 2. Work Breakdown Structure (50/50 Division)

| Parameter | Mukund Rakholiya (Member 1) | Lakshay Ahuja (Member 2) |
| :--- | :--- | :--- |
| **Module / Role** | **Oracle Simulation & Single-Byte Decryption Engine** | **Multi-Block Orchestrator & Attack Analytics** |
| **Primary Code Files** | `attacks/padding_oracle_attack/oracle.py`<br>`attacks/padding_oracle_attack/byte_decryptor.py` | `attacks/padding_oracle_attack/block_attack.py`<br>`attacks/padding_oracle_attack/run_attack.py` |
| **Test File** | `tests/test_oracle_and_byte.py` | `tests/test_block_attack.py` |
| **Assigned Functions / Responsibilities** | 1. `pad_pkcs7(data: bytes, block_size: int) -> bytes`<br>2. `unpad_pkcs7(data: bytes, block_size: int) -> bytes`<br>3. `PaddingOracle` class (AES-CBC encrypt, padding oracle validator, query counter)<br>4. `recover_byte(oracle, prev_block, target_block, byte_index, known_intermediates) -> tuple[int, int]` | 1. `split_blocks(ciphertext: bytes, block_size: int) -> list[bytes]`<br>2. `recover_block(oracle, prev_block, target_block) -> bytes`<br>3. `padding_oracle_decrypt(oracle, iv: bytes, ciphertext: bytes) -> bytes`<br>4. Attack CLI runner with query stats, execution profiling, and formatted deliverables |
| **Theoretical Tasks** | **Task 1**: AES-CBC mode operation, PKCS#7 padding mechanics, padding oracle vulnerability mechanism.<br>**Task 3 (Part B)**: Mathematical proof of bit manipulation ($P_i = D_K(C_i) \oplus C_{i-1}$) and why modifying $C_{i-1}$ isolates individual plaintext bytes. | **Task 3 (Part A)**: Query complexity analysis (best, average $\sim 128$ queries/byte, worst case 256), theoretical vs recorded queries.<br>**Task 4**: Industrial security recommendations (AEAD, AES-GCM, Encrypt-then-MAC with constant-time verification, mitigation of side channels). |
| **Deliverables Ownership** | Core oracle engine, byte recovery module, single-byte unit tests, theory sections 1 & 3B. | Full multi-block pipeline, test suite, query benchmarking, security analysis sections 3A & 4. |

---

## 3. Architecture & Interface Specifications

### Directory Layout
```
CryptoLabX_Group17/
├── attacks/
│   └── padding_oracle_attack/
│       ├── __init__.py
│       ├── oracle.py              # [Mukund] AES-CBC environment & Oracle class
│       ├── byte_decryptor.py      # [Mukund] Single byte recovery & intermediate logic
│       ├── block_attack.py        # [Lakshay] Block iteration & full plaintext recovery
│       └── run_attack.py          # [Lakshay] Interactive CLI driver & reporter
├── docs/
│   ├── ASSIGNMENT_7_COLLABORATION_GUIDE.md
│   └── LAB_MANUAL_ASSIGNMENT_7.md
└── tests/
    ├── test_oracle_and_byte.py    # [Mukund] Oracle & byte-level tests
    └── test_block_attack.py       # [Lakshay] Multi-block integration tests
```

### Module Interface Contracts

#### 1. Mukund's Modules (`oracle.py` & `byte_decryptor.py`)

```python
class PaddingOracle:
    """Simulates a server with an unknown AES key that decrypts CBC ciphertext 
    and returns whether PKCS#7 padding is valid. Tracks query count."""
    def __init__(self, key: bytes = None, block_size: int = 16): ...
    def encrypt(self, plaintext: bytes) -> tuple[bytes, bytes]: 
        """Returns (iv, ciphertext) using secret key."""
        ...
    def is_padding_valid(self, iv: bytes, ciphertext: bytes) -> bool: 
        """Queries the oracle: returns True if decrypted plaintext has valid PKCS#7 padding."""
        ...
    @property
    def query_count(self) -> int: ...
    def reset_query_count(self) -> None: ...

def recover_byte(
    oracle: PaddingOracle,
    prev_block: bytes,
    target_block: bytes,
    byte_index: int,
    known_intermediate: dict[int, int]
) -> tuple[int, int]:
    """
    Recovers intermediate state byte I[byte_index] and plaintext byte P[byte_index].
    
    Args:
        oracle: PaddingOracle instance
        prev_block: 16-byte previous ciphertext block (or IV for block 0)
        target_block: 16-byte target ciphertext block being attacked
        byte_index: Target byte position (15 down to 0)
        known_intermediate: Dict mapping index -> intermediate byte value for indices > byte_index
        
    Returns:
        (intermediate_byte, plaintext_byte)
    """
    ...
```

#### 2. Lakshay's Modules (`block_attack.py` & `run_attack.py`)

```python
def split_blocks(data: bytes, block_size: int = 16) -> list[bytes]:
    """Splits raw byte stream into uniform block_size chunks."""
    ...

def recover_block(oracle: PaddingOracle, prev_block: bytes, target_block: bytes) -> bytes:
    """Recovers the full 16-byte plaintext block by iterating byte 15 down to 0 
    using recover_byte()."""
    ...

def padding_oracle_decrypt(oracle: PaddingOracle, iv: bytes, ciphertext: bytes) -> tuple[bytes, int]:
    """
    Recovers the complete plaintext message across all blocks and strips PKCS#7 padding.
    
    Returns:
        (unpadded_plaintext, total_queries_used)
    """
    ...
```

---

## 4. Deliverables Checklist & Task Alignment

- [x] **Completed Python Program**:
  - `oracle.py` + `byte_decryptor.py` (Mukund)
  - `block_attack.py` + `run_attack.py` (Lakshay)
- [x] **Recovered Plaintext**:
  - Validated by unit tests against arbitrary plaintexts and block counts.
- [x] **Number of Oracle Queries**:
  - Tracked in `PaddingOracle`, profiled per byte, per block, and total.
- [x] **Theoretical & Prevention Analysis**:
  - Detailed in lab manual and report covering AES-CBC, PKCS#7, bitwise differential analysis, and AEAD/Encrypt-then-MAC prevention.
