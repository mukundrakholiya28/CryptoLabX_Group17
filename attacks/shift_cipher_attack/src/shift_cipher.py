"""
Shift Cipher Implementation (Encryption and Decryption)
"""

def encrypt(plaintext: str, key: int) -> str:
    """Encrypts plaintext using Caesar shift key k (0-25)."""
    result = []
    key = key % 26
    for char in plaintext:
        if char.isupper():
            result.append(chr((ord(char) - ord('A') + key) % 26 + ord('A')))
        elif char.islower():
            result.append(chr((ord(char) - ord('a') + key) % 26 + ord('a')))
        else:
            result.append(char)
    return "".join(result)


def decrypt(ciphertext: str, key: int) -> str:
    """Decrypts ciphertext using Caesar shift key k (0-25)."""
    return encrypt(ciphertext, -key)