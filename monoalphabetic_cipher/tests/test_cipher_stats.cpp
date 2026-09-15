#include "cipher_and_stats.hpp"

#include <algorithm>
#include <cassert>
#include <fstream>
#include <iostream>
#include <set>
#include <sstream>

void test_key_generation() {
    std::cout << "[TEST] Running test_key_generation..." << std::endl;
    std::string key = generate_random_key();
    assert(key.length() == 26);

    std::set<char> unique_chars(key.begin(), key.end());
    assert(unique_chars.size() == 26);
    for (char c = 'A'; c <= 'Z'; ++c) {
        assert(unique_chars.count(c) == 1);
    }
    std::cout << "  ✓ Generated valid 26-character random permutation: " << key << std::endl;
}

void test_encrypt_decrypt_roundtrip() {
    std::cout << "[TEST] Running test_encrypt_decrypt_roundtrip..." << std::endl;
    std::string key = "QWERTYUIOPASDFGHJKLZXCVBNM";
    std::string sample_plaintext = "Hello, World! This is Modern Cryptography Lab 6 (Group 17).";

    std::string ciphertext = mono_encrypt(sample_plaintext, key);
    assert(!ciphertext.empty());
    assert(ciphertext != sample_plaintext);

    // Non-letters should be preserved
    assert(ciphertext.find(',') != std::string::npos);
    assert(ciphertext.find('!') != std::string::npos);
    assert(ciphertext.find("17") != std::string::npos);

    std::string decrypted = mono_decrypt(ciphertext, key);
    assert(decrypted == sample_plaintext);
    std::cout << "  ✓ Encryption/Decryption perfectly restored original plaintext." << std::endl;
}

void test_frequency_analysis() {
    std::cout << "[TEST] Running test_frequency_analysis..." << std::endl;
    std::string text = "AAAAA BBB CC D";
    auto freqs = frequency_analysis(text);

    assert(freqs.size() == 26);
    assert(freqs[0].letter == 'A');
    assert(freqs[0].count == 5);
    assert(freqs[1].letter == 'B');
    assert(freqs[1].count == 3);
    assert(freqs[2].letter == 'C');
    assert(freqs[2].count == 2);
    assert(freqs[3].letter == 'D');
    assert(freqs[3].count == 1);

    // Check descending order
    for (size_t i = 1; i < freqs.size(); ++i) {
        assert(freqs[i - 1].count >= freqs[i].count);
    }
    std::cout << "  ✓ Single letter frequencies correctly calculated and sorted descending." << std::endl;
}

void test_word_frequency_analysis() {
    std::cout << "[TEST] Running test_word_frequency_analysis..." << std::endl;
    std::string text = "A cat sat on a mat. The cat was on the mat.";
    WordStats stats = word_frequency_analysis(text);

    // 1-letter word: "A"
    assert(stats.one_letter_words.count("A") == 1);
    assert(stats.one_letter_words["A"] == 2);

    // 2-letter word: "ON"
    assert(stats.two_letter_words.count("ON") == 1);
    assert(stats.two_letter_words["ON"] == 2);

    // 3-letter words: "CAT", "SAT", "MAT", "THE", "WAS"
    assert(stats.three_letter_words.count("CAT") == 1);
    assert(stats.three_letter_words["CAT"] == 2);
    assert(stats.three_letter_words.count("THE") == 1);
    assert(stats.three_letter_words["THE"] == 2);

    // Repeated words
    assert(stats.repeated_words.count("CAT") == 1);
    assert(stats.repeated_words.count("MAT") == 1);

    std::cout << "  ✓ Word token categorization (1, 2, 3-letter & repeated words) verified." << std::endl;
}

void test_dataset_analysis() {
    std::cout << "[TEST] Running test_dataset_analysis on Katz & Lindell Page 47..." << std::endl;
    std::ifstream file("../datasets/katz_lindell_p47.txt");
    if (!file.is_open()) {
        file.open("datasets/katz_lindell_p47.txt");
    }

    if (file.is_open()) {
        std::stringstream buffer;
        buffer << file.rdbuf();
        std::string plaintext = buffer.str();
        assert(plaintext.length() > 500);

        std::string key = "QWERTYUIOPASDFGHJKLZXCVBNM";
        std::string ciphertext = mono_encrypt(plaintext, key);

        auto freqs = frequency_analysis(ciphertext);
        WordStats word_stats = word_frequency_analysis(ciphertext);

        std::cout << "  ✓ Read " << plaintext.length() << " characters from dataset." << std::endl;
        std::cout << "  Top 5 Ciphertext Letters:" << std::endl;
        for (int i = 0; i < 5 && i < static_cast<int>(freqs.size()); ++i) {
            std::cout << "    " << freqs[i].letter << ": " << freqs[i].count
                      << " (" << freqs[i].percentage << "%)" << std::endl;
        }

        std::cout << "  Found " << word_stats.one_letter_words.size() << " unique 1-letter words, "
                  << word_stats.two_letter_words.size() << " unique 2-letter words, "
                  << word_stats.three_letter_words.size() << " unique 3-letter words." << std::endl;
    } else {
        std::cout << "  (Dataset file not found at relative path; skipping file read test)" << std::endl;
    }
}

int main() {
    std::cout << "==================================================" << std::endl;
    std::cout << " CryptoLabX - Assignment 6 C++ Engine Unit Tests " << std::endl;
    std::cout << " Author: Mukund Rakholiya (2024UCP1163) - Group 17" << std::endl;
    std::cout << "==================================================" << std::endl;

    test_key_generation();
    test_encrypt_decrypt_roundtrip();
    test_frequency_analysis();
    test_word_frequency_analysis();
    test_dataset_analysis();

    std::cout << "\n>>> ALL ASSIGNMENT 6 C++ UNIT TESTS PASSED SUCCESSFULLY! <<<" << std::endl;
    return 0;
}
