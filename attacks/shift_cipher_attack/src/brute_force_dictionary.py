import string
from shift_cipher import decrypt

with open("attacks\\shift_cipher_attack\\dictionary\\english_words.txt", "r") as file:
    dictionary = set()

    for word in file:
        word = word.strip().lower()
        dictionary.add(word)


def dictionary_score(text):
    score = 0

    words = text.split()

    for word in words:
        word = word.strip(string.punctuation).lower()

        if word in dictionary:
            score += 1

    return score

def brute_force_attack(ciphertext):
    best_key = 0
    best_score = 0
    best_plaintext = ""

    for key in range(26):
        plaintext = decrypt(ciphertext, key)

        score = dictionary_score(plaintext)

        if score > best_score:
            best_score = score
            best_key = key
            best_plaintext = plaintext

    return best_key, best_plaintext, best_score

