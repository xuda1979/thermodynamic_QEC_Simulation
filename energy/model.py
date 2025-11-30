"""Energy accounting utilities."""

from dataclasses import dataclass
import stim
from typing import Dict
import numpy as np

@dataclass
class EnergyModel:
    """Simple energy cost model."""

    single_qubit_gate: float = 1.0
    two_qubit_gate: float = 2.0
    measurement: float = 5.0
    reset: float = 3.0

    # Decoding costs
    # Cost per detection event (syndrome defect) processed by MWPM.
    # This accounts for the classical processing energy required to match this defect.
    decoding_event_cost: float = 20.0

    def calculate_circuit_energy(self, circuit: stim.Circuit) -> float:
        """
        Calculate the energy cost of a stim circuit based on instruction counts.

        Args:
            circuit: The stim circuit.

        Returns:
            total_energy: The estimated energy cost.
        """
        energy = 0.0

        for instruction in circuit.flattened():
            name = instruction.name
            targets = len(instruction.targets_copy())

            # Simple heuristic mapping
            if name in ["H", "R", "X", "Y", "Z", "I", "S", "S_DAG", "SQRT_X", "SQRT_X_DAG", "SQRT_Y", "SQRT_Y_DAG"]:
                energy += self.single_qubit_gate * targets
            elif name in ["CX", "CY", "CZ", "CNOT", "SWAP", "ISWAP", "SQRT_XX", "SQRT_YY", "SQRT_ZZ", "XCX", "XCY", "XCZ", "YCX", "YCY", "YCZ", "ZCX", "ZCY", "ZCZ"]:
                # Two qubit gates. Stim format: targets list contains pairs.
                num_gates = targets / 2
                energy += self.two_qubit_gate * num_gates
            elif name in ["M", "MX", "MY", "MZ", "MPP"]:
                energy += self.measurement * targets
            elif name in ["R", "RX", "RY", "RZ"]:
                energy += self.reset * targets
            elif name in ["MR", "MRX", "MRY", "MRZ"]:
                energy += (self.measurement + self.reset) * targets

        return energy

    def calculate_decoding_energy(self, num_detection_events: int) -> float:
        """
        Calculate the energy cost of decoding based on the number of detection events.

        Args:
            num_detection_events: The number of defects observed in the shot.

        Returns:
            energy: The estimated decoding energy.
        """
        return self.decoding_event_cost * num_detection_events
