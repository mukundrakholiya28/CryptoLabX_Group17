#include "cipher_and_stats.hpp"

#include <algorithm>
#include <cctype>
#include <random>
#include <sstream>
#include <stdexcept>

// ==========================================
// Monoalphabetic Substitution Cipher
// ==========================================

std::string generate_random_key() {
    std::string alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";
    std::random_device rd;
    std::mt19937 g(rd());
    std::shuffle(alphabet.begin(), alphabet.end(), g);
    return alphabet;
}

std::string mono_encrypt(const std::string& plaintext, const std::string& key) {
    if (key.length() != 26) {
        throw std::invalid_argument("Substitution key must be exactly 26 characters.");
    }

    std::string ciphertext = "";
    ciphertext.reserve(plaintext.length());

    for (char ch : plaintext) {
        if (std::isupper(static_cast<unsigned char>(ch))) {
            int index = ch - 'A';
            ciphertext += std::toupper(static_cast<unsigned char>(key[index]));
        } else if (std::islower(static_cast<unsigned char>(ch))) {
            int index = ch - 'a';
            ciphertext += std::tolower(static_cast<unsigned char>(key[index]));
        } else {
            ciphertext += ch; // preserve whitespace, numbers, punctuation
        }
    }
    return ciphertext;
}

std::string mono_decrypt(const std::string& ciphertext, const std::string& key) {
    if (key.length() != 26) {
        throw std::invalid_argument("Substitution key must be exactly 26 characters.");
    }

    // Build inverse mapping: key[i] maps back to 'A' + i
    char inverse_map_upper[26];
    char inverse_map_lower[26];

    for (int i = 0; i < 26; ++i) {
        char key_char_upper = std::toupper(static_cast<unsigned char>(key[i]));
        int target_index = key_char_upper - 'A';
        inverse_map_upper[target_index] = static_cast<char>('A' + i);
        inverse_map_lower[target_index] = static_cast<char>('a' + i);
    }

    std::string plaintext = "";
    plaintext.reserve(ciphertext.length());

    for (char ch : ciphertext) {
        if (std::isupper(static_cast<unsigned char>(ch))) {
            int index = ch - 'A';
            plaintext += inverse_map_upper[index];
        } else if (std::islower(static_cast<unsigned char>(ch))) {
            int index = ch - 'a';
            plaintext += inverse_map_lower[index];
        } else {
            plaintext += ch;
        }
    }
    return plaintext;
}

// ==========================================
// Statistical & Frequency Analysis
// ==========================================

std::vector<LetterFrequency> frequency_analysis(const std::string& ciphertext) {
    std::map<char, int> counts;
    for (char c = 'A'; c <= 'Z'; ++c) {
        counts[c] = 0;
    }

    int total_letters = 0;
    for (char ch : ciphertext) {
        if (std::isalpha(static_cast<unsigned char>(ch))) {
            char upper_ch = std::toupper(static_cast<unsigned char>(ch));
            counts[upper_ch]++;
            total_letters++;
        }
    }

    std::vector<LetterFrequency> results;
    results.reserve(26);

    for (char c = 'A'; c <= 'Z'; ++c) {
        int cnt = counts[c];
        double pct = (total_letters > 0) ? (static_cast<double>(cnt) / total_letters * 100.0) : 0.0;
        results.push_back({c, cnt, pct});
    }

    // Sort descending by count, tie-break alphabetically
    std::sort(results.begin(), results.end(), [](const LetterFrequency& a, const LetterFrequency& b) {
        if (a.count != b.count) {
            return a.count > b.count;
        }
        return a.letter < b.letter;
    });

    return results;
}

WordStats word_frequency_analysis(const std::string& ciphertext) {
    WordStats stats;
    std::map<std::string, int> all_words_map;

    std::string current_word = "";
    for (size_t i = 0; i <= ciphertext.length(); ++i) {
        char ch = (i < ciphertext.length()) ? ciphertext[i] : ' ';
        if (std::isalpha(static_cast<unsigned char>(ch))) {
            current_word += std::toupper(static_cast<unsigned char>(ch));
        } else {
            if (!current_word.empty()) {
                all_words_map[current_word]++;

                if (current_word.length() == 1) {
                    stats.one_letter_words[current_word]++;
                } else if (current_word.length() == 2) {
                    stats.two_letter_words[current_word]++;
                } else if (current_word.length() == 3) {
                    stats.three_letter_words[current_word]++;
                }

                current_word.clear();
            }
        }
    }

    for (const auto& pair : all_words_map) {
        if (pair.second >= 2) {
            stats.repeated_words[pair.first] = pair.second;
        }
    }

    return stats;
}
