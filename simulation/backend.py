"""Simulation backend abstractions."""

from abc import ABC, abstractmethod

import stim


class Simulator(ABC):
    """Abstract simulator."""

    @abstractmethod
    def run(self, circuit, noise_model, shots: int = 1):
        """Run a noisy circuit and return results."""


class StimSimulator(Simulator):
    """Simulator implementation using stim."""

    def run(self, circuit: stim.Circuit, noise_model, shots: int = 1):
        noisy = noise_model.apply(circuit)
        sampler = noisy.compile_sampler()
        return sampler.sample(shots)
