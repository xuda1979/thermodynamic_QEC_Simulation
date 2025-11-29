
import pytest
import stim
import sys
import os

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from codes.surface_code import SurfaceCode
from decoders.pymatching_decoder import PyMatchingDecoder
from energy.model import EnergyModel
from simulation.backend import QECSimulation

def test_surface_code_generation():
    d = 3
    code = SurfaceCode(distance=d)
    circuit = code.generate_circuit()
    assert isinstance(circuit, stim.Circuit)
    # Check if circuit seems reasonable (not empty)
    assert len(circuit.flattened()) > 0

def test_pymatching_decoder_init():
    d = 3
    code = SurfaceCode(distance=d)
    circuit = code.generate_circuit()
    decoder = PyMatchingDecoder(circuit)
    assert decoder.matcher is not None

def test_energy_model_calculation():
    model = EnergyModel()
    # Simple circuit: H 0, CNOT 0 1, M 0 1
    circuit = stim.Circuit("""
        H 0
        CX 0 1
        M 0 1
    """)
    # Costs:
    # H (single): 1.0 * 1 = 1.0
    # CX (two): 2.0 * 1 = 2.0
    # M (meas): 5.0 * 2 = 10.0
    # Total: 13.0
    energy = model.calculate_circuit_energy(circuit)
    assert energy == 13.0

def test_simulation_run():
    d = 3
    shots = 10
    p = 0.001
    code = SurfaceCode(distance=d)
    energy_model = EnergyModel()
    sim = QECSimulation(code, energy_model)

    result = sim.run(p, shots, PyMatchingDecoder)

    assert result.total_shots == shots
    assert result.total_energy > 0
    assert 0 <= result.logical_errors <= shots
