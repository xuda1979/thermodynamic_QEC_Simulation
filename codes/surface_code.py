"""Placeholder for a surface code implementation."""

from .base import QECCode


class SurfaceCode(QECCode):
    """Simple surface code skeleton."""

    def __init__(self, distance: int):
        self.distance = distance

    def generate_circuit(self):
        """Generate the stabilizer measurement circuit (placeholder)."""
        pass

    def decode(self, syndrome):
        """Decode the given syndrome (placeholder)."""
        pass
