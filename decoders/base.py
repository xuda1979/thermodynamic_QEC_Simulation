"""Decoder abstractions."""

from abc import ABC, abstractmethod


class Decoder(ABC):
    """Abstract decoder."""

    @abstractmethod
    def decode(self, syndrome):
        """Return a correction based on the syndrome."""
