# CryptoLabX - Group 17

**A Professional Cryptography Laboratory Project**

## 📋 Project Overview

CryptoLabX is a comprehensive cryptography laboratory designed for educational purposes. This project provides a structured framework for exploring cryptographic algorithms, implementing attacks, and analyzing security measures.

The project follows a **modular design principle**, where each module has a specific responsibility, making it easy to extend and maintain throughout the semester.

---

## 👥 Team Members

- Group 17
  - Student 1
  - Student 2
  - Student 3
  - Student 4

---

## 📁 Project Structure

```
CryptoLabX/
├── classical/           # Classical cryptography algorithms
├── attacks/             # Cryptographic attack implementations
├── math/                # Mathematical utility functions
├── modern/              # Modern encryption algorithms (AES, RSA, etc.)
├── analysis/            # Statistical analysis tools
├── datasets/            # Text files for testing and analysis
├── outputs/             # Generated logs and results
├── docs/                # Documentation and references
├── tests/               # Unit and integration tests
├── utils/               # Helper functions and utilities
├── main.py              # Entry point of the program
├── README.md            # This file
└── requirements.txt     # Project dependencies
```

### Folder Descriptions

| Folder | Purpose |
|--------|---------|
| **classical/** | Caesar, Playfair, Hill, Rail Fence, Vigenère, Affine ciphers |
| **attacks/** | Frequency analysis, Brute force, Dictionary attacks |
| **math/** | GCD, Extended Euclid, Modulo, Prime testing, Matrix operations |
| **modern/** | DES, AES, RSA, ECC, SHA, Diffie-Hellman |
| **analysis/** | Letter frequency, Entropy, Chi-square test, N-gram analysis |
| **datasets/** | Sample text files for encryption and analysis |
| **outputs/** | Execution logs and analysis results |
| **tests/** | Automated testing for all modules |
| **utils/** | Reusable functions (logger, file analysis) |

---

## 🚀 Features (Week 1)

- ✅ **Menu-Driven CLI** - User-friendly command-line interface
- ✅ **File Analysis** - Character, word, line count and letter frequency analysis
- ✅ **Execution Logging** - Records all user actions with timestamps
- ✅ **Dataset Collection** - 5 sample text files for testing
- ✅ **Professional Structure** - Modular design for future expansion

### Future Features (Week 2 onwards)

- Classical cipher implementations (Caesar, Vigenère, Hill, etc.)
- Modern encryption algorithms (AES, RSA, ECC, etc.)
- Cryptographic attacks (Frequency analysis, Brute force, etc.)
- Statistical cryptanalysis tools
- Comprehensive test suite

---

## 📖 How to Run

### Prerequisites
- Python 3.7 or higher
- Git

### Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd CryptoLabX_Group17
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the program:
   ```bash
   python main.py
   ```

### Usage

Once the program starts, you'll see a menu:

```
========== CryptoLabX ==========
1. Encrypt
2. Decrypt
3. Attack
4. Analyze Dataset
5. Exit
================================
```

**Current Status**: Options 1-3 show "Coming Soon" placeholders. Option 4 analyzes text files from the `datasets/` folder.

**Example**: To analyze `book.txt`:
```
Select: 4
Enter filename from datasets folder: book.txt
```

---

## 📊 Sample Analysis Output

When analyzing a file, the program displays:
- Total characters
- Total words
- Total lines
- Unique characters
- Letter frequency distribution

Example:
```
========== File Analysis ==========
Characters       : 456
Words            : 78
Lines            : 5
Unique Characters: 42

Letter Frequency
a : 25
e : 32
i : 18
...
```

---

## 📝 Execution Log

Every action is recorded in `outputs/execution.log`:

```
2026-07-31 10:20:15 -> Analyze
2026-07-31 10:25:30 -> Encrypt
2026-07-31 10:30:45 -> Exit
```

---

## 📦 Dataset Files

The `datasets/` folder contains 5 sample text files:

1. **book.txt** - Excerpts from literature
2. **speech.txt** - Famous historical speech
3. **poem.txt** - Poetry excerpt
4. **news.txt** - News article
5. **random.txt** - Cryptography-related content

These files are used for:
- Testing encryption/decryption
- Frequency analysis
- Algorithm validation

---

## 🔧 Technologies Used

- **Python 3** - Programming language
- **Git** - Version control
- **Collections (Counter)** - For frequency analysis

---

## 📚 Learning Objectives

By completing this project, you will learn:

1. **Software Engineering** - Modular design and project organization
2. **Git & Version Control** - Tracking changes and collaboration
3. **File I/O** - Reading and processing text files
4. **Data Analysis** - Frequency analysis and statistics
5. **Logging & Debugging** - Recording program execution
6. **Professional Coding** - Clean code and documentation

---

## 🎯 Weekly Breakdown

| Week | Focus | Deliverables |
|------|-------|--------------|
| **Week 1** | Project infrastructure | Menu, logging, file analysis |
| **Week 2+** | Classical cryptography | Caesar, Vigenère, Hill implementations |
| **Week 3+** | Modern cryptography | RSA, AES, ECC implementations |
| **Week 4+** | Attacks & Analysis | Frequency analysis, brute force attacks |

---

## 📄 Git History

This project is version-controlled using Git. Initial commit:
```
git init
git add .
git commit -m "Initial Project Structure"
git push origin main
```

---

## ✅ Week 1 Deliverables

- [x] Git Repository Initialized
- [x] Folder Structure Created
- [x] Menu-Driven CLI Implemented
- [x] File Analysis Module
- [x] Logging System
- [x] Sample Datasets (5 files)
- [x] README Documentation

---

## 📞 Support & Documentation

- Check `docs/` for detailed documentation
- Review `outputs/execution.log` for program history
- See specific module files for implementation details

---

## 📜 License

Educational Project - Group 17

---

**Last Updated**: 2026-07-31
