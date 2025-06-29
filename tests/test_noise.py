import stim

from noise.channels import DepolarizingNoise, AmplitudeDampingNoise


def test_noise_application():
    circuit = stim.Circuit("H 0")
    depol = DepolarizingNoise(0.1)
    amp = AmplitudeDampingNoise(0.05)

    circ1 = depol.apply(circuit)
    circ2 = amp.apply(circuit)

    assert isinstance(circ1, stim.Circuit)
    assert isinstance(circ2, stim.Circuit)
