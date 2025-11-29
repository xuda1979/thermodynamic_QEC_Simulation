"""Simulation backend abstractions."""

from abc import ABC, abstractmethod
import stim
from energy.model import EnergyModel
from decoders.base import Decoder

class SimulationResult:
    def __init__(self, logical_errors: int, total_shots: int, total_energy: float):
        self.logical_errors = logical_errors
        self.total_shots = total_shots
        self.total_energy = total_energy

    @property
    def logical_error_rate(self):
        return self.logical_errors / self.total_shots

    @property
    def average_energy_per_shot(self):
        return self.total_energy / self.total_shots

class QECSimulation:
    def __init__(self, code, energy_model: EnergyModel):
        self.code = code
        self.energy_model = energy_model

    def run(self, physical_error_rate: float, shots: int, decoder_class) -> SimulationResult:
        """
        Run the full QEC simulation.

        Args:
            physical_error_rate: The physical error rate (p).
            shots: Number of shots.
            decoder_class: The class of the decoder to use (e.g. PyMatchingDecoder).

        Returns:
            SimulationResult containing error rates and energy consumption.
        """
        # 1. Generate Circuit with Noise
        # Using the simplified "generate_circuit" which uses built-in stim params
        circuit = self.code.generate_circuit(physical_error_rate=physical_error_rate)

        # 2. Calculate Energy
        circuit_energy = self.energy_model.calculate_circuit_energy(circuit)
        total_energy = circuit_energy * shots

        # 3. Compile Sampler
        sampler = circuit.compile_detector_sampler()

        # 4. Run Simulation
        detection_events, observable_flips = sampler.sample(shots, separate_observables=True)

        # 5. Decode
        decoder = decoder_class(circuit)
        predictions = decoder.decode_shots(detection_events)

        # 6. Count Errors
        import numpy as np
        num_errors = np.sum(np.any(predictions != observable_flips, axis=1))

        return SimulationResult(num_errors, shots, total_energy)
