"""Energy accounting utilities."""

from dataclasses import dataclass


@dataclass
class EnergyModel:
    """Simple energy cost model."""

    single_qubit_gate: float = 0.0
    two_qubit_gate: float = 0.0
    measurement: float = 0.0
    reset: float = 0.0

    def compute_circuit_energy(self, circuit) -> float:
        """Estimate energy based on operation counts."""
        energy = 0.0
        for op in circuit:
            name = op.name
            if name in {"H", "X", "Y", "Z"}:
                energy += self.single_qubit_gate
            elif name in {"CX", "CNOT"}:
                energy += self.two_qubit_gate
            elif name == "M":
                energy += self.measurement
        return energy
