"""
CryptoLabX — Unit Tests for Predictable Password Reset Token Attack
Author: Lakshay Ahuja (2024UCP1157)
Group: 17
"""

import pytest
from attacks.reset_token_attack import (
    generate_reset_token,
    predict_reset_token,
    verify_token_match,
)


class TestResetTokenGeneration:
    """Tests for token generation format, length, and determinism."""

    def test_token_length_and_format(self):
        t, hex_tok, raw = generate_reset_token()
        assert isinstance(t, int)
        assert len(hex_tok) == 32  # 16 bytes in hex = 32 chars
        assert len(raw) == 16
        assert bytes.fromhex(hex_tok) == raw

    def test_token_determinism(self):
        seed_t = 1700000000
        _, hex1, _ = generate_reset_token(seed_t)
        _, hex2, _ = generate_reset_token(seed_t)
        _, hex3, _ = generate_reset_token(seed_t + 1)
        assert hex1 == hex2
        assert hex1 != hex3


class TestTokenPredictionAttack:
    """Tests for timestamp brute-force search within time window."""

    @pytest.mark.parametrize("offset", [0, -150, 150, -299, 300])
    def test_predict_token_within_window(self, offset):
        actual_t = 1750000000
        _, hex_tok, _ = generate_reset_token(actual_t)

        approx_t = actual_t + offset
        res = predict_reset_token(hex_tok, approx_timestamp=approx_t, window_seconds=300)

        assert res.recovered_timestamp == actual_t
        assert res.is_verified is True
        assert verify_token_match(res.recovered_timestamp, hex_tok) is True

    def test_outside_window_returns_none(self):
        actual_t = 1750000000
        _, hex_tok, _ = generate_reset_token(actual_t)

        # Attacker timestamp is 500 seconds away (window is only 300s)
        approx_t = actual_t + 500
        res = predict_reset_token(hex_tok, approx_timestamp=approx_t, window_seconds=300)

        assert res.recovered_timestamp is None
        assert res.is_verified is False
        assert res.candidates_tested == 601

    def test_invalid_token_hex_raises_error(self):
        with pytest.raises(ValueError, match="must be exactly 16 bytes"):
            predict_reset_token("abcd", approx_timestamp=1700000000)
