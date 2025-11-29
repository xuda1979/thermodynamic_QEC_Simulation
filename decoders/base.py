"""Decoder abstractions."""

from abc import ABC, abstractmethod


class Decoder(ABC):
    """Abstract decoder."""

    @abstractmethod
    def decode(self, syndrome):
        """Return a correction based on the syndrome."""

    @abstractmethod
    def decode_shots(self, shots):
        """Decode a batch of shots."""
        pass
