import numpy as np


class ADC:
    """
    Analog-to-Digital Converter model.

    Includes:
        - sampling
        - quantization
    """

    def __init__(self, num_bits=12, v_ref=1.0):
        self.num_bits = num_bits
        self.v_ref = v_ref

    def quantize(self, signal):
        """
        Uniform quantization model.
        """
        max_level = 2**self.num_bits - 1

        normalized = signal / self.v_ref
        normalized = np.clip(normalized, -1, 1)

        quantized = np.round(normalized * max_level) / max_level
        return quantized

    def sample(self, analog_signal):
        """ADC sampling + quantization."""
        return self.quantize(analog_signal)
