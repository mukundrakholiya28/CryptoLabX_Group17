"""
Single-Byte Decryption Engine — Assignment 7 (CryptoLabX Group 17)
Member 1: Mukund Rakholiya (2024UCP1163)

This module implements the core byte-level cryptographic logic for the
Padding Oracle Attack against AES-CBC.

Mathematical Foundation:
In AES-CBC mode, decryption of block C_i is governed by:
    P_i = D_K(C_i) ^ C_{i-1} = I_i ^ C_{i-1}
where I_i = D_K(C_i) represents the intermediate state value prior to CBC XOR.

By crafting a modified predecessor block C'_{i-1}, we query the padding oracle
to find a candidate byte that yields valid PKCS#7 padding of value pad_val = 16 - k:
    P'_i[k] = pad_val  ==>  I_i[k] ^ C'_{i-1}[k] = pad_val
    ==>  I_i[k] = C'_{i-1}[k] ^ pad_val

Once I_i[k] is extracted, the true plaintext byte is recovered unconditionally:
    P_i[k] = I_i[k] ^ C_{i-1}[k]
"""

from typing import Dict, Tuple
from attacks.padding_oracle_attack.oracle import PaddingOracle


def recover_byte(
    oracle: PaddingOracle,
    prev_block: bytes,
    target_block: bytes,
    byte_index: int,
    known_intermediate: Dict[int, int]
) -> Tuple[int, int]:
    """Recovers the intermediate state byte and original plaintext byte at byte_index.
    
    Operates from right to left (byte_index: 15 down to 0).
    
    Args:
        oracle: Active PaddingOracle instance with unexposed AES key.
        prev_block: The original 16-byte predecessor block (C_{i-1} or IV).
        target_block: The 16-byte target ciphertext block (C_i) being attacked.
        byte_index: Index of the target byte within the block (0 <= byte_index <= 15).
        known_intermediate: Dictionary mapping solved byte indices (> byte_index)
                            to their recovered intermediate values I_i[j].
                            
    Returns:
        A tuple (intermediate_byte, plaintext_byte):
        - intermediate_byte: The recovered I_i[byte_index] in range [0, 255].
        - plaintext_byte: The original decrypted byte P_i[byte_index] in range [0, 255].
        
    Raises:
        ValueError: If inputs have invalid lengths or byte_index is out of range.
        RuntimeError: If all 256 candidate values fail to satisfy the oracle.
    """
    block_size = oracle.block_size
    if len(prev_block) != block_size or len(target_block) != block_size:
        raise ValueError(
            f"Both prev_block and target_block must be exactly {block_size} bytes"
        )
    if not (0 <= byte_index < block_size):
        raise ValueError(
            f"byte_index {byte_index} is out of valid range [0, {block_size - 1}]"
        )
    
    pad_val = block_size - byte_index
    crafted_prev = bytearray(block_size)
    
    # Configure all already-known bytes to the right (j > byte_index)
    # so that: P'_i[j] = I_i[j] ^ crafted_prev[j] = pad_val
    for j in range(byte_index + 1, block_size):
        if j not in known_intermediate:
            raise ValueError(f"Missing intermediate value for byte index {j}")
        crafted_prev[j] = known_intermediate[j] ^ pad_val
    
    # Try all 256 possible byte values for crafted_prev[byte_index]
    for candidate in range(256):
        crafted_prev[byte_index] = candidate
        
        if oracle.is_padding_valid(iv=bytes(crafted_prev), ciphertext=target_block):
            # Edge Case Disambiguation:
            # When attacking the last byte (byte_index == 15, pad_val == 1),
            # the decrypted text could accidentally end in (0x02, 0x02), (0x03, 0x03, 0x03), etc.
            # We verify that candidate yields a genuine 0x01 pad by perturbing byte 14.
            if byte_index == block_size - 1:
                perturbed_prev = bytearray(crafted_prev)
                perturbed_prev[byte_index - 1] ^= 0x01
                if not oracle.is_padding_valid(iv=bytes(perturbed_prev), ciphertext=target_block):
                    # Padding was broken by altering byte 14 -> accidental multi-byte pad!
                    continue
            
            intermediate_byte = candidate ^ pad_val
            plaintext_byte = intermediate_byte ^ prev_block[byte_index]
            return intermediate_byte, plaintext_byte
            
    raise RuntimeError(
        f"Failed to recover byte at index {byte_index}: no candidate satisfied oracle"
    )
