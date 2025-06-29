import stim

from codes.surface_code import SurfaceCode
from decoders.simple import SimpleDecoder
from noise.channels import DepolarizingNoise
from simulation.backend import StimSimulator
from energy.model import EnergyModel


def test_surface_code_cycle():
    code = SurfaceCode(distance=2)
    circuit = code.generate_circuit()
    noise = DepolarizingNoise(0.1)
    sim = StimSimulator()
    results = sim.run(circuit, noise, shots=1)
    syndrome = results[0].tolist()
    decoder = SimpleDecoder()
    correction = decoder.decode(syndrome)
    assert correction is None or isinstance(correction, tuple)


def test_energy_model():
    circuit = stim.Circuit()
    circuit.append_operation("H", [0])
    circuit.append_operation("CNOT", [0, 1])
    circuit.append_operation("M", [0, 1])

    model = EnergyModel(single_qubit_gate=1.0, two_qubit_gate=2.0, measurement=0.5)
    energy = model.compute_circuit_energy(circuit)
    assert energy == 1.0 + 2.0 + 0.5
