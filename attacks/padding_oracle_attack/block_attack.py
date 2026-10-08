from attacks.padding_oracle_attack.oracle import PaddingOracle, unpad_pkcs7
from attacks.padding_oracle_attack.byte_decryptor import recover_byte


def split_blocks(data: bytes, block_size: int = 16) -> list[bytes]:
    """Split data into blocks of block_size bytes."""

    if block_size <= 0:
        raise ValueError("Block size must be positive")

    if len(data) % block_size != 0:
        raise ValueError(
            f"Data length {len(data)} is not a multiple of block size {block_size}"
        )

    return [
        data[i:i + block_size]
        for i in range(0, len(data), block_size)
    ]


def recover_block(
    oracle: PaddingOracle,
    prev_block: bytes,
    target_block: bytes
) -> bytes:
    """
    Recover one complete plaintext block using the padding oracle.

    The bytes are recovered from right to left:
        byte 15 -> byte 14 -> ... -> byte 0
    """

    block_size = oracle.block_size

    if len(prev_block) != block_size:
        raise ValueError("Invalid previous block length")

    if len(target_block) != block_size:
        raise ValueError("Invalid target block length")

    known_intermediate = {}
    plaintext = bytearray(block_size)

    # Recover bytes from right to left
    for byte_index in range(block_size - 1, -1, -1):

        intermediate_byte, plaintext_byte = recover_byte(
            oracle=oracle,
            prev_block=prev_block,
            target_block=target_block,
            byte_index=byte_index,
            known_intermediate=known_intermediate
        )

        # Store intermediate value because it is required
        # when attacking the next byte to the left.
        known_intermediate[byte_index] = intermediate_byte

        # Store recovered plaintext byte.
        plaintext[byte_index] = plaintext_byte

    return bytes(plaintext)


def padding_oracle_decrypt(
    oracle: PaddingOracle,
    iv: bytes,
    ciphertext: bytes
) -> tuple[bytes, int]:
    """
    Recover the complete plaintext using the padding oracle.

    Returns:
        (unpadded_plaintext, total_oracle_queries)
    """

    block_size = oracle.block_size

    if len(iv) != block_size:
        raise ValueError("IV must be exactly one block long")

    if not ciphertext:
        raise ValueError("Ciphertext cannot be empty")

    if len(ciphertext) % block_size != 0:
        raise ValueError(
            "Ciphertext length must be a multiple of the block size"
        )

    # Start counting only the queries belonging to the attack.
    oracle.reset_query_count()

    ciphertext_blocks = split_blocks(ciphertext, block_size)

    recovered_plaintext = bytearray()

    previous_block = iv

    # Attack every ciphertext block.
    for target_block in ciphertext_blocks:

        plaintext_block = recover_block(
            oracle,
            previous_block,
            target_block
        )

        recovered_plaintext.extend(plaintext_block)

        # For the next block, the current ciphertext block
        # becomes the previous block.
        previous_block = target_block

    # Remove PKCS#7 padding.
    plaintext = unpad_pkcs7(
        bytes(recovered_plaintext),
        block_size
    )

    return plaintext, oracle.query_count