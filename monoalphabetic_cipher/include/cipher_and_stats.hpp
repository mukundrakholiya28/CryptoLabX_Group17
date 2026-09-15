#ifndef CIPHER_AND_STATS_HPP
#define CIPHER_AND_STATS_HPP

#include <string>
#include <vector>
#include <map>

/**
 * @brief Represents letter frequency metrics for a single letter.
 */
struct LetterFrequency {
    char letter;
    int count;
    double percentage;
};

/**
 * @brief Word frequency metrics across different word lengths.
 */
struct WordStats {
    std::map<std::string, int> one_letter_words;
    std::map<std::string, int> two_letter_words;
    std::map<std::string, int> three_letter_words;
    std::map<std::string, int> repeated_words; // Words appearing >= 2 times
};

// ==========================================
// Monoalphabetic Substitution Cipher
// ==========================================

/**
 * @brief Generates a random 26-character permutation key from 'A' to 'Z'.
 */
std::string generate_random_key();

/**
 * @brief Encrypts plaintext using a 26-character substitution key.
 * Non-alphabetic characters are preserved; letter case is maintained.
 */
std::string mono_encrypt(const std::string& plaintext, const std::string& key);

/**
 * @brief Decrypts ciphertext using the 26-character substitution key.
 */
std::string mono_decrypt(const std::string& ciphertext, const std::string& key);

// ==========================================
// Statistical & Frequency Analysis
// ==========================================

/**
 * @brief Performs single letter frequency analysis on ciphertext.
 * Returns letter frequencies sorted in descending order of occurrence.
 */
std::vector<LetterFrequency> frequency_analysis(const std::string& ciphertext);

/**
 * @brief Analyzes ciphertext word tokens and categorizes 1-letter, 2-letter, 3-letter,
 * and repeated words.
 */
WordStats word_frequency_analysis(const std::string& ciphertext);

#endif // CIPHER_AND_STATS_HPP
