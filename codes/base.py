"""Base classes for quantum error-correcting codes."""

from abc import ABC, abstractmethod


class QECCode(ABC):
    """Abstract base class for a quantum error-correcting code."""

    @abstractmethod
    def generate_circuit(self):
        """Return a circuit representing one round of syndrome extraction."""

    @abstractmethod
    def decode(self, syndrome):
        """Decode a syndrome and return a correction."""
