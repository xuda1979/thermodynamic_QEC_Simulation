"""Energy accounting utilities."""

from dataclasses import dataclass


@dataclass
class EnergyModel:
    """Simple energy cost model."""

    single_qubit_gate: float = 0.0
    two_qubit_gate: float = 0.0
    measurement: float = 0.0
    reset: float = 0.0
