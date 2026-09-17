#ifndef PATTERN_SOLVER_HPP
#define PATTERN_SOLVER_HPP

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
    std::map<std::string, std::vector<std::string>> pattern_signatures;
    std::map<std::string, int> double_letter_patterns;
};

PatternStats pattern_analysis(const std::string& ciphertext);

std::string apply_substitution(
    const std::string& ciphertext,
    const std::map<char, char>& cipher_to_plain_map
);

void display_partial_plaintext(
    const std::string& ciphertext,
    const std::map<char, char>& cipher_to_plain_map
);

bool verify_solution(
    const std::string& original_plaintext,
    const std::string& recovered_key,
    const std::string& ciphertext
);

#endif