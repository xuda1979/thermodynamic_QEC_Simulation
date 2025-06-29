"""Simulation backend abstractions."""

from abc import ABC, abstractmethod


class Simulator(ABC):
    """Abstract simulator."""

    @abstractmethod
    def run(self, circuit, noise_model, shots: int = 1):
        """Run a noisy circuit and return results."""
