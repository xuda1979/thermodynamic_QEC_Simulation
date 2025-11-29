"""Energy accounting utilities."""

from dataclasses import dataclass
import stim
from typing import Dict

@dataclass
class EnergyModel:
    """Simple energy cost model."""

    single_qubit_gate: float = 1.0
    two_qubit_gate: float = 2.0
    measurement: float = 5.0
    reset: float = 3.0
    # Decoding cost parameters could be added here, e.g. per graph node or edge
    decoding_graph_node_cost: float = 0.0
    decoding_graph_edge_cost: float = 0.0

    def calculate_circuit_energy(self, circuit: stim.Circuit) -> float:
        """
        Calculate the energy cost of a stim circuit based on instruction counts.

        Args:
            circuit: The stim circuit.

        Returns:
            total_energy: The estimated energy cost.
        """
        energy = 0.0

        # Iterate over instructions and count
        # Note: flatten() might be needed if there are loops, but usually generated circuits
        # have REPEAT blocks. We can iterate recursively or flatten.
        # Flattening is safer for accurate counts.

        for instruction in circuit.flattened():
            name = instruction.name
            targets = len(instruction.targets_copy())

            # Simple heuristic mapping
            if name in ["H", "R", "X", "Y", "Z", "I", "S", "S_DAG", "SQRT_X", "SQRT_X_DAG", "SQRT_Y", "SQRT_Y_DAG"]:
                # Single qubit gates applied to 'targets' qubits
                energy += self.single_qubit_gate * targets
            elif name in ["CX", "CY", "CZ", "CNOT", "SWAP", "ISWAP", "SQRT_XX", "SQRT_YY", "SQRT_ZZ", "XCX", "XCY", "XCZ", "YCX", "YCY", "YCZ", "ZCX", "ZCY", "ZCZ"]:
                # Two qubit gates. Stim format: targets list contains pairs.
                # So number of gates is targets / 2
                num_gates = targets / 2
                energy += self.two_qubit_gate * num_gates
            elif name in ["M", "MX", "MY", "MZ", "MPP"]:
                # Measurement
                energy += self.measurement * targets
            elif name in ["R", "RX", "RY", "RZ"]:
                # Reset
                energy += self.reset * targets
            elif name in ["MR", "MRX", "MRY", "MRZ"]:
                # Measure and Reset
                energy += (self.measurement + self.reset) * targets
            elif name in ["DETECTOR", "OBSERVABLE_INCLUDE", "SHIFT_COORDS", "QUBIT_COORDS", "TICK"]:
                # Annotations cost nothing
                pass
            else:
                # Default for unknown or other gates (e.g. C_XYZ)
                # Treat as single qubit gate per target for safety, or log warning
                pass

        return energy
