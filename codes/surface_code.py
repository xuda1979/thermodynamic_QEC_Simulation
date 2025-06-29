"""Placeholder for a surface code implementation."""

"""Very small surface code example using Stim."""

from typing import Sequence

import stim

from .base import QECCode


class SurfaceCode(QECCode):
    """Simple surface code skeleton."""

    def __init__(self, distance: int):
        self.distance = distance

    def generate_circuit(self) -> stim.Circuit:
        """Generate a simple stabilizer measurement circuit."""
        num_qubits = self.distance**2
        circuit = stim.Circuit()
        for q in range(num_qubits):
            circuit.append_operation("H", [q])
        circuit.append_operation("M", list(range(num_qubits)))
        return circuit

    def decode(self, syndrome: Sequence[int]):
        """Naive decoder returning no correction if syndrome has even parity."""
        parity = sum(syndrome) % 2
        return None if parity == 0 else (0, "X")
