import time

from attacks.padding_oracle_attack.oracle import PaddingOracle
from attacks.padding_oracle_attack.block_attack import padding_oracle_decrypt


def main():

    print("=" * 60)
    print("AES-CBC Padding Oracle Attack")
    print("CryptoLabX - Group 17")
    print("=" * 60)

    plaintext = (
        b"Padding Oracle Attack demonstrates how CBC encryption "
        b"can leak plaintext without revealing the AES key."
    )

    # Create the simulated server/oracle.
    # The AES key remains hidden inside the oracle.
    oracle = PaddingOracle()

    # Server encrypts the plaintext.
    iv, ciphertext = oracle.encrypt(plaintext)

    print("\nOriginal plaintext:")
    print(plaintext.decode())

    print("\nCiphertext length:", len(ciphertext), "bytes")
    print(
        "Number of ciphertext blocks:",
        len(ciphertext) // oracle.block_size
    )

    print("\nStarting padding oracle attack...")

    start_time = time.perf_counter()

    recovered_plaintext, total_queries = padding_oracle_decrypt(
        oracle,
        iv,
        ciphertext
    )

    execution_time = time.perf_counter() - start_time

    print("\nRecovered plaintext:")
    print(recovered_plaintext.decode())

    print("\nOracle queries:", total_queries)
    print(f"Execution time: {execution_time:.4f} seconds")

    print("\nVerification:")

    if recovered_plaintext == plaintext:
        print("SUCCESS: Recovered plaintext matches original.")
    else:
        print("FAILURE: Recovered plaintext does not match original.")

    print("\nAES key accessed during attack: NO")

    print("=" * 60)


if __name__ == "__main__":
    main()