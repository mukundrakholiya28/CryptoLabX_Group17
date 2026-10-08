from attacks.padding_oracle_attack.oracle import PaddingOracle
from attacks.padding_oracle_attack.block_attack import (
    split_blocks,
    padding_oracle_decrypt,
)


def test_split_blocks():

    data = b"A" * 32

    blocks = split_blocks(data, 16)

    assert len(blocks) == 2
    assert blocks[0] == b"A" * 16
    assert blocks[1] == b"A" * 16


def test_split_blocks_invalid_length():

    data = b"A" * 17

    try:
        split_blocks(data, 16)
        assert False
    except ValueError:
        assert True


def test_single_block_recovery():

    oracle = PaddingOracle()

    plaintext = b"Hello Padding!"

    iv, ciphertext = oracle.encrypt(plaintext)

    recovered, queries = padding_oracle_decrypt(
        oracle,
        iv,
        ciphertext
    )

    assert recovered == plaintext
    assert queries > 0


def test_multi_block_recovery():

    oracle = PaddingOracle()

    plaintext = (
        b"This plaintext is intentionally longer than one AES block "
        b"so that we can test multi-block recovery."
    )

    iv, ciphertext = oracle.encrypt(plaintext)

    recovered, queries = padding_oracle_decrypt(
        oracle,
        iv,
        ciphertext
    )

    assert recovered == plaintext
    assert queries > 0


def test_exact_block_size_plaintext():

    oracle = PaddingOracle()

    plaintext = b"A" * 16

    iv, ciphertext = oracle.encrypt(plaintext)

    recovered, queries = padding_oracle_decrypt(
        oracle,
        iv,
        ciphertext
    )

    assert recovered == plaintext
    assert queries > 0