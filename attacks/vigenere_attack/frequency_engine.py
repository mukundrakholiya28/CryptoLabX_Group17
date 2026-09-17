from attacks.shift_cipher_attack.src.chi_square_attack import ENGLISH_FREQ


def split_into_groups(ciphertext: str, key_length: int) -> list[str]:
    """Divide ciphertext into key_length interleaved groups."""

    if key_length <= 0:
        raise ValueError("Key length must be greater than 0")

    cleaned = "".join(
        char.upper() for char in ciphertext if char.isalpha()
    )

    groups = ["" for _ in range(key_length)]

    for i, char in enumerate(cleaned):
        groups[i % key_length] += char

    return groups


def frequency_analysis(group_text: str) -> dict[str, float]:
    """Calculate observed A-Z letter frequencies as percentages."""

    letters = [
        char.upper()
        for char in group_text
        if char.isalpha()
    ]

    total = len(letters)

    frequencies = {
        chr(ord("A") + i): 0.0
        for i in range(26)
    }

    if total == 0:
        return frequencies

    for char in letters:
        frequencies[char] += 1

    for char in frequencies:
        frequencies[char] = (
            frequencies[char] / total
        ) * 100

    return frequencies


def find_shift(group_text: str) -> int:
    """
    Estimate the Caesar shift for a Vigenere coset
    using Chi-Square goodness-of-fit.
    """

    letters = [
        char.upper()
        for char in group_text
        if char.isalpha()
    ]

    if not letters:
        return 0

    best_shift = 0
    lowest_chi_square = float("inf")

    total = len(letters)

    for shift in range(26):
        observed = {
            chr(ord("A") + i): 0
            for i in range(26)
        }

        # Decrypt the group using this candidate shift
        for char in letters:
            cipher_value = ord(char) - ord("A")
            plain_value = (cipher_value - shift) % 26
            plain_char = chr(ord("A") + plain_value)

            observed[plain_char] += 1

        chi_square = 0.0

        for char, probability in ENGLISH_FREQ.items():
            expected = total * probability
            observed_count = observed[char]

            if expected > 0:
                chi_square += (
                    (observed_count - expected) ** 2
                ) / expected

        if chi_square < lowest_chi_square:
            lowest_chi_square = chi_square
            best_shift = shift

    return best_shift


def find_key(groups: list[str]) -> str:
    """Combine the best Caesar shifts into the Vigenere key."""

    key = ""

    for group in groups:
        shift = find_shift(group)
        key += chr(ord("A") + shift)

    return key


def vigenere_decrypt(ciphertext: str, key: str) -> str:
    """Decrypt ciphertext using the repeating Vigenere key."""

    if not key:
        raise ValueError("Key cannot be empty")

    key = key.upper()
    plaintext = []
    key_index = 0

    for char in ciphertext:
        if char.isalpha():
            cipher_value = ord(char.upper()) - ord("A")
            key_value = ord(key[key_index % len(key)]) - ord("A")

            plain_value = (cipher_value - key_value) % 26
            plaintext.append(chr(ord("A") + plain_value))

            key_index += 1
        else:
            plaintext.append(char)

    return "".join(plaintext)


def vigenere_encrypt(plaintext: str, key: str) -> str:
    """Encrypt plaintext using the repeating Vigenere key."""

    if not key:
        raise ValueError("Key cannot be empty")

    key = key.upper()
    ciphertext = []
    key_index = 0

    for char in plaintext:
        if char.isalpha():
            plain_value = ord(char.upper()) - ord("A")
            key_value = ord(key[key_index % len(key)]) - ord("A")

            cipher_value = (plain_value + key_value) % 26
            ciphertext.append(chr(ord("A") + cipher_value))

            key_index += 1
        else:
            ciphertext.append(char)

    return "".join(ciphertext)


def verify(
    original_ciphertext: str,
    re_encrypted_text: str
) -> bool:
    """Check whether re-encryption matches the original ciphertext."""

    original_clean = "".join(
        char.upper()
        for char in original_ciphertext
        if char.isalpha()
    )

    re_encrypted_clean = "".join(
        char.upper()
        for char in re_encrypted_text
        if char.isalpha()
    )

    return original_clean == re_encrypted_clean