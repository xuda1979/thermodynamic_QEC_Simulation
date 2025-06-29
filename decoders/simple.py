"""Extremely simple decoder for demonstration."""

from typing import Sequence

from .base import Decoder


class SimpleDecoder(Decoder):
    """A naive decoder that checks syndrome parity."""

    def decode(self, syndrome: Sequence[int]):
        parity = sum(syndrome) % 2
        return None if parity == 0 else (0, "X")
