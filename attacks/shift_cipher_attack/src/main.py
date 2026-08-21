import os
from brute_force_dictionary import load_dictionary, attack_dictionary
from chi_square_attack import attack_chi_square
from shift_cipher import encrypt

def main():
    dict_path = os.path.join(os.path.dirname(__file__), "..", "dictionary", "english_words.txt")
    
    if os.path.exists(dict_path):
        dictionary = load_dictionary(dict_path)
    else:
        dictionary = {"the", "quick", "brown", "fox", "jumps", "over", "lazy", "dog",
                      "cryptography", "is", "essential", "for", "secure", "communication",
                      "attack", "cipher", "secret", "message", "this", "test"}

    test_corpus = [
        ("TC1: Standard Sentence", "Cryptography provides confidentiality and integrity.", 7),
        ("TC2: Short Ambiguous Phrase", "Be back soon", 15),
        ("TC3: Stripped Whitespace", "CONFIDENTIALMESSAGEFORDIRECTOR", 3),
        ("TC4: Slang / Technical Jargon", "K8s cluster zero day vulnerability exploit", 11)
    ]

    print("=" * 88)
    print(f"{'Test Case':<32} | {'Act Key':<7} | {'Dict Key':<8} | {'Chi Key':<7} | {'Dict Match':<10} | {'Chi Match'}")
    print("=" * 88)

    for name, plaintext, key in test_corpus:
        ciphertext = encrypt(plaintext, key)
        
        dict_res = attack_dictionary(ciphertext, dictionary)
        chi_res = attack_chi_square(ciphertext)

        dict_pred = dict_res["predicted_key"]
        chi_pred = chi_res["predicted_key"]

        dict_ok = "YES" if dict_pred == key else "NO"
        chi_ok = "YES" if chi_pred == key else "NO"

        print(f"{name:<32} | {key:<7} | {dict_pred:<8} | {chi_pred:<7} | {dict_ok:<10} | {chi_ok}")
    print("=" * 88)

if __name__ == "__main__":
    main()