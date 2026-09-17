#include "../include/pattern_solver.hpp"

#include <cctype>
#include <iostream>
#include <string>
#include <vector>
#include <map>
#include <set>
#include <algorithm>

PatternStats pattern_analysis(const std::string& ciphertext)
{
    PatternStats stats;

    // Store the current word while scanning the ciphertext
    std::string word;

    // Process one word at a time
    for (size_t i = 0; i <= ciphertext.length(); i++)
    {
        // A word ends at a space or at the end of the text
        if (i == ciphertext.length() ||
            std::isspace(static_cast<unsigned char>(ciphertext[i])))
        {
            if (!word.empty())
            {
                // Generate word pattern
                std::map<char, int> mapping;
                int next_number = 1;
                std::string pattern;

                for (char ch : word)
                {
                    if (mapping.find(ch) == mapping.end())
                    {
                        mapping[ch] = next_number++;
                    }

                    pattern += std::to_string(mapping[ch]);
                }

                stats.pattern_signatures[pattern].push_back(word);

                // Find double letters
                for (size_t j = 1; j < word.length(); j++)
                {
                    if (word[j] == word[j - 1])
                    {
                        std::string pair;
                        pair += word[j - 1];
                        pair += word[j];

                        stats.double_letter_patterns[pair]++;
                    }
                }

                word.clear();
            }
        }
        else
        {
            // Keep only alphabetic characters
            if (std::isalpha(static_cast<unsigned char>(ciphertext[i])))
            {
                word += static_cast<char>(
                    std::toupper(static_cast<unsigned char>(ciphertext[i]))
                );
            }
        }
    }

    return stats;
}

std::string apply_substitution(
    const std::string& ciphertext,
    const std::map<char, char>& cipher_to_plain_map)
{
    std::string plaintext;

    for (char ch : ciphertext)
    {
        char upper_ch = static_cast<char>(
            std::toupper(static_cast<unsigned char>(ch))
        );

        // Preserve spaces and punctuation
        if (!std::isalpha(static_cast<unsigned char>(ch)))
        {
            plaintext += ch;
            continue;
        }

        // Check whether this ciphertext letter has a mapping
        auto it = cipher_to_plain_map.find(upper_ch);

        if (it != cipher_to_plain_map.end())
        {
            plaintext += it->second;
        }
        else
        {
            // Unknown letter
            plaintext += '_';
        }
    }

    return plaintext;
}

void display_partial_plaintext(
    const std::string& ciphertext,
    const std::map<char, char>& cipher_to_plain_map)
{
    std::string partial_plaintext =
        apply_substitution(ciphertext, cipher_to_plain_map);

    std::cout << "Partial Plaintext:\n";
    std::cout << partial_plaintext << "\n";
}

bool verify_solution(
    const std::string& original_plaintext,
    const std::string& recovered_key,
    const std::string& ciphertext)
{
    std::string encrypted_text;

    // Monoalphabetic substitution uses a 26-character key.
    if (recovered_key.length() != 26)
    {
        return false;
    }

    // Encrypt the original plaintext using the recovered key.
    for (char ch : original_plaintext)
    {
        if (std::isalpha(static_cast<unsigned char>(ch)))
        {
            char upper_ch = static_cast<char>(
                std::toupper(static_cast<unsigned char>(ch))
            );

            int index = upper_ch - 'A';

            char encrypted_char =
                static_cast<char>(std::toupper(
                    static_cast<unsigned char>(recovered_key[index])
                ));

            encrypted_text += encrypted_char;
        }
        else
        {
            encrypted_text += ch;
        }
    }

    // Compare the generated ciphertext with the supplied ciphertext.
    return encrypted_text == ciphertext;
}