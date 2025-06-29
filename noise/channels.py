"""Basic noise channel implementations using stim."""

import stim

from .base import NoiseModel


class DepolarizingNoise(NoiseModel):
    """Apply single-qubit depolarizing noise."""

    def __init__(self, probability: float):
        self.p = probability

    def apply(self, circuit: stim.Circuit) -> stim.Circuit:
        noisy = circuit.copy()
        noisy.append_operation("DEPOLARIZE1", circuit.num_qubits, self.p)
        return noisy


class AmplitudeDampingNoise(NoiseModel):
    """Apply amplitude damping using stim's PAULI_CHANNEL."""

    def __init__(self, probability: float):
        self.p = probability

    def apply(self, circuit: stim.Circuit) -> stim.Circuit:
        noisy = circuit.copy()
        # approximate amplitude damping via a simple pauli channel
        noisy.append_operation("PAULI_CHANNEL_1", circuit.num_qubits, [self.p, 0.0, 0.0])
        return noisy
