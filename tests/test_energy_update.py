
import pytest
import stim
import sys
import os

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from energy.model import EnergyModel
from simulation.backend import QECSimulation
from codes.surface_code import SurfaceCode
from decoders.pymatching_decoder import PyMatchingDecoder

def test_decoding_energy_calculation():
    model = EnergyModel(decoding_event_cost=10.0)
    num_events = 5
    expected_cost = 5 * 10.0
    assert model.calculate_decoding_energy(num_events) == expected_cost

def test_simulation_integrates_decoding_energy():
    # This test checks if decoding energy is added to the total energy.

    # 1. Setup a simulation
    d = 3
    code = SurfaceCode(distance=d)

    # Use a high cost for decoding events to make it obvious,
    # and 0 cost for circuit ops to isolate it (if possible, but circuit ops are hardcoded in model defaults if not overridden)
    model = EnergyModel(
        single_qubit_gate=0,
        two_qubit_gate=0,
        measurement=0,
        reset=0,
        decoding_event_cost=100.0
    )

    sim = QECSimulation(code, model)

    # 2. Run with high error rate to guarantee some defects
    shots = 100
    p = 0.1
    result = sim.run(p, shots, PyMatchingDecoder)

    # 3. Assert energy is non-zero (since circuit energy is 0, all energy comes from decoding)
    # Note: It's statistically possible but unlikely to have 0 defects in 100 shots at p=0.1
    assert result.total_energy > 0

    # Also verify that energy is a multiple of the cost (100.0)
    # Since total_energy = sum(defects) * 100.0
    assert result.total_energy % 100.0 == 0.0

def test_simulation_zero_error_zero_decoding_energy():
    # If p=0, there should be no defects, so decoding energy should be 0.
    # Total energy should be just circuit energy.

    d = 3
    code = SurfaceCode(distance=d)
    model = EnergyModel(decoding_event_cost=100.0) # High cost to be sure
    sim = QECSimulation(code, model)

    shots = 10
    p = 0.0
    result = sim.run(p, shots, PyMatchingDecoder)

    # Calculate expected circuit energy
    circuit = code.generate_circuit(physical_error_rate=p)
    expected_circuit_energy = model.calculate_circuit_energy(circuit) * shots

    assert result.total_energy == expected_circuit_energy
