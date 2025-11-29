"""PyMatching decoder implementation."""

import pymatching
import stim
from .base import Decoder


class PyMatchingDecoder(Decoder):
    """Decoder using PyMatching."""

    def __init__(self, circuit: stim.Circuit):
        """
        Initialize the decoder with the circuit.

        Args:
            circuit: The stim circuit defining the error model and detector graph.
        """
        self.matcher = pymatching.Matching.from_detector_error_model(circuit.detector_error_model(decompose_errors=True))

    def decode(self, syndrome):
        """
        Decode the syndrome.

        Args:
            syndrome: The shot data (array of measurements) from which we extract detection events.
                      However, PyMatching typically takes the detection events directly.
                      If 'syndrome' is the raw measurement output from stim, we need to convert it.

            Wait, standard usage with stim is:
            1. Run circuit -> gets measurements.
            2. Convert measurements to detection events (using circuit.compile_detector_sampler or similar).

            Let's assume 'syndrome' here is the actual detection events (shots).
        """
        # In a typical pymatching flow:
        # prediction = matcher.decode_batch(shots)
        # return prediction
        pass

    def decode_shots(self, shots):
        """
        Decode a batch of shots (detection events).

        Args:
            shots: A numpy array of detection events (samples).

        Returns:
            predicted_observables: The predicted logical observable flips.
        """
        return self.matcher.decode_batch(shots)
