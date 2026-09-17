#include "../include/pattern_solver.hpp"

#include <cassert>
#include <iostream>
#include <map>
#include <string>

void test_pattern_analysis()
{
    std::string ciphertext = "HELLO WORLD";

    PatternStats stats = pattern_analysis(ciphertext);

    // HELLO -> 12334
    assert(stats.pattern_signatures["12334"].size() == 1);
    assert(stats.pattern_signatures["12334"][0] == "HELLO");

    // WORLD -> 12345
    assert(stats.pattern_signatures["12345"].size() == 1);
    assert(stats.pattern_signatures["12345"][0] == "WORLD");

    // LL is a double-letter pattern
    assert(stats.double_letter_patterns["LL"] == 1);

    std::cout << "test_pattern_analysis passed\n";
}

void test_apply_substitution()
{
    std::map<char, char> mapping = {
        {'H', 'T'},
        {'E', 'H'},
        {'L', 'E'},
        {'O', 'R'}
    };

    std::string ciphertext = "HELLO WORLD";

    std::string result = apply_substitution(ciphertext, mapping);

    assert(result == "THEER _R_E_");

    std::cout << "test_apply_substitution passed\n";
}

void test_verify_solution()
{
    // Identity substitution:
    // A -> A, B -> B, ..., Z -> Z
    std::string identity_key = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";

    std::string plaintext = "HELLO WORLD";
    std::string ciphertext = "HELLO WORLD";

    assert(verify_solution(plaintext, identity_key, ciphertext));

    // Wrong ciphertext should fail
    assert(!verify_solution(plaintext, identity_key, "HELLO THERE"));

    // Wrong key length should fail
    assert(!verify_solution(plaintext, "ABC", ciphertext));

    std::cout << "test_verify_solution passed\n";
}

int main()
{
    test_pattern_analysis();
    test_apply_substitution();
    test_verify_solution();

    std::cout << "\nAll pattern solver tests passed!\n";

    return 0;
}