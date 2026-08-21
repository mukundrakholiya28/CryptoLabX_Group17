def encrypt(text, key):
    result = ""

    for i in range(len(text)):
        ch = text[i]

        if ch.isalpha():
            x = ord(ch.upper()) - ord('A')
            encrypted = (x + key) % 26
            result += chr(encrypted + ord('A'))
        else:
            result += ch

    return result


def decrypt(text, key):
    result = ""

    for i in range(len(text)):
        ch = text[i]

        if ch.isalpha():
            x = ord(ch.upper()) - ord('A')
            decrypted = (x - key) % 26
            result += chr(decrypted + ord('A'))
        else:
            result += ch

    return result