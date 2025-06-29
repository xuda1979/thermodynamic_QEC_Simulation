"""Noise model abstractions."""

from abc import ABC, abstractmethod


class NoiseModel(ABC):
    """Abstract noise model interface."""

    @abstractmethod
    def apply(self, circuit):
        """Apply noise to a circuit (placeholder)."""
